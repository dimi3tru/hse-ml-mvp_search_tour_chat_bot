from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.config import llm_gpt_4o_search_preview
import json
from prompts.prompts import WEB_SEARCH_PROMPT

# Создаем цепочку LLM
web_search_prompt = ChatPromptTemplate.from_template(WEB_SEARCH_PROMPT)
web_search_chain = web_search_prompt | llm_gpt_4o_search_preview | StrOutputParser()

# Основная функция
def web_search_tool(search_query: str):    
    try:
        raw_response = web_search_chain.invoke({"search_query": search_query})
        print("[web_search_tool] Сырые данные от LLM:", raw_response[:300], "...")
        
        tours = json.loads(raw_response)
        if not isinstance(tours, list) or len(tours) != 7:
            raise ValueError("Ответ не содержит 7 туров или неверный формат")
        
        print("[web_search_tool] Успешно извлечено 7 туров")
        return tours
    
    except Exception as e:
        print(f"[web_search_tool] Ошибка при обработке запроса: {e}")
        return [{
            "title": "Ошибка при поиске туров",
            "description": "Не удалось получить туры из-за технической ошибки.",
            "reason": "Возможно, временные проблемы с моделью.",
            "price": None,
            "location": None,
            "dates": None,
            "additional_info": "Попробуйте повторить запрос позже.",
            "booking_url": None
        }]
