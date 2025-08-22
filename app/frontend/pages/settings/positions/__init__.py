# app/frontend/pages/settings/positions/__init__.py
# Module de gestion des postes avec base SQLite centralisée

import streamlit as st
from .list import show_positions_list
from .new import show_new_position_form
from .edit import show_position_detail_config

def positions_router():
    """Routeur pour la gestion des postes"""
    
    # Récupérer la page actuelle depuis la session
    current_page = st.session_state.get("current_config_page", None)
    
    # Navigation entre les pages
    if current_page == "new_position":
        show_new_position_form()
    elif current_page == "position_detail":
        show_position_detail_config()
    else:
        # Page par défaut : liste des postes
        show_positions_list()
