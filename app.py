# app.py
import streamlit as st
from auth.login import logged_in, logged_out
from navigation import get_nav

if logged_in():
    nav = get_nav()
    
    if nav:
        here = st.navigation(nav, position="sidebar")
        if st.sidebar.button("Logout"):
            logged_out()
            st.rerun()
        here.run()
    else:
        st.warning("Nenhuma navegação disponível.")
