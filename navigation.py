# navigation.py
import streamlit as st
from collections import defaultdict
from db import get_connection

def dynamic_nav(user_id):
    user_role_id = st.session_state.get("user_role_id")
    user_role = st.session_state.get("user_role")

    if not user_role_id or not user_role:
        st.warning("user_role não definida na sessão.")
        return {}, {}, {}, {}

    con = get_connection()
    cur = con.cursor()

    query = """
        SELECT p.page_id, 
               p.page_description, 
               p.url_path, 
               p.page_status, 
               p.icon, 
               p.param_default, 
               p.title, 
               p.page_hierarchy
        FROM pages p
        JOIN navigation n ON n.page_id = p.page_id
        WHERE n.role_id = ?
          AND p.page_status = 1
        ORDER BY p.page_hierarchy, p.title
    """
    pages_data = cur.execute(query, (user_role_id,)).fetchall()
    con.close()

    page_objects = {}
    pages_metadata = {}
    hierarchy_dict = defaultdict(list)
    page_id_by_obj = {}

    for row in pages_data:
        page_id, page_description, url_path, page_status, icon, param_default, title, page_hierarchy = row

        # Cria objeto st.Page
        page_obj = st.Page(url_path, title=title, icon=icon)

        page_objects[page_id] = page_obj
        pages_metadata[page_id] = {
            "url_path": url_path,
            "title": title,
            "icon": icon
        }
        page_id_by_obj[page_obj] = page_id

        hierarchy_key = page_hierarchy.lstrip('/')
        hierarchy_dict[hierarchy_key].append(page_obj)

    navapp = dict(hierarchy_dict)

    # Cria navinfo com base em pages_metadata
    navinfo = {}
    for hierarchy, plist in navapp.items():
        navinfo[hierarchy] = []
        for p in plist:
            pid = page_id_by_obj[p]
            meta = pages_metadata[pid]
            navinfo[hierarchy].append({
                "url_path": meta["url_path"],
                "title": meta["title"],
                "icon": meta["icon"]
            })

    return page_objects, pages_metadata, navapp, navinfo

def generate_navapp(navinfo):
    """
    Gera um dicionário com listas de objetos st.Page no formato correto.
    """
    navapp = defaultdict(list)

    for hierarchy, pages in navinfo.items():
        for page_data in pages:
            url_path = page_data["url_path"]
            title = page_data["title"]
            icon = page_data["icon"]

            # Cria um objeto st.Page com os parâmetros fornecidos
            page_obj = st.Page(url_path, title=title, icon=icon)
            navapp[hierarchy].append(page_obj)

    return dict(navapp)

# Função para gerar nav dinâmico
def get_nav():
    user_id = st.session_state.get("user_id")
    if not user_id:
        return {}

    _, _, _, navinfo = dynamic_nav(user_id)
    return generate_navapp(navinfo)