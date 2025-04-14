from typing import TypedDict, Literal, Optional
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    route: Optional[Literal["search", "chat"]]
    search_params: Optional[dict]
    confirmed_source: Optional[bool]
    result: Optional[str]
