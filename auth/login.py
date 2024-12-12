import streamlit as st
from db import get_connection
import bcrypt


def fetch_user_from_db(username):
    """
    Busca o usuário no banco de dados pelo nome de usuário.
    Agora retorna também o user_id e o role_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT user_id, user_name, password, role, user_status, role_id FROM users WHERE user = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def verify_credentials(username, password):
    """
    Verifica as credenciais e retorna o status, user_id, role e role_id.
    """
    user = fetch_user_from_db(username)
    if user:
        user_id, db_username, db_password, role, status, role_id = user
        if bcrypt.checkpw(password.encode(), db_password.encode()) and status == 1:
            return True, user_id, role, role_id
    return False, None, None, None


# Login
def logged_in():
    """
    Gerencia o estado de login.
    """
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state["user_role"] = None
        st.session_state["user_role_id"] = None

    if not st.session_state["logged_in"]:
        st.text_input(label="Usuário :", key="usuario", on_change=credencials)
        st.text_input(label="Senha :", key="senha", on_change=credencials, type="password")
        return False
    return True


def credencials():
    """
    Processa o login e atualiza os estados de sessão.
    """
    usuario = st.session_state.get("usuario", "").strip()
    senha = st.session_state.get("senha", "").strip()

    if not usuario:
        st.warning("Insira seu usuário.")
        st.session_state["logged_in"] = False
    elif not senha:
        st.warning("Insira sua senha.")
        st.session_state["logged_in"] = False
    else:
        is_valid, user_id, role, role_id = verify_credentials(usuario, senha)
        if is_valid:
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user_id
            st.session_state["user_role"] = role
            st.session_state["user_role_id"] = role_id
            st.success("Login bem-sucedido!")
        else:
            st.error("Usuário ou senha inválidos.")
            st.session_state["logged_in"] = False


def logged_out():
    """
    Gerencia o logout do usuário e redefine os estados de sessão.
    """
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_role = None
    st.session_state.user_role_id = None
