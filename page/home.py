import streamlit as st
from auth.login import logged_out
from sessions.state import sessions

if "logged_in" not in st.session_state:
    logged_out()
else:
    st.title("Welcome to home page!")
    st.write("Lorem Ipsun")
    page_name = "home"
    sessions(page_name)