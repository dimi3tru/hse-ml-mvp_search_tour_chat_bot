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

    print("Извлеченные параметры поиска search_params: ", search_params)

    search_result = search_tool(search_params)
    
    # Сохраняем результат в состоянии
    state["result"] = search_result
    
    return state
