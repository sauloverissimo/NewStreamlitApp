import streamlit as st
from auth.login import logged_out, logged_in

# Application
if st.button("logout"):
    logged_out()
    