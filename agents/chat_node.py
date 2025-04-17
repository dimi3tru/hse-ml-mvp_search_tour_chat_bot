from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from tools.config import gpt_4o
from prompts.node_prompts import SYSTEM_CHAT_NODE_PROMPT
from models.agent_state import AgentState

# Промпт для общения
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_CHAT_NODE_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

chat_chain = chat_prompt | gpt_4o | StrOutputParser()

# Основная функция узла
def chat_node(state: AgentState) -> AgentState:
    print("Заходим в chat_node")
    
    # Получаем строку с уже предоставленными параметрами, если они есть
    provided_params = "пока нет предоставленных параметров"
    if state.get("search_params") and state["search_params"].get("provided_params_str"):
        provided_params = state["search_params"]["provided_params_str"]
        print(f">> current provided_params: {provided_params}")
    
    # Добавляем информацию о сбросе параметров, если был выполнен сброс
    was_reset = False
    if state.get("search_params") and state["search_params"].get("was_reset"):
        was_reset = True
        state["search_params"]["was_reset"] = False  # Сбрасываем флаг для следующих вызовов
        provided_params = "все параметры были сброшены, давайте начнем заново"
    
    # Используем обновленный промпт в цепочке
    response = chat_chain.invoke({
        "input": state["input"],
        "chat_history": state["chat_history"],
        "provided_params": provided_params
    })

    # Если был сброс параметров, добавляем информацию к ответу
    if was_reset:
        response = "Все ранее указанные параметры для поиска были сброшены. " + response

    state["result"] = response
    return state
