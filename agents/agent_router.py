from graph.langgraph_graph import graph
from core.memory import memory

def agent_router(user_input: str, callback=None):
    """
    Маршрутизатор агента, который обрабатывает ввод пользователя и возвращает ответ.
    
    Args:
        user_input: Строка запроса пользователя
        callback: Опциональная функция обратного вызова для отслеживания узлов графа.
                 Принимает имя узла (строку) и вызывается при активации каждого узла.
    
    Returns:
        Строка ответа от агента
    """
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

    # Если предоставлен callback, создаем функцию-обертку для отслеживания узлов
    if callback:
        # Определяем функцию для отслеживания узлов
        def node_tracker(state, node):
            print(f"ОТЛАДКА: node_tracker: {node}")
            # Вызываем callback с именем узла
            callback(node)
            # Возвращаем исходное состояние
            return state
            
        # Запускаем граф с функцией отслеживания
        final_state = graph.invoke(state, {"on_node_start": node_tracker})
    else:
        # Запускаем граф без отслеживания
        final_state = graph.invoke(state)

    print("got final_state and starting to get response")
    response = final_state["result"]
    memory.chat_memory.add_ai_message(response)

    return response


def agent_router_streaming(user_input: str):
    memory.chat_memory.add_user_message(user_input)

    state = {
        "input": user_input,
        "chat_history": memory.chat_memory.messages,
        "route": None,
        "search_params": None,
        "confirmed_source": None,
        "result": None
    }

    # Стримим с режимом updates
    stream = graph.stream(state, stream_mode="updates")

    last_node_state = None

    for update in stream:
        # print(f">> STREAM UPDATE: {update}")
        last_node_state = update  # сохраняем последнее обновление
        yield update  # передаём наружу для UI

    # Достаём имя последнего узла
    if last_node_state:
        # Получаем имя последнего обработанного узла (ключ словаря)
        node_name = list(last_node_state.keys())[0]
        node_output = last_node_state[node_name]

        # Пытаемся достать результат из output состояния
        final_result = node_output.get("result", "[Нет результата]")
        memory.chat_memory.add_ai_message(final_result)

        return final_result
    else:
        return "[Ошибка: не удалось получить финальное состояние]"
