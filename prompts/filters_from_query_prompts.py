EXTRACT_FILTERS_SYSTEM_PROMPT = """\
You are a helpful assistant that converts a user's query into a JSON format according to provided example.
Use the given filter definitions and ensure the output is a properly structured JSON object with the required keys and values.
Respond only with JSON when instructed, and do not include additional commentary.
"""

EXTRACT_FILTERS_USER_PROMPT = """\
Extract tour filter parameters from this user query: '{user_query}'
Available filters with descriptions:
{filter_desc_str}

Return ONLY a JSON dictionary where:
- Key is the URL parameter name (e.g. 'regions', 'comfort', 'daysMin', 'priceMax')
- Value is the corresponding code/value from filter definitions
- Include ONLY parameters that are clearly mentioned in the query
- Use English for keys and thinking, but user query is in Russian

Example:
User query: "Хочу тур в Карелию или на Байкал с 12 по 15 мая, на 3–4 дня, бюджетом от 100000 до 183000 рублей, для группы из 5 человек максимум, чтобы можно было жить в гостинице или гостевом доме. Уровень комфорта — выше среднего. Интересуют пешие туры, экскурсии и фототуры. Пусть тур будет лёгким или средним по сложности, с проживанием обязательно, с ребёнком 9 лет. Важно: бесплатная отмена и необычный формат." 
Assistant answer (yours):
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
