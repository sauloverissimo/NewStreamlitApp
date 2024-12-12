import streamlit as st
from auth.login import credencials, logged_in, logged_out
from sessions.state import sessions

if "logged_in" not in st.session_state:
    logged_out()
else:
    page_name = "admin"
    st.title("admin Area")
    sessions(page_name)