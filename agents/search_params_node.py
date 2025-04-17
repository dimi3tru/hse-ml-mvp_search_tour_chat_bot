from models.agent_state import AgentState
import time
from prompts.prompts import CHECK_SEARCH_PARAMS_USER_PROMPT, CHECK_SEARCH_PARAMS_SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.config import llm_deepseek_chat_v3_free
from tools.json_extractor import extract_json

# Создаем шаблон промпта
params_check_prompt = ChatPromptTemplate.from_messages([
    ("system", CHECK_SEARCH_PARAMS_SYSTEM_PROMPT),
    ("human", CHECK_SEARCH_PARAMS_USER_PROMPT)
])

# Создаем цепочку обработки
params_check_chain = params_check_prompt | llm_deepseek_chat_v3_free | StrOutputParser()

# Константы
LLM_TIMEOUT = 90  # Таймаут в секундах для вызова LLM
MAX_RETRIES = 2   # Максимальное количество попыток

def collect_dialog_context(state: AgentState) -> str:
    """Сбор контекста диалога из текущего запроса и истории чата."""
    user_input = state.get("input", "")
    chat_history = state.get("chat_history", [])
    
    full_context = user_input
    if chat_history:
        for message in chat_history:
            if hasattr(message, 'content') and hasattr(message, 'type'):
                content = message.content
                msg_type = message.type
                if msg_type == 'human':
                    full_context += f"\nПользователь: {content}"
                elif msg_type == 'ai':
                    full_context += f"\nАссистент: {content}"
    
    return full_context

def call_llm_with_timeout(context: str) -> dict:
    """Вызов LLM с таймаутом для предотвращения зависания."""
    default_result = {
        "все_параметры_предоставлены": False, 
        "параметры": {
            "даты": {"предоставлено": False, "значение": ""},
            "направление": {"предоставлено": False, "значение": ""},
            "бюджет": {"предоставлено": False, "значение": ""},
            "продолжительность": {"предоставлено": False, "значение": ""},
            "уровень_комфорта": {"предоставлено": False, "значение": ""},
            "размещение": {"предоставлено": False, "значение": ""}
        }, 
        "сбросить_поиск": False,
        "исходный_запрос": context
    }
    
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            print(f"Попытка вызова LLM {attempts+1}/{MAX_RETRIES}")
            start_time = time.time()
            
            # Устанавливаем контекст таймаута
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(params_check_chain.invoke, {"full_context": context})
                try:
                    content = future.result(timeout=LLM_TIMEOUT)
                    print(f"LLM ответил за {time.time() - start_time:.2f} секунд")
                    result = extract_json_from_response(content)
                    # Добавляем исходный запрос к результату
                    result["исходный_запрос"] = context
                    return result
                except concurrent.futures.TimeoutError:
                    print(f"Таймаут вызова LLM после {LLM_TIMEOUT} секунд ожидания")
                    attempts += 1
                    if attempts < MAX_RETRIES:
                        # Добавляем паузу перед повторной попыткой
                        print(f"Повторная попытка через 2 секунды...")
                        time.sleep(2)
                    continue
        
        except Exception as e:
            print(f"Ошибка при вызове LLM: {str(e)}")
            attempts += 1
            if attempts < MAX_RETRIES:
                print(f"Повторная попытка через 2 секунды...")
                time.sleep(2)
            else:
                print("Исчерпаны все попытки вызова LLM")
                break
    
    print("Возвращаю дефолтный результат из-за ошибки вызова LLM")
    return default_result

def extract_json_from_response(content: str) -> dict:
    """Извлечение JSON из ответа LLM с обработкой ошибок."""
    default_result = {
        "все_параметры_предоставлены": False, 
        "параметры": {
            "даты": {"предоставлено": False, "значение": ""},
            "направление": {"предоставлено": False, "значение": ""},
            "бюджет": {"предоставлено": False, "значение": ""},
            "продолжительность": {"предоставлено": False, "значение": ""},
            "уровень_комфорта": {"предоставлено": False, "значение": ""},
            "размещение": {"предоставлено": False, "значение": ""}
        }, 
        "сбросить_поиск": False
    }
    
    json_result = extract_json(content)
    
    # Проверяем, что результат является JSON-объектом
    if isinstance(json_result, dict):
        return json_result
    else:
        print(f"Неожиданная ошибка при обработке ответа LLM: \n{content}")
        return default_result

def log_missing_params(analysis_result: dict) -> None:
    """Логирование отсутствующих параметров для отладки."""
    if not analysis_result.get("все_параметры_предоставлены", False):
        print("Не все параметры для поиска предоставлены")
        missing_params = []
        
        if "параметры" in analysis_result:
            for param, details in analysis_result["параметры"].items():
                if not details.get("предоставлено", False):
                    missing_params.append(param)
            if missing_params:
                print(f"Отсутствующие параметры: {', '.join(missing_params)}")

def format_provided_params_for_prompt(params_data: dict) -> str:
    """Формирование строки с предоставленными параметрами для промпта."""
    if not params_data:
        return "пока нет предоставленных параметров"
    
    result = []
    for param, details in params_data.items():
        if details.get("предоставлено", False):
            value = details.get("значение", "")
            result.append(f"{param}: {value}")
    
    if not result:
        return "пока нет предоставленных параметров"
    
    return ", ".join(result)

def check_search_params_node(state: AgentState) -> AgentState:
    """Проверка наличия всех необходимых параметров для поиска тура 
    и сохранение предоставленных параметров."""
    print("Заходим в check_search_params_node")
    
    # Инициализируем search_params, если еще не создан
    if state.get("search_params") is None:
        state["search_params"] = {}
    
    # Сбор контекста диалога
    context = collect_dialog_context(state)
    
    # Вызов LLM для анализа параметров с таймаутом
    analysis_result = call_llm_with_timeout(context)
    
    # Проверяем, запросил ли пользователь сбросить параметры
    if analysis_result.get("сбросить_поиск", False):
        print("Пользователь запросил сбросить параметры поиска")
        # Сбрасываем параметры поиска
        state["search_params"] = {
            "search_params_data": {},
            "provided_params_str": "пока нет предоставленных параметров",
            "was_reset": True,  # Помечаем, что был сброс для логирования и отчета пользователю
            "user_query": "" 
        }
    
    # Если пользователь не запросил сброс, обрабатываем параметры
    if not analysis_result.get("сбросить_поиск", False):
        # Сохраняем параметры, которые были предоставлены
        if "параметры" in analysis_result:
            # Создаем структуру для хранения параметров, если еще не существует
            if "search_params_data" not in state["search_params"]:
                state["search_params"]["search_params_data"] = {}
                
            # Добавляем извлеченные параметры и их значения
            for param, details in analysis_result["параметры"].items():
                if details.get("предоставлено", False):
                    state["search_params"]["search_params_data"][param] = details
            
            # Для будущего использования в chat_node сохраняем строковое представление
            # предоставленных параметров
            state["search_params"]["provided_params_str"] = format_provided_params_for_prompt(
                analysis_result["параметры"]
            )

            # Сохраняем исходный запрос пользователя
            state["search_params"]["user_query"] = context
        
        # Если все параметры предоставлены, устанавливаем флаг для перехода к search_node
        if analysis_result.get("все_параметры_предоставлены", False):
            print("Все параметры для поиска предоставлены")
            state["search_params"]["all_provided"] = True
        else:
            log_missing_params(analysis_result)
            # Оставляем словарь search_params, но без флага all_provided
            # Это позволит сохранить уже введенные параметры
    
    return state
