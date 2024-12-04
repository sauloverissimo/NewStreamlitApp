import streamlit as st
from db import get_connection
import bcrypt


def fetch_user_from_db(username):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT user_name, password, role, user_status FROM users WHERE user = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def verify_credentials(username, password):
    user = fetch_user_from_db(username)
    if user:
        db_username, db_password, role, status = user
        if bcrypt.checkpw(password.encode(), db_password.encode()) and status == 1:
            return True, role
    return False, None


# Login
def logged_in():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None

    if not st.session_state["logged_in"]:
        st.text_input(label="Usuário :", key="usuario", on_change=credencials)
        st.text_input(label="Senha :", key="senha", on_change=credencials, type="password")
        return False
    return True


def credencials():
    usuario = st.session_state.get("usuario", "").strip()
    senha = st.session_state.get("senha", "").strip()

    if not usuario:
        st.warning("Insira seu usuário.")
        st.session_state["logged_in"] = False
    elif not senha:
        st.warning("Insira sua senha.")
        st.session_state["logged_in"] = False
    else:
        is_valid, role = verify_credentials(usuario, senha)
        if is_valid:
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = role
            st.success("Login bem-sucedido!")
        else:
            st.error("Usuário ou senha inválidos.")
            st.session_state["logged_in"] = False


def logged_out():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.rerun()
