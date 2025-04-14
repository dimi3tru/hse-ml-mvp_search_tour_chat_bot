from models.agent_state import AgentState
from core.search_tool import search_tool

def confirm_source_node(state: AgentState) -> AgentState:
    print("Заходим в confirm_source_node")
    # Здесь можно добавить логику подтверждения, пока предполагаем согласие
    state["confirmed_source"] = True
    return state

def search_node(state: AgentState) -> AgentState:
    print("Заходим в search_node")
    state["result"] = search_tool(state["search_params"])
    return state
