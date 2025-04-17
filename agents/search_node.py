from models.agent_state import AgentState
from core.search_tool import search_tool

def search_node(state: AgentState) -> AgentState:
    """
    Выполняет поиск туров или вариантов размещения на основе предоставленных параметров.
    
    Использует метод search_tool.
    
    Args:
        state: AgentState с параметрами поиска
        
    Returns:
        Обновленный AgentState с результатами поиска
    """
    print("Заходим в search_node")
    
    # Получаем структуру search_params
    search_params = state.get("search_params", {})

    # Получаем исходный запрос пользователя, если доступен
    user_query = search_params.get("user_query", state.get("input", ""))
    
    # # Формируем запрос на основе извлеченных параметров
    # user_query = ""
    
    # if "search_params_data" in search_params:
    #     params_data = search_params.get("search_params_data", {})
    #     query_parts = []

    #     query_parts.append(f"Оригинальный запрос пользователя: {state.get("input", "Ответь, что запроса не было")}")

    #     query_parts.append("Далее тебе будет предоставлен параметризированный запрос пользователя")
        
    #     # Добавляем направление
    #     if "направление" in params_data and params_data["направление"].get("предоставлено", False):
    #         query_parts.append(f"Направление: {params_data['направление']['значение']}")
            
    #     # Добавляем даты
    #     if "даты" in params_data and params_data["даты"].get("предоставлено", False):
    #         query_parts.append(f"Даты: {params_data['даты']['значение']}")
            
    #     # Добавляем бюджет
    #     if "бюджет" in params_data and params_data["бюджет"].get("предоставлено", False):
    #         query_parts.append(f"Бюджет: {params_data['бюджет']['значение']}")
            
    #     # Добавляем продолжительность
    #     if "продолжительность" in params_data and params_data["продолжительность"].get("предоставлено", False):
    #         query_parts.append(f"Продолжительность: {params_data['продолжительность']['значение']}")
            
    #     # Добавляем уровень комфорта
    #     if "уровень_комфорта" in params_data and params_data["уровень_комфорта"].get("предоставлено", False):
    #         query_parts.append(f"Уровень комфорта: {params_data['уровень_комфорта']['значение']}")
            
    #     # Добавляем размещение
    #     if "размещение" in params_data and params_data["размещение"].get("предоставлено", False):
    #         query_parts.append(f"Размещение: {params_data['размещение']['значение']}")
        
    #     # Формируем окончательную строку запроса
    #     user_query = ". ".join(query_parts)
    
    # # Если запрос пустой, возьмем оригинальный ввод пользователя
    # if not user_query:
    #     user_query = state.get("input", "Ответь, что запроса не было")
    
    print(f"Подготовленный запрос для поиска: {user_query}")

    # Передаем строку запроса в search_tool
    search_result = search_tool(user_query)
    
    # Сохраняем результат в состоянии
    state["result"] = search_result
    
    return state
