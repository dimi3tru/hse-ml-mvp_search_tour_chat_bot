from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from core.config import llm_deepseek_chat_v3_free
from prompts.prompts import SYSTEM_CHAT_NODE_PROMPT
from models.agent_state import AgentState

# Промпт для общения
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_CHAT_NODE_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

chat_chain = chat_prompt | llm_deepseek_chat_v3_free | StrOutputParser()

# Основная функция узла
def chat_node(state: AgentState) -> AgentState:
    print("Заходим в chat_node")

    response = chat_chain.invoke({
        "input": state["input"],
        "chat_history": state["chat_history"]
    })

    state["result"] = response
    return state
