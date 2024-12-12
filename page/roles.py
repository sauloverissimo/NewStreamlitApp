import streamlit as st
from auth.login import logged_out, logged_out
from sessions.state import sessions
from db import get_connection
import pandas as pd
import bcrypt
import time

# Verifica se o User está logado
if "logged_in" not in st.session_state:
    st.write("User not logged in.")
    logged_out()

else:
    page_name = "roles"
    st.title("Roles Navigation Admin")
    sessions(page_name)
    
    def fetch_table_data(query, params=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        data = cursor.fetchall()
        conn.close()
        return data

    def update_table(query, params):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    tabs = st.tabs(["Users", "Roles", "Pages", "Navigation"])
    # Funções para manipular tabelas
    with tabs[0]:
        #st.header("Users")

        # Estado para controle de edição e exclusão
        if "delete_user_id" not in st.session_state:
            st.session_state["delete_user_id"] = None
        if "edit_user_id" not in st.session_state:
            st.session_state["edit_user_id"] = None

        # Exibir Users existentes
        users = fetch_table_data("SELECT user_id, user, user_name, user_email, user_status, role FROM users")
        df_users = pd.DataFrame(users, columns=["ID", "User", "Name", "Email", "Status", "Role"])

        # Tabela com botões de edição e exclusão
        # st.write("### Existing Users")
        for index, row in df_users.iterrows():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 3, 3, 1, 1, 1])
            with col1:
                st.text(row["ID"])
            with col2:
                st.text(row["User"])
            with col3:
                st.text(row["Name"])
            with col4:
                st.text(row["Email"])
            with col5:
                st.text("Active" if row["Status"] == 1 else "Inactive")
            with col6:
                if st.button("⚙️", key=f"edit_{row['ID']}_{index}"):  # Corrigido com sufixo exclusivo
                    st.session_state["edit_user_id"] = row["ID"]
            with col7:
                if st.button("🗑️", key=f"delete_{row['ID']}_{index}"):  # Corrigido com sufixo exclusivo
                    st.session_state["delete_user_id"] = row["ID"]

        # Modal de confirmação para deletar
        if st.session_state["delete_user_id"] is not None:
            user_id = st.session_state["delete_user_id"]
            st.warning(f"Are you sure you want to delete User ID: {user_id}?")
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("Yes, Delete"):
                    try:
                        update_table("DELETE FROM users WHERE user_id = ?", (user_id,))
                        st.success(f"User ID {user_id} deleted successfully!")
                        st.session_state["delete_user_id"] = None
                        time.sleep(0.3)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting user: {e}")
            with col_cancel:
                if st.button("Cancel"):
                    st.session_state["delete_user_id"] = None

        # Se estivermos editando um user existente, preencher os campos
        st.subheader("Insert/Edit User")

        # Botão "New User"
        if st.button("➕ Add New User", key="add_new_user", help="Click to add a new user"):
            st.session_state["edit_user_id"] = None  # Reseta estado de edição

        # Determinar se estamos editando ou adicionando um usuário
        if st.session_state["edit_user_id"] is not None:
            edit_user_id = st.session_state["edit_user_id"]
            user_data = fetch_table_data(
                "SELECT user, user_name, user_email, user_status, role, password FROM users WHERE user_id = ?", (edit_user_id,)
            )
            if user_data:
                user, user_name, user_email, user_status, role, current_password = user_data[0]
            else:
                st.error("User not found!")
                user, user_name, user_email, user_status, role, current_password = "", "", "", 1, "", ""
        else:
            edit_user_id = None
            user, user_name, user_email, user_status, role, current_password = "", "", "", 1, "", ""

        # Formulário para adicionar/editar Users
        with st.form("user_form", clear_on_submit=True):
            user = st.text_input("User", value=user)
            user_name = st.text_input("Name", value=user_name)
            user_email = st.text_input("E-mail", value=user_email)
            password = st.text_input("Password (Leave blank to keep the current. Deixe em branco para manter a atual.)", type="password")
            user_status = st.selectbox("Status", [1, 0], index=(0 if user_status == 1 else 1), format_func=lambda x: "Active" if x == 1 else "Inactive")
            
            # Obter roles disponíveis para selecionar
            roles = fetch_table_data("SELECT role, role_id FROM roles")
            role_dict = {role: role_id for role, role_id in roles}
            role_options = list(role_dict.keys())

            # Verifica se o role existe na lista; caso contrário, usa o primeiro valor como padrão
            if role not in role_options:
                role = role_options[0] if role_options else ""

            role = st.selectbox("Role", options=role_options, index=role_options.index(role) if role in role_options else 0)

            submitted = st.form_submit_button("Save")

            if submitted:
                if not user or not user_name or not user_email:
                    st.error("All fields (User, Name, Email) are required!")
                else:
                    try:
                        # Se o campo senha estiver vazio, mantém a senha atual
                        if password.strip() == "":
                            final_password = current_password
                        else:
                            # Gera o hash da senha para salvar no banco de dados
                            final_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                        
                        role_id = role_dict.get(role)
                        
                        if edit_user_id:  # Se for edição
                            update_table(
                                """
                                UPDATE users 
                                SET user = ?, 
                                    user_name = ?, 
                                    user_email = ?, 
                                    password = ?, 
                                    user_status = ?, 
                                    role = ?, 
                                    role_id = ?
                                WHERE user_id = ?
                                """,
                                (user, user_name, user_email, final_password, user_status, role, role_id, edit_user_id)
                            )
                            st.success(f"User {user_name} updated successfully!")
                        else:  # Se for novo registro
                            update_table(
                                """
                                INSERT INTO users (user, user_name, user_email, password, user_status, role, role_id) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                """,
                                (user, user_name, user_email, final_password, user_status, role, role_id)
                            )
                            st.success(f"User {user_name} added successfully!")

                        # Resetar o estado de edição
                        st.session_state["edit_user_id"] = None
                        time.sleep(0.3)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Save Error: {e}")



    # Aba Roles
    with tabs[1]:
        st.header("Roles")

        # Estado para controle de edição e exclusão
        if "delete_role_id" not in st.session_state:
            st.session_state["delete_role_id"] = None
        if "edit_role_id" not in st.session_state:
            st.session_state["edit_role_id"] = None

        # Exibir Roles existentes
        roles = fetch_table_data("SELECT role_id, role, role_description FROM roles")
        df_roles = pd.DataFrame(roles, columns=["ID", "Role", "Description"])

        # Tabela com botões de edição e exclusão
        st.write("### Existing Roles")
        for index, row in df_roles.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 3, 4, 1, 1])
            with col1:
                st.text(row["ID"])
            with col2:
                st.text(row["Role"])
            with col3:
                st.text(row["Description"])
            with col4:
                if st.button("⚙️", key=f"edit_{row['ID']}"):
                    st.session_state["edit_role_id"] = row["ID"]
            with col5:
                if st.button("🗑️", key=f"delete_{row['ID']}"):
                    st.session_state["delete_role_id"] = row["ID"]

        # Modal de confirmação para deletar
        if st.session_state["delete_role_id"] is not None:
            role_id = st.session_state["delete_role_id"]
            st.warning(f"Are you sure you want to delete Role ID: {role_id}?")
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("Yes, Delete"):
                    try:
                        update_table("DELETE FROM roles WHERE role_id = ?", (role_id,))
                        st.success(f"Role {role_id} deleted successfully!")
                        st.session_state["delete_role_id"] = None
                        time.sleep(0.3)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting role: {e}")
            with col_cancel:
                if st.button("Cancel"):
                    st.session_state["delete_role_id"] = None

        # Formulário para editar ou adicionar Roles
        st.subheader("Insert/Edit Role")

        # Botão "Add New Role"
        st.markdown(
            """
            <style>
            .new-role-btn {
                display: block;
                margin: 10px auto 20px auto;
                padding: 10px 20px;
                font-size: 16px;
                text-align: center;
                background-color: #6200ea;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .new-role-btn:hover {
                background-color: #3700b3;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        if st.button("⭐ Add New Role", key="add_new_role", help="Click to add a new role"):
            st.session_state["edit_role_id"] = None  # Reseta estado de edição

        # Se estivermos editando uma role existente, preencher os campos
        if st.session_state["edit_role_id"] is not None:
            edit_role_id = st.session_state["edit_role_id"]
            role_data = fetch_table_data("SELECT role, role_description FROM roles WHERE role_id = ?", (edit_role_id,))
            if role_data:
                role_name, role_description = role_data[0]
            else:
                st.error("Role not found!")
                role_name, role_description = "", ""
        else:
            edit_role_id = None
            role_name, role_description = "", ""

        with st.form("role_form", clear_on_submit=True):
            role_name = st.text_input("Role Name", value=role_name)
            role_description = st.text_area("Description", value=role_description)

            submitted = st.form_submit_button("Save")

            if submitted:
                try:
                    if edit_role_id:  # Se for edição
                        update_table(
                            """
                            UPDATE roles 
                            SET role = ?, 
                                role_description = ?
                            WHERE role_id = ?
                            """,
                            (role_name, role_description, edit_role_id)
                        )
                        st.success(f"Role {role_name} updated successfully!")
                    else:  # Se for novo registro
                        update_table(
                            """
                            INSERT INTO roles (role, role_description) 
                            VALUES (?, ?)
                            """,
                            (role_name, role_description)
                        )
                        st.success(f"Role {role_name} added successfully!")

                    # Resetar o estado de edição
                    st.session_state["edit_role_id"] = None
                    time.sleep(0.3)
                    st.rerun()
                except Exception as e:
                    st.error(f"Save Error: {e}")


    with tabs[2]:
        st.header("Pages")

        # Estado para controle de edição e exclusão
        if "delete_page_id" not in st.session_state:
            st.session_state["delete_page_id"] = None
        if "edit_page_id" not in st.session_state:
            st.session_state["edit_page_id"] = None

        # Exibir Pages existentes
        pages = fetch_table_data(
            "SELECT page_id, title, page_description, url_path, page_status, icon, param_default, page_hierarchy FROM pages"
        )
        df_pages = pd.DataFrame(
            pages,
            columns=["ID", "Title", "Description", "URL Path", "Status", "Icon", "Default", "Hierarchy"]
        )

        # Tabela com botões de edição e exclusão
        st.write("### Existing Pages")
        for index, row in df_pages.iterrows():
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([0.5, 1.5, 3, 3, 0.8, 0.5, 0.5, 0.7, 0.7])
            with col1:
                st.text(row["ID"])
            with col2:
                st.text(row["Title"])
            with col3:
                st.text(row["Hierarchy"])
            with col4:
                st.text(row["URL Path"])
            with col5:
                st.text("Active" if row["Status"] == 1 else "Inactive")
            with col6:
                st.text(row["Icon"])
            with col7:
                st.text("Yes" if row["Default"] == 1 else "No")
            with col8:
                if st.button("⚙️", key=f"edit_pages_{row['ID']}_{index}"):  # Chave com prefixo único
                    st.session_state["edit_page_id"] = row["ID"]
            with col9:
                if st.button("🗑️", key=f"delete_pages_{row['ID']}_{index}"):  # Chave com prefixo único
                    st.session_state["delete_page_id"] = row["ID"]

        # Modal de confirmação para deletar
        if st.session_state["delete_page_id"] is not None:
            page_id = st.session_state["delete_page_id"]
            st.warning(f"Are you sure you want to delete Page ID: {page_id}?")
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("Yes, Delete"):
                    try:
                        update_table("DELETE FROM pages WHERE page_id = ?", (page_id,))
                        st.success(f"Page ID {page_id} deleted successfully!")
                        st.session_state["delete_page_id"] = None
                        time.sleep(0.3)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting page: {e}")
            with col_cancel:
                if st.button("Cancel"):
                    st.session_state["delete_page_id"] = None

        # Formulário para adicionar/editar Pages
        st.subheader("Insert/Edit Page")

        # Botão "Add New Page"
        if st.button("➕ Add New Page", key="add_new_page", help="Click to add a new page"):
            st.session_state["edit_page_id"] = None  # Reseta estado de edição

        # Preencher formulário de edição, se necessário
        if st.session_state["edit_page_id"] is not None:
            edit_page_id = st.session_state["edit_page_id"]
            page_data = fetch_table_data(
                """
                SELECT title, page_description, url_path, page_status, icon, param_default, page_hierarchy 
                FROM pages WHERE page_id = ?
                """,
                (edit_page_id,)
            )
            if page_data:
                (
                    title,
                    page_description,
                    url_path,
                    page_status,
                    icon,
                    param_default,
                    page_hierarchy,
                ) = page_data[0]
            else:
                st.error("Page not found!")
                title, page_description, url_path, page_status, icon, param_default, page_hierarchy = "", "", "", 1, "", 0, ""
        else:
            edit_page_id = None
            title, page_description, url_path, page_status, icon, param_default, page_hierarchy = "", "", "", 1, "", 0, ""

        # Formulário
        with st.form("page_form", clear_on_submit=True):
            title = st.text_input("Title", value=title)
            page_description = st.text_area("Description", value=page_description)
            url_path = st.text_input("URL Path", value=url_path)
            page_status = st.selectbox(
                "Status", [1, 0], index=(0 if page_status == 1 else 1), format_func=lambda x: "Active" if x == 1 else "Inactive"
            )
            icon = st.text_input("Icon", value=icon)
            param_default = st.selectbox(
                "Default Page", [1, 0], index=(0 if param_default == 1 else 1), format_func=lambda x: "Yes" if x == 1 else "No"
            )
            page_hierarchy = st.text_input("Page Hierarchy", value=page_hierarchy)

            submitted = st.form_submit_button("Save")

            if submitted:
                if not title or not url_path:
                    st.error("Both 'Title' and 'URL Path' are required!")
                else:
                    try:
                        if edit_page_id:  # Se for edição
                            update_table(
                                """
                                UPDATE pages 
                                SET title = ?, 
                                    page_description = ?, 
                                    url_path = ?, 
                                    page_status = ?, 
                                    icon = ?, 
                                    param_default = ?, 
                                    page_hierarchy = ?
                                WHERE page_id = ?
                                """,
                                (title, page_description, url_path, page_status, icon, param_default, page_hierarchy, edit_page_id)
                            )
                            st.success(f"Page {title} updated successfully!")
                        else:  # Se for novo registro
                            update_table(
                                """
                                INSERT INTO pages (title, page_description, url_path, page_status, icon, param_default, page_hierarchy) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                """,
                                (title, page_description, url_path, page_status, icon, param_default, page_hierarchy)
                            )
                            st.success(f"Page {title} added successfully!")

                        # Resetar o estado de edição
                        st.session_state["edit_page_id"] = None
                        time.sleep(0.3)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Save Error: {e}")




    # Aba Navigation
    with tabs[3]:
        st.header("Navigation")

        # Obter as Roles do banco de dados
        roles = fetch_table_data("SELECT role_id, role FROM roles")
        role_dict = {role: role_id for role_id, role in roles}  # Mapeia role -> role_id
        role_names = list(role_dict.keys())

        # Iterar sobre as Roles dentro de expanders
        for role_name in role_names:
            role_id = role_dict[role_name]
            with st.expander(f"Role: {role_name}", expanded=False):
                # Obter todas as páginas
                pages = fetch_table_data("SELECT page_id, title FROM pages")
                page_dict = {title: page_id for page_id, title in pages}  # Mapeia page -> page_id
                page_names = list(page_dict.keys())

                # Obter as páginas já vinculadas à role atual
                linked_pages = fetch_table_data(
                    "SELECT page_id FROM navigation WHERE role_id = ?", (role_id,)
                )
                linked_page_ids = {row[0] for row in linked_pages}  # Conjunto de IDs de páginas vinculadas
                linked_page_names = [title for title, page_id in page_dict.items() if page_id in linked_page_ids]

                # Multiselect para selecionar/desmarcar páginas
                selected_pages = st.multiselect(
                    "Select Pages:",
                    options=page_names,
                    default=linked_page_names,
                    help="Select the pages you want to associate with this role.",
                    key=f"multiselect_role_{role_id}"  # Adicionando uma chave única
                )

                # Botão para salvar alterações
                if st.button(f"Save Changes for {role_name}", key=f"save_changes_role_{role_id}"):
                    try:
                        # Converter os títulos selecionados para IDs
                        selected_page_ids = {page_dict[page] for page in selected_pages}

                        # Criar ou atualizar relações
                        for page_name, page_id in page_dict.items():
                            if page_id in selected_page_ids and page_id not in linked_page_ids:
                                # Adicionar nova relação
                                update_table(
                                    "INSERT INTO navigation (page_id, role_id) VALUES (?, ?)",
                                    (page_id, role_id)
                                )
                            elif page_id not in selected_page_ids and page_id in linked_page_ids:
                                # Remover relação existente
                                update_table(
                                    "DELETE FROM navigation WHERE page_id = ? AND role_id = ?",
                                    (page_id, role_id)
                                )

                        st.success(f"Navigation for {role_name} updated successfully!")
                        time.sleep(0.3)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating navigation for {role_name}: {e}")
