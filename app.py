import streamlit as st
from tools.memory import memory
from components.ui import show_results
from agents.agent_router import agent_router, agent_router_streaming
import time

# Настройка страницы
st.set_page_config(page_title="ИИ-агент по поиску туров", layout="centered")
st.title("Поисковый ИИ-агент для путешествий по России")

# --- Session ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "results" not in st.session_state:
    st.session_state.results = []
if "tool_logs" not in st.session_state:
    st.session_state.tool_logs = []

# --- Очистка памяти ---
if st.button("Новый диалог"):
    st.session_state.messages = []
    st.session_state.results = []
    st.session_state.tool_logs = []
    memory.clear()

# --- UI чата ---
chat_container = st.container()
with chat_container:
    for role, content in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(content)

# --- Ввод пользователя ---
user_input = st.chat_input("Напишите, куда хотите поехать или что вас интересует?")

if user_input:
    st.session_state.messages.append(("user", user_input))
    st.session_state.tool_logs = []
    st.rerun()

# --- Описание этапов графа ---
TOOL_DESCRIPTIONS = {
    "router": "[agent 'router']: Маршрутизирую ваш запрос...",
    "chat": "[agent 'chat']: Формирую текстовый ответ...",
    "check_search_params": "[agent 'check_search_params']: Проверяю достаточность параметров для поиска...",
    "search": "[agent 'search']: Осуществляю поиск туров...",
    "default": "[agent 'default']: Обрабатываю ваш запрос..."
}

def log_tool_status(tool_name):
    desc = TOOL_DESCRIPTIONS.get(tool_name, TOOL_DESCRIPTIONS["default"])
    st.session_state.tool_logs.append((tool_name, desc))
    return desc

# --- Основная логика стриминга ---
if st.session_state.messages and st.session_state.messages[-1][0] == "user":
    last_user_input = st.session_state.messages[-1][1]
    st.session_state.messages.append(("assistant", ""))  # Заготовка под ответ

    # Размещаем пустое сообщение ассистента
    msg_placeholder = st.empty()
    status_placeholder = st.empty()

    full_response = ""

    try:
        for update in agent_router_streaming(last_user_input):
            # print(f">> UI STREAM UPDATE: {update}")

            # 🔍 Отображение ноды
            node_name = list(update.keys())[0]  # извлекаем имя узла
            print(f">> node_name: {node_name}")
            status = log_tool_status(node_name)
            status_placeholder.markdown(status)

            # ⏱️ даем UI обновиться
            time.sleep(0.5)

            # 📦 Если есть результат — показываем
            output = update.get(node_name, {})
            if "result" in output and output["result"]:
                full_response = output["result"]
                msg_placeholder.chat_message("assistant").markdown(full_response)

    except Exception as e:
        full_response = f"Ошибка: {str(e)}"
        msg_placeholder.chat_message("assistant").markdown(full_response)

    # Обновляем последнее сообщение в истории
    st.session_state.messages[-1] = ("assistant", full_response)
    st.rerun()


# --- Результаты поиска ---
show_results(st.session_state.results)
