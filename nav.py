import streamlit as st

navapp = [
    st.Page("page/home.py", title="Home", icon=":material/mitre:"),
    st.Page("page/management.py", title="Management", icon=":material/mitre:"),
    st.Page("page/archtecture.py", title="Archtecture", icon=":material/mitre:"),
    st.Page("page/development.py", title="Development", icon=":material/mitre:"),
]