import streamlit as st
from auth.login import logged_in, logged_out

def sessions(page_name):

    if not st.checkbox(":green[Hide Sessions]"):
        st.write(f'logged_in: :blue[{st.session_state["logged_in"]}]')

        if "counter_global" not in st.session_state:
            st.session_state["counter_global"] = 0

        page_key = f"counter_{page_name}"
        if page_key not in st.session_state:
            st.session_state[page_key] = 0

        if st.button("Update Global Session"):
            st.session_state["counter_global"] += 1

        if st.button(f"Update {page_name} Session"):
            st.session_state[page_key] += 1

        if st.button("Logout"):
            logged_out()
            st.rerun()

        st.write("Global:", st.session_state["counter_global"])
        st.write(f"Local {page_name}:", st.session_state[page_key])
        st.write("All States:", st.session_state)
