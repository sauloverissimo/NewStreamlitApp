# nav_debug.py
import streamlit as st
from auth.login import logged_out
from sessions.state import sessions
from navigation import get_nav

if "logged_in" not in st.session_state:
    logged_out()
else:
    st.title("Debug Page")
    st.write("Lorem Ipsum architecture.")
    page_name = "nav_debug"
    sessions(page_name)

    # Gera o nav dinâmico
    nav = get_nav()

    st.write("**Conteúdo de nav:**")
    st.write(nav)
