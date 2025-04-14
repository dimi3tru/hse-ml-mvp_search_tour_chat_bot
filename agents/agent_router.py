from graph.langgraph_graph import graph
from core.memory import memory

def agent_router(user_input: str):
    print("Заходим в agent_router")
    
    memory.chat_memory.add_user_message(user_input)

    print("Заходим в graph.invoke")
    state = {
        "input": user_input,
        "chat_history": memory.chat_memory.messages,
        "route": None,
        "search_params": None,
        "confirmed_source": None,
        "result": None
    }

    final_state = graph.invoke(state)

    print("got final_state and starting to get response")
    response = final_state["result"]
    memory.chat_memory.add_ai_message(response)

    return response
