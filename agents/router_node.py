from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from tools.config import gpt_4o
from models.agent_state import AgentState
from prompts.node_prompts import SYSTEM_ROUTER_PROMPT


router_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_ROUTER_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

router_chain = router_prompt | gpt_4o | StrOutputParser()

def extract_command(response: str) -> str:
    """
    Извлекает команду 'search' или 'chat' из ответа LLM, даже если ответ содержит дополнительный текст.
    Всегда возвращает одну из двух команд, используя "chat" как безопасное значение по умолчанию.
    
    Args:
        response: Строка ответа от LLM
        
    Returns:
        "search" или "chat"
    """
    response = response.strip().lower()
    
    # Если ответ содержит только "search" или "chat", возвращаем его
    if response in ["search", "chat"]:
        return response
    
    # Проверяем, начинается ли ответ с "search" или "chat"
    if response.strip().startswith("chat"):
        return "chat"
    if response.strip().startswith("search"):
        return "search"
    
    # Если не удалось определить команду, возвращаем "chat" как безопасное значение
    print(f"Не удалось определить команду из ответа: '{response}'. Возвращаем 'chat' как безопасное значение.")
    return "chat"

def route_decision(value: dict) -> str:
    print("Заходим в route_decision")
    try:
        # Выполнение запроса к LLM
        response = router_chain.invoke(value)
        
        # Извлекаем команду из ответа (всегда будет "search" или "chat")
        command = extract_command(response)
        print(f"Извлечена команда: {command}")
        return command
            
    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        # В случае ошибки, возвращаем chat как безопасное значение
        return "chat"

def router_node(state: AgentState) -> AgentState:
    print("Заходим в router_node")
    
    # route_decision всегда вернет либо "search", либо "chat"
    state["route"] = route_decision({
        "input": state["input"],
        "chat_history": state["chat_history"]
    })
    
    # Печатаем состояние для отладки
    print(f"Значения в router_node: {state['route']}")
    
    return state
