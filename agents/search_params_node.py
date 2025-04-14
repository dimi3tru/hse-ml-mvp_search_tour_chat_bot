from models.agent_state import AgentState

def check_search_params_node(state: AgentState) -> AgentState:
    print("Заходим в check_search_params_node")
    
    # # Простейшая эвристика — можно заменить на NER, RAG или модель извлечения
    # if any(word in state["input"].lower() for word in [
    #     "два", "на", "в", "до", "июнь", "день", "тысяч",
    #     "семья", "отель", "лететь", "период"
    # ]):
    #     state["search_params"] = {
    #         "направление": "введено пользователем",
    #         "дата": "предположительно найдена"
    #     }
    
    return state
