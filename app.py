import streamlit as st
from auth.login import credencials, logged_in, logged_out
from nav import navapp

# Application
if logged_in():
    # st.write(f'logged_in: :blue[{st.session_state["logged_in"]}]')
    here = st.navigation(navapp, position="sidebar")
    here.run()
    
    