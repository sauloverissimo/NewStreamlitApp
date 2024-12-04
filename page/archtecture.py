import streamlit as st
from auth.login import credencials, logged_in, logged_out
from sessions.state import sessions

if "logged_in" not in st.session_state:
    logged_out()
else:
    st.title("Archtecture page")
    st.write("Lorem Ipsum archtecture.")
    page_name = "archtecture"
    sessions(page_name)