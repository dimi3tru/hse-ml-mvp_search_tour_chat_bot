import streamlit as st
from core.memory import memory
from components.ui import show_chat_history, show_results
from agents.agent_router import agent_router

st.set_page_config(page_title="ИИ-агент по поиску туров", layout="centered")
st.title("Поисковый ИИ-агент для путешествий по России")

# --- Session ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "results" not in st.session_state:
    st.session_state.results = []

# --- Очистка памяти ---
if st.button("🔄 Новый диалог"):
    st.session_state.messages = []
    st.session_state.results = []
    memory.clear()


# --- Ввод пользователя ---
user_input = st.chat_input("Напишите, куда хотите поехать или что вас интересует?")

if user_input:
    st.session_state.messages.append(("user", user_input))

    with st.spinner("Ассистент обрабатывает ваш запрос..."):
        try:
            response = agent_router(user_input)
        except Exception as e:
            response = f"Ошибка: {str(e)}"

    st.session_state.messages.append(("assistant", response))

# --- UI ---
show_chat_history(st.session_state.messages)
show_results(st.session_state.results)
