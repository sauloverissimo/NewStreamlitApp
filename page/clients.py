import streamlit as st
from auth.login import credencials, logged_in, logged_out
from sessions.state import sessions

# Inicializando contadores globais e específicos da página
if "logged_in" not in st.session_state:
    logged_out()
else:
    st.title("Clients page")
    st.write("Lorem Ipsum development.")
    page_name = "clients"
    sessions(page_name)