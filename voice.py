import streamlit as st
from ai_engine import get_ai_response

st.title("🤖 Pooja AI Test")

user_input = st.text_input("Ask something")

if user_input:
    response = get_ai_response(user_input)
    st.write("AI:", response)