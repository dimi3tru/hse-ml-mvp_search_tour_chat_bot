import streamlit as st

def show_chat_history(messages):
    for role, msg in messages:
        with st.chat_message(role):
            st.markdown(msg)

def show_results(results):
    if results:
        st.subheader("📋 Найденные туры")
        for tour in results:
            with st.container(border=True):
                st.markdown(f"### {tour['title']}")
                st.markdown(tour["description"])
                st.markdown(f"💰 **Цена:** {tour['price']}")
                st.link_button("Перейти к бронированию", tour["link"])

