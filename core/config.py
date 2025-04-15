import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI

load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_KEY")

llm_gpt_4o = ChatOpenAI(
    model="openai/gpt-4o-2024-11-20",
    temperature=0.1,
    openai_api_key=OPEN_ROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    streaming=True
)

llm_deepseek_chat_v3_free = ChatOpenAI(
    # model="deepseek/deepseek-chat-v3-0324:free",
    model="openai/gpt-4o-2024-11-20",
    temperature=0.1,
    openai_api_key=OPEN_ROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    streaming=True
)

llm_gpt_4o_search_preview = ChatOpenAI(
    model="openai/gpt-4o-search-preview",
    temperature=0.1,
    openai_api_key=OPEN_ROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    streaming=True
)
