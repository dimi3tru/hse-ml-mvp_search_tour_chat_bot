from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from core.config import llm_deepseek_chat_v3_free
from models.agent_state import AgentState
from prompts.prompts import SYSTEM_ROUTER_PROMPT


router_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_ROUTER_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

router_chain = router_prompt | llm_deepseek_chat_v3_free | StrOutputParser()

def route_decision(value: dict) -> str:
    print("Заходим в route_decision")
    try:
        # Выполнение запроса к LLM
        response = router_chain.invoke(value).strip().lower()
        # Проверка, что возвращается одно из двух значений
        if response not in ["search", "chat"]:
            raise ValueError(f"Неожиданный ответ от LLM: {response}")
        return response
    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        # В случае ошибки, возвращаем дефолтное сообщение
        return "Возникли временные неполадки с обработкой запроса. Повторите его, пожалуйста."

def router_node(state: AgentState) -> AgentState:
    print("Заходим в router_node")
    state["route"] = route_decision({
        "input": state["input"],
        "chat_history": state["chat_history"]
    })
    
    # Печатаем состояние для отладки
    print(f"Значения в route: {state['route']}")
    
    # Если результат не chat и не search, вернем дефолтное сообщение
    if state["route"] not in ["search", "chat"]:
        state["route"] = "Возникли временные неполадки с обработкой запроса. Повторите его, пожалуйста."
    
    return state
