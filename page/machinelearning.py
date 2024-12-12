import streamlit as st
from auth.login import credencials, logged_in, logged_out
from sessions.state import sessions

if "logged_in" not in st.session_state:
    logged_out()
else:
    st.title("machinelearning page")
    st.write("Lorem Ipsum archtecture.")
    page_name = "machinelearning"
    sessions(page_name)