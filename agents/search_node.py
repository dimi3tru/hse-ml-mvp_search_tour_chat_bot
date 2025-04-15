from models.agent_state import AgentState
from core.search_tool import search_tool
from core.web_search_tool import web_search_tool

def prepare_search_query(search_params):
    """Подготавливает поисковый запрос из структуры search_params."""
    # Если имеются данные параметров поиска
    if "search_params_data" in search_params:
        # Формируем строку запроса из значений предоставленных параметров
        query_parts = []
        for param, details in search_params["search_params_data"].items():
            if details.get("предоставлено", False):
                value = details.get("значение", "")
                if value and value.lower() not in ["любые", "любое", "любой", "любая"]:
                    query_parts.append(f"{param}: {value}")
        
        return ", ".join(query_parts)
    
    # Если используется старый формат или отсутствуют параметры
    return "Поиск тура по предоставленным параметрам"

def search_node(state: AgentState) -> AgentState:
    """
    Выполняет поиск туров или вариантов размещения на основе предоставленных параметров.
    
    Использует web_search_tool для поиска в интернете с помощью gpt-4o-search-preview.
    В случае ошибки или недоступности, использует резервный метод search_tool.
    
    Args:
        state: AgentState с параметрами поиска
        
    Returns:
        Обновленный AgentState с результатами поиска
    """
    print("Заходим в search_node")
    
    # Получаем структуру search_params
    search_params = state.get("search_params", {})

    print("Извлеченные параметры поиска search_params: ", search_params)
    
    # Формируем поисковый запрос из предоставленных параметров
    search_query = prepare_search_query(search_params)

    print("Поисковый запрос: ", search_query)
    
    # try:
    #     # Пробуем использовать web_search_tool для расширенного поиска
    #     print("Запускаем веб-поиск через web_search_tool...")
    #     search_result = web_search_tool(search_query)
        
    # except Exception as e:
    #     # В случае ошибки используем резервный метод
    #     print(f"Ошибка при использовании web_search_tool: {str(e)}")
    #     print("Используем резервный метод search_tool...")
    search_result = search_tool(search_query)
    
    # Сохраняем результат в состоянии
    state["result"] = search_result
    
    return state
