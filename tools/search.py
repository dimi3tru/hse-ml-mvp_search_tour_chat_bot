from typing import Dict, Any, List, Tuple, Optional
import requests
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from tools.config import gpt_4o, openai_gpt_4o_search_preview, MAX_URLS
from utils.json_extractor import extract_json
from utils.url_preprocessing import fetch_urls, build_filtered_url
from utils.bolshayastrana_filters import transform_filter_values, build_filter_descriptions
from utils.bolshayastrana_filters import regions, cities, restKinds, collections, accommodation, comfort, difficulty
from prompts.filters_from_query_prompts import EXTRACT_FILTERS_SYSTEM_PROMPT, EXTRACT_FILTERS_USER_PROMPT
from prompts.search_prompts import SEARCH_SYSTEM_PROMPT, SEARCH_USER_PROMPT



def extract_filters_llm(user_query: str, filter_definitions: Dict[str, Any], llm: ChatOpenAI = gpt_4o) -> Dict[str, Any]:
    """
    Uses a language model to extract structured filter parameters from a user's natural language query.

    Args:
        user_query (str): A user query written in natural language (e.g., in Russian).
        filter_definitions (Dict[str, Any]): A dictionary of all available filters and their descriptions.
        llm (Optional[ChatOpenAI]): A pre-configured ChatOpenAI instance to use for inference.
                                     If None, defaults to llm_gpt_4o.

    Returns:
        Dict[str, Any]: A dictionary mapping URL parameter names to their extracted values,
                        based on the filters explicitly or implicitly mentioned in the query.
    """

    filter_desc_str = build_filter_descriptions(filter_definitions)

    template = ChatPromptTemplate.from_messages([("system", EXTRACT_FILTERS_SYSTEM_PROMPT), ("human", EXTRACT_FILTERS_USER_PROMPT)])

    messages = template.format_messages(
        user_query=user_query,
        filter_desc_str=filter_desc_str
    )

    response = llm.invoke(messages)
    answer = response.content

    answer_parsed = extract_json(answer)
    return transform_filter_values(answer_parsed)



def search_with_llm(user_query: str, search_urls: List[str] = [], max_urls: int = MAX_URLS, 
                    llm: ChatOpenAI = openai_gpt_4o_search_preview) -> Dict[str, Any]:
    """
    Search for tours using OpenRouter's GPT-4o search preview.

    Args:
        user_query (str): A natural language request from the user describing desired tour parameters 
                          (e.g. destination, dates, budget, type of activity, accommodation, etc.).

        base_site_urls (List[str], optional): A list of travel site URLs that can be used for searching. 
                                         If search_url is not specified, the model can use any of these.

        search_url (Optional[str]): A specific URL to strictly limit the search to a single website. 
                                    If provided, only this site will be used for data retrieval.

        tours_qty (int): The number of tour options to return in the response. Default is 3.

    Returns:
        Dict[str, Any]: A dictionary containing search results or error details.
    """

    search_instruction = (
        f"You must find relevant tours strictly from the following website: {' \n'.join(search_urls)}. \n"
        f"Process them strictly in the order in which they are listed — from top to bottom. \n"
        f"Use only this specific website and do not include results from other sources. \n"
        f"Do NOT rely on general web results, summaries, or unrelated sources. \n\n"
        f"The user's search criteria are: \n{user_query} \n\n"
    )

    template = ChatPromptTemplate.from_messages([("system", SEARCH_SYSTEM_PROMPT), ("human", SEARCH_USER_PROMPT)])
    messages = template.format_messages(search_instruction=search_instruction, max_urls=max_urls)

    try:
        response = llm.invoke(messages, config={"plugins": [{"id": "web", 
                                                             "max_results": max_urls, 
                                                             "search_prompt": search_instruction}]})
        answer = response.content
        return answer
    
    except Exception as e:
        return f'ERROR: {e} \nResponse: {response}'


    
def search_tool(user_query: str, base_site_urls=['https://bolshayastrana.com', 'https://www.aviasales.ru/guides', 'https://www.russiadiscovery.ru/', 'https://www.rtoperator.ru/']):

    filter_definitions = {
        'regions': regions,
        'cities': cities,
        'restKinds': restKinds,
        'collections': collections,
        'comfort': comfort,
        'difficulty': difficulty,
        'accommodation': accommodation,
        # Examples
        'dateFrom': '2025-05-12',
        'dateTo': '2025-05-15',
        'sort': 'default',
        'priceMin': '5000',
        'priceMax': '183000',
        'pricePerDayMin': '1000',
        'pricePerDayMax': '26000',
        'daysMin': '1',
        'daysMax': '5',
        'minAge': '9',
        'maxGroupSize': '5'
    }

    filters = extract_filters_llm(user_query, filter_definitions, llm=gpt_4o)
    
    if filters:
        main_url = 'https://bolshayastrana.com'
        search_url = build_filtered_url(main_url, filters)
        valid_urls = fetch_urls(url=search_url, max_urls=MAX_URLS) # Tuple[List[str], bool]
        direct_urls, incomplete = valid_urls[0], valid_urls[1]

        if not direct_urls: # If no url
            search_urls = ['https://bolshayastrana.com', 'https://www.aviasales.ru/guides', 'https://www.russiadiscovery.ru/', 'https://www.rtoperator.ru/']
        elif direct_urls and not incomplete:
            search_urls = direct_urls
        else:
            default_urls = ['https://bolshayastrana.com', 'https://www.aviasales.ru/guides', 'https://www.russiadiscovery.ru/', 'https://www.rtoperator.ru/']
            search_urls = direct_urls + default_urls[:MAX_URLS - len(direct_urls)]

        answer = search_with_llm(user_query=user_query, search_urls=search_urls, 
                                 max_urls=MAX_URLS, llm=openai_gpt_4o_search_preview)
        if answer and "ERROR: " not in answer:
            return (f'**Сконструированная по вашему запросу ссылка**: {search_url}\n\n\n'
                    f'**Используемые ссылки для поиска по вашему запросу**: \n{' \n'.join(search_urls)}\n\n\n'
                    f'**Ответ**: \n{answer}')
        else:
            return f'Произошла ошибка: {answer}'
