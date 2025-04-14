from langgraph.graph import StateGraph, END

from models.agent_state import AgentState
from agents.chat_node import chat_node
from agents.router_node import router_node
from agents.search_params_node import check_search_params_node
from agents.search_node import confirm_source_node, search_node


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("router", router_node)
    builder.add_node("chat", chat_node)
    builder.add_node("check_search_params", check_search_params_node)
    builder.add_node("confirm_source", confirm_source_node)
    builder.add_node("search", search_node)

    builder.set_entry_point("router")

    builder.add_conditional_edges(
        "router", 
        lambda s: s["route"], {
            "chat": "chat",
            "search": "check_search_params"
        }
    )

    builder.add_conditional_edges(
        "check_search_params", 
        lambda s: "confirm_source" if s["search_params"] else "chat", {
            "confirm_source": "confirm_source",
            "chat": "chat"
        }
    )

    builder.add_conditional_edges(
        "confirm_source", 
        lambda s: "search" if s["confirmed_source"] else "chat", {
            "search": "search",
            "chat": "chat"
        }
    )

    builder.add_edge("chat", END)
    builder.add_edge("search", END)

    return builder.compile()
