from typing import Dict, Any, List, Optional
import requests
import json
import re
from datetime import date
from urllib.parse import urlencode

import os
from dotenv import load_dotenv

load_dotenv()

OPEN_ROUTER_KEY = os.getenv('OPEN_ROUTER_KEY', None)

# Dicts of filters for https://bolshayastrana.com
regions = {
    "Адыгея": "3",
    "Алтай": "1",
    "Антарктида": "47",
    "Арктика": "50",
    "Архангельская область": "2",
    "Архыз": "31",
    "Астраханская область": "68",
    "Байкал": "4",
    "Башкирия": "78",
    "Белгородская область": "36",
    "Бурятия": "57",
    "Владивосток": "28",
    "Владимирская область": "46",
    "Волгоградская область": "101",
    "Вологодская область": "74",
    "Воронежская область": "37",
    "Дагестан": "26",
    "Дальний Восток": "82",
    "Домбай": "27",
    "Забайкальский край": "173",
    "Золотое кольцо": "134",
    "Ивановская область": "49",
    "Ингушетия": "29",
    "Кабардино-Балкария": "32",
    "Кавказ": "5",
    "Кавказские Минеральные Воды": "205",
    "Казань": "56",
    "Калининград": "57",
    "Калининградская область": "48",
    "Калмыкия": "19",
    "Калужская область": "33",
    "Камчатка": "13",
    "Карачаево-Черкесия": "28",
    "Карелия": "14",
    "Кемеровская область": "202",
    "Кольский полуостров": "15",
    "Коми": "56",
    "Костромская область": "44",
    "Краснодарский край": "94",
    "Красноярский край": "55",
    "Крым": "16",
    "Ленинградская область": "42",
    "Липецкая область": "45",
    "Магаданская область": "41",
    "Малое Золотое кольцо": "131",
    "Марий Эл": "133",
    "Москва": "82",
    "Московская область": "75",
    "Мурманская область": "85",
    "Ненецкий автономный округ": "51",
    "Нижегородская область": "53",
    "Новгородская область": "102",
    "Орловская область": "34",
    "Пермский край": "64",
    "Плато Путорана": "11",
    "Приморье": "9",
    "Псковская область": "39",
    "Ростовская область": "69",
    "Рязанская область": "35",
    "Самарская область": "157",
    "Санкт-Петербург": "132",
    "Саратовская область": "166",
    "Сахалин и Курильские острова": "8",
    "Свердловская область": "98",
    "Северная Осетия": "30",
    "Северный Полюс": "7",
    "Серебряное кольцо": "135",
    "Сибирь": "12",
    "Смоленская область": "155",
    "Ставропольский край": "103",
    "Таймыр": "72",
    "Тамбовская область": "100",
    "Татарстан": "95",
    "Тверская область": "38",
    "Тульская область": "43",
    "Тыва (Тува)": "25",
    "Тюменская область": "97",
    "Удмуртия": "73",
    "Ульяновская область": "96",
    "Урал": "10",
    "Хабаровский край": "52",
    "Хакасия": "24",
    "Челябинская область": "83",
    "Чечня": "21",
    "Чувашия": "161",
    "Чукотка": "18",
    "Шантарские острова": "22",
    "Шерегеш": "79",
    "Шпицберген": "86",
    "Эльбрус": "23",
    "Якутия": "6",
    "Ямал": "54",
    "Ярославская область": "40"
}

restKinds = {
    "Велотуры": "9",
    "Вертолетные туры": "20",
    "Восхождения": "10",
    "Горнолыжные туры": "11",
    "Дайвинг и снорклинг": "12",
    "Джип-туры": "13",
    "ЖД туры": "31",
    "Каньонинг": "23",
    "Комбинированные туры": "15",
    "Конные туры": "16",
    "Лыжные походы": "19",
    "Пешие туры": "7",
    "Рыболовные туры": "21",
    "Серфинг и SUP-туры": "14",
    "Сплавы": "8",
    "Туры на квадроциклах": "6",
    "Туры на снегоходах": "5",
    "Туры на собачьих упряжках": "4",
    "Фитнес и йога-туры": "22",
    "Экскурсионные туры": "18",
    "Экспедиции": "3",
    "Яхтинг": "1"
}

collections = {
    "Автобусные туры": "105",
    "Айс-флоатинг": "156",
    "Бесплатная отмена бронирования": "15",
    "Винные туры": "33",
    "Гастрономические туры": "35",
    "Избинг": "154",
    "Исторические туры": "91",
    "Корпоративные туры": "23",
    "Литературные туры": "87",
    "Мистические туры": "90",
    "На рафтах": "67",
    "Национальные туристические маршруты России": "123",
    "Необычные туры": "80",
    "Обзорные туры": "79",
    "Оздоровительные туры": "61",
    "Отдых с детьми": "6",
    "Познавательные туры": "89",
    "Популярные туры": "86",
    "Походы без рюкзаков": "118",
    "Проживание в глэмпинге": "19",
    "Промышленные туры": "155",
    "Событийные туры": "88",
    "Спа-туры": "111",
    "Спелеотуры": "108",
    "Туры для пенсионеров": "75",
    "Туры к Деду Морозу": "78",
    "Туры к петроглифам": "85",
    "Туры на байдарках": "63",
    "Туры на каяках": "110",
    "Туры на термальные источники": "20",
    "Туры на хивусах": "106",
    "Туры на Черную пятницу": "141",
    "Туры с наблюдением за дикими животными": "103",
    "Туры с северным сиянием": "24",
    "Туры, в которые можно с собакой": "59",
    "Фототуры": "52",
    "Экологические туры": "38",
    "Этнотуры": "57"
}

accommodation = {
    "Палатка": "tent",
    "Гостиница": "hotel",
    "Каюта": "cabin",
    "Квартира": "flat",
    "Поезд": "train",
    "Турбаза": "camp-site",
    "Гостевой дом": "guest-house",
    "Без проживания": "not-set"
}

comfort = {
    "Базовый": {
        "value": "base",
        "description": "Туристы живут в палатках, кемпингах или хижинах. Удобств нет или они находятся на улице"
    },
    "Простой": {
        "value": "base_plus",
        "description": "Гостевые дома или гостиницы 1* (одна звезда). Удобства могут быть в каждом номере или на этаже"
    },
    "Средний": {
        "value": "medium",
        "description": "Апартаменты, коттеджи или гостиницы 2* (две звезды). Обычно есть удобства: питание и уборка"
    },
    "Выше среднего": {
        "value": "improved",
        "description": "Гостиницы 3* (три звезды) или виллы. Обычно удобства в каждом номере, на территории могут быть спа-зона, бассейн и тренажерный зал"
    },
    "Высокий": {
        "value": "premium",
        "description": "Гостиницы 4 и 5* (четыре и пять звёзд), бутик-отели или глэмпинги. Часто включает в себя эксклюзивные услуги вроде собственного бассейна"
    }
}

difficulty = {
    "Легкий": {
        "value": "1",
        "description": "Физическая нагрузка минимальна. Подходит для всех, вне зависимости от физической подготовки и возраста"
    },
    "Средний": {
        "value": "2",
        "description": "Не требует физической подготовки, но предполагает умеренную физическую нагрузку"
    },
    "Интенсивный": {
        "value": "3",
        "description": "Не требует специальных навыков, но туристы должны быть в хорошей физической форме"
    },
    "Экстремальный": {
        "value": "4",
        "description": "Только для опытных и физически подготовленных туристов. Нужны специальные навыки и снаряжение"
    }
}


def check_url(url: str, timeout: int = 15) -> bool:
    """
    Проверяет, доступна ли ссылка, возвращает True, если статус ответа 200.

    Args:
        url (str): URL для проверки.
        timeout (int, optional): Таймаут запроса в секундах. По умолчанию 5 секунд.

    Returns:
        bool: True, если ссылка отвечает статусом 200, иначе False.
    """
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error checking URL {url}: {e}")
        return False



def build_filtered_url(base_url: str, filters: Dict[str, Any]) -> str:
    """Build URL with filter parameters, supporting multiple values per key, and always including /tury?plainSearch=1"""
    if not filters:
        return f"{base_url}/tury?plainSearch=1"

    expanded_params = []
    for key, value in filters.items():
        if isinstance(value, list):
            for v in value:
                expanded_params.append((key, v))
        else:
            expanded_params.append((key, value))

    query_string = urlencode(expanded_params, doseq=True)
    return f"{base_url}/tury?plainSearch=1&{query_string}"



def transform_filter_values(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms filter values for the following keys:
      'regions', 'restKinds', 'collections', 'comfort', 'difficulty', 'accommodation'
    by replacing display names with corresponding codes from the mapping dictionaries.

    The mapping dictionaries (regions, restKinds, etc.) must be defined in the environment,
    each of which has the structure:
        'Name': 'Code'
    or for filters with additional info (like comfort, difficulty):
        'Name': {'value': 'Code', 'description': '...'}
    
    Args:
        filters (Dict[str, Any]): Input filters with possible multiple values (list) for the keys.
    
    Returns:
        Dict[str, Any]: The filters dictionary with transformed values for the specified keys.
    """

    mappings = {
        'regions': regions, 
        'restKinds': restKinds,
        'collections': collections,
        'comfort': comfort,
        'difficulty': difficulty,
        'accommodation': accommodation,
    }
    
    new_filters = dict(filters)
    
    for key, mapping_dict in mappings.items():
        if key in filters:
            original_value = filters[key]
            if not isinstance(original_value, list):
                original_value = [original_value]
            transformed_values: List[str] = []
            for item in original_value:
                if item in mapping_dict:
                    code = mapping_dict[item]
                    if isinstance(code, dict):
                        transformed_values.append(code.get('value', item))
                    else:
                        transformed_values.append(code)
                else:
                    transformed_values.append(item)
            new_filters[key] = transformed_values
    return new_filters



def extract_filters_llm(user_query: str, filter_definitions: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract filter parameters from user query using LLM.
    
    Args:
        user_query: User's natural language query
        filter_definitions: Dictionary with all available filters and their descriptions
        
    Returns:
        Dictionary with extracted filter parameters (URL param name -> value)
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    filter_descriptions = []

    for name, values in filter_definitions.items():
        if isinstance(values, dict) and all(isinstance(v, dict) and 'description' in v for v in values.values()):
            # Filters with additional description
            if name == "comfort":
                desc = ("comfort: Specifies the level of comfort provided by the tour. "
                        "Options: " + ", ".join([f'''"{k}" - {v['description']}''' for k, v in values.items()]))
            elif name == "difficulty":
                desc = ("difficulty: Specifies the physical difficulty of the tour. "
                        "Options: " + ", ".join([f'''"{k}" - {v['description']}''' for k, v in values.items()]))
            else:
                desc = f"{name}: " + ", ".join([f'''"{k}" - {v['description']}''' for k, v in values.items()])
        elif isinstance(values, dict):
            if name == "regions":
                desc = ("regions: Specifies the Russian region where the tour is available. "
                        "Options: " + ", ".join(values.keys()))
            elif name == "restKinds":
                desc = ("restKinds: Specifies the type of tour or activity. "
                        "Options: " + ", ".join(values.keys()))
            elif name == "collections":
                desc = ("collections: Specifies the tour collection or theme. "
                        "Options: " + ", ".join(values.keys()))
            elif name == "accommodation":
                desc = ("accommodation: Specifies the lodging type provided during the tour. "
                        "Options: " + ", ".join(values.keys()))
            else:
                desc = f"{name}: " + ", ".join(values.keys())
        else:
            # Фильтры-скалярные значения (одиночные параметры)
            if name == "dateFrom":
                desc = (f"dateFrom: Tour start date; cannot be before today ({date.today()}). "
                        "If a past season or month is requested, the date is auto-adjusted to the next valid period "
                        "(e.g., in April 2025, an autumn request becomes Sept–Nov 2025, and a February request becomes February 2026).")
            elif name == "dateTo":
                desc = ("dateTo: Tour end date; must be later than dateFrom and match the adjusted seasonal period.")
            elif name == "sort":
                desc = ("sort: Defines the sorting order of tour results. "
                        "Possible values include 'default' (by popularity), 'price' (ascending), and '-price' (descending).")
            elif name == "priceMin":
                desc = "priceMin: Specifies the minimum total price for the tour in rubles."
            elif name == "priceMax":
                desc = ("priceMax: Specifies the maximum total price for the tour in rubles. "
                        "When using total price filters (priceMin, priceMax), per-day filters (pricePerDayMin, pricePerDayMax) should not be used.")
            elif name == "pricePerDayMin":
                desc = "pricePerDayMin: Specifies the minimum price per day for the tour in rubles."
            elif name == "pricePerDayMax":
                desc = ("pricePerDayMax: Specifies the maximum price per day for the tour in rubles. "
                        "When using per-day price filters (pricePerDayMin, pricePerDayMax), total price filters (priceMin, priceMax) should not be used.")
            elif name == "daysMin":
                desc = "daysMin: Defines the minimum duration of the tour in days."
            elif name == "daysMax":
                desc = "daysMax: Defines the maximum duration of the tour in days."
            elif name == "minAge":
                desc = ("minAge: Specifies the minimum allowed participant age. "
                        "This filter ensures that the tour is appropriate for the intended age group (from 0 to 18, where 18 means no age filter).")
            elif name == "maxGroupSize":
                desc = ("maxGroupSize: Specifies the maximum number of participants allowed in the tour group. "
                        "This filter is used to maintain an optimal group size for the tour experience.")
            else:
                desc = f"{name}: {values}"
        filter_descriptions.append(desc)

    filter_desc_str = "\n".join(filter_descriptions)

    prompt = f"""
Extract tour filter parameters from this user query: '{user_query}'
Available filters with descriptions:
{filter_desc_str}

Return ONLY a JSON dictionary where:
- Key is the URL parameter name (e.g. 'regions', 'comfort', 'daysMin')
- Value is the corresponding code/value from filter definitions
- Include ONLY parameters that are clearly mentioned in the query
- Use English for keys and thinking, but user query is in Russian

Example output for "Хочу тур в Карелию или на Байкал с 12 по 15 мая, на 3–4 дня, бюджетом от 100000 до 183000 рублей, для группы из 5 человек максимум, чтобы можно было жить в гостинице или гостевом доме. Уровень комфорта — выше среднего. Интересуют пешие туры, экскурсии и фототуры. Пусть тур будет лёгким или средним по сложности, с проживанием обязательно, с ребёнком 9 лет. Важно: бесплатная отмена и необычный формат.":
{{
    "regions": ["14", "4"],
    "dateFrom": "2025-05-12",
    "dateTo": "2025-05-15",
    "daysMin": "3",
    "daysMax": "4",
    "priceMin": "100000",
    "priceMax": "183000",
    "maxGroupSize": "5",
    "accommodation": ["hotel", "guest-house"],
    "comfort": "improved",
    "restKinds": ["7", "18", "52"],
    "difficulty": ["1", "2"],
    "minAge": "9",
    "collections": ["15", "80"]
}}

Repeat of user query: '{user_query}'
"""
    messages = [
        {"role": "system", "content": ("You are a helpful assistant that converts a user's query into a JSON format according to provided example. "
                                       "Use the given filter definitions and ensure the output is a properly structured JSON object with the required keys and values. "
                                       "Respond only with JSON when instructed, and do not include additional commentary.")},
        {"role": "user", "content": prompt}
    ]
    
    payload = {
        "model": "openai/gpt-4o",  
        "messages": messages,
        "temperature": 0,
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "{}")

        try:
            return transform_filter_values(json.loads(content))
        except json.JSONDecodeError:
            content_cleaned = re.sub(r"^```json\s*|\s*```$", "", content.strip(), flags=re.DOTALL)

            try:
                return transform_filter_values(json.loads(content_cleaned))
            except json.JSONDecodeError:
                match = re.search(r"\{.*\}", content, re.DOTALL)
                if match:
                    try:
                        return transform_filter_values(json.loads(match.group(0)))
                    except json.JSONDecodeError as e:
                        print(f"Error extracting filters: {e} \nContent: \n{content}")
    except Exception:
        return {}



def search_tours_with_llm(user_query: str, site_urls: List[str] = None, search_url: Optional[str] = None, tours_qty: int = 3) -> Dict[str, Any]:
    """
    Search for tours using OpenRouter's GPT-4o search preview.

    Args:
        user_query (str): A natural language request from the user describing desired tour parameters 
                          (e.g. destination, dates, budget, type of activity, accommodation, etc.).

        site_urls (List[str], optional): A list of travel site URLs that can be used for searching. 
                                         If search_url is not specified, the model can use any of these.

        search_url (Optional[str]): A specific URL to strictly limit the search to a single website. 
                                    If provided, only this site will be used for data retrieval.

        tours_qty (int): The number of tour options to return in the response. Default is 3.

    Returns:
        Dict[str, Any]: A dictionary containing search results or error details.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    if search_url:
        search_instruction = (
            f"You must find relevant tours strictly from the following website: {search_url}.\n"
            f"Use only this specific website and do not include results from other sources.\n\n"
            f"The user's search criteria are:\n{user_query}\n"
        )
    else:
        search_instruction = (
            f"You must find relevant tours strictly from the following websites: {', '.join(site_urls)}.\n"
            f"Use only this specific websites and do not include results from other sources.\n\n"
            f"The user's search criteria are:\n{user_query}\n"
        )

    user_prompt = f"""
You are an expert tour operator and consultant specializing in domestic tourism in Russia. Your task is to select the most suitable options for tours, excursions, routes, and events in a specific region of Russia based on the user's request. Take into account all preferences and parameters provided by the user: travel dates, budget, number of participants, interests (nature, culture, gastronomy, active leisure, and others), duration, type of accommodation, transportation, and more.
Your goal is to find and offer a list of the most relevant and diverse options according to the request. Always think like a professional tour operator who understands the specifics of each region, seasonality, logistics, current offers, and events.

{search_instruction}

**Your response format should include:**
- Tour/Excursion name  
- Brief description  
- Key points of the route  
- Duration (with start and end dates)  
- Price  
- What’s included  
- What’s not included  
- Special features (e.g. route difficulty, comfort level, meals provided, etc.)  
- URL for viewing and booking the tour (**this is the most important field — provide only valid, direct, working links without 404 errors**)  

Provide a list of **{tours_qty} options** and comment on which one best fits the given parameters.

Answer only in Russian language (отвечай на русском языке).
    """
    messages = [
        {"role": "system", "content": ("You are an expert tour operator and consultant specializing in domestic tourism in Russia. "
            "Your task is to help convert user requests into structured tour options by searching the provided website(s). "
            "Be precise and return only valid, working tour information.")},
        {"role": "user", "content": user_prompt}
    ]
    payload = {
        # "model": "google/gemini-2.5-pro-preview-03-25",  
        "model": "openai/gpt-4o-search-preview",  
        "messages": messages,
        "plugins": [
            {
                "id": "web",
                "max_results": 5,
                "search_prompt": search_instruction
            }
        ],
        "temperature": 0,
        "top_p": 1,
        "seed": 0,
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


    
def search_tool(user_query: str, site_urls=['https://bolshayastrana.com']):

    filter_definitions = {
        'regions': regions,
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

    filters = extract_filters_llm(user_query, filter_definitions)
    
    if filters:
        base_url = f"{site_urls[0]}"
        search_url = build_filtered_url(base_url, filters)
        if check_url(url=search_url, timeout=15):
            answer_json = search_tours_with_llm(user_query=user_query, search_url=search_url, tours_qty=3)
            if "choices" in answer_json and answer_json["choices"]:
                return f'Используемая ссылка для поиска по вашему запросу: \n{search_url} \n\n\n{answer_json["choices"][0]["message"]["content"]}'
            else:
                return f'Произошла ошибка: {json.dumps(answer_json, indent=2, ensure_ascii=False)}'
        else:
            answer_json = search_tours_with_llm(user_query=user_query, site_urls=site_urls, tours_qty=3)
            if "choices" in answer_json and answer_json["choices"]:
                return f'Используемая ссылка для поиска по вашему запросу:\n {search_url} \n\n\n{answer_json["choices"][0]["message"]["content"]}'
            else:
                return f'Произошла ошибка: {json.dumps(answer_json, indent=2, ensure_ascii=False)}'
