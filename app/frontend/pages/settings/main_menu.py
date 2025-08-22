# app/frontend/pages/settings/main_menu.py
# Menu principal de configuration

import streamlit as st

def show_main_menu():
    """Show main configuration menu"""
    st.markdown("""
        <div style='
            background: linear-gradient(90deg, #e0effd 0%, #fff5e8 100%);
            padding: 0rem 2rem;
            border-radius: 0rem;
            border-left: 5px solid #2994f2;
            border-right: 5px solid #fbbf5d;
            margin-bottom: 2rem;
            display: flex;
            justify-content: center;
            align-items: center;
        '>
            <h2 style='margin: 0; font-weight: bold;'>⚙️ Configuration du système</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Le secteur est automatiquement défini selon le profil utilisateur
    # Les superviseurs voient leur secteur, l'admin voit tout
    user_secteur = st.session_state.get("user_secteur")
    if user_secteur:
        st.session_state["selected_sector"] = user_secteur
    
    
    st.info("Sélectionnez la section de configuration que vous souhaitez gérer.", icon="ℹ️")
    
    # Créer une grille 2x2 pour les 4 sections de configuration
    col1, col2 = st.columns(2)
    
    with col1:
        # Gestion des utilisateurs
        with st.container(border=True):
            st.markdown("### 👤 Gestion des utilisateurs")
            st.markdown("Gérez les comptes utilisateurs, les rôles, les permissions et les disponibilités.")
            if st.button("Accéder à la gestion des utilisateurs", use_container_width=True, key="users_config_btn"):
                st.session_state["current_config_page"] = "users"
                st.rerun()
        
        # Configuration des postes
        with st.container(border=True):
            st.markdown("### 🎯 Configuration des postes")
            st.markdown("Configurez les postes de travail, leurs exigences et leurs contraintes.")
            if st.button("Accéder à la configuration des postes", use_container_width=True, key="positions_config_btn"):
                st.session_state["current_config_page"] = "positions"
                st.rerun()
    
    with col2:
        # Configuration des horaires
        with st.container(border=True):
            st.markdown("### 🕐 Configuration des horaires")
            st.markdown("Configurez les horaires de travail et les plannings du laboratoire.")
            if st.button("Accéder à la configuration des horaires", use_container_width=True, key="schedules_config_btn"):
                st.session_state["current_config_page"] = "schedules"
                st.rerun()
        
        # Paramètres globaux
        with st.container(border=True):
            st.markdown("### ⚙️ Paramètres globaux")
            st.markdown("Configurez les paramètres globaux du système et les règles générales.")
            if st.button("Accéder aux paramètres globaux", use_container_width=True, key="global_config_btn"):
                st.session_state["current_config_page"] = "global"
                st.rerun()
    
    # Divider and back button
    st.divider()
    
    # Bouton retour
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Accueil", use_container_width=True, key="home_btn"):
            st.session_state['selected_page'] = 'Accueil'
            st.rerun()
    
    # Ajouter de l'espace en bas de page
    from app.frontend.utils import add_bottom_spacing
    add_bottom_spacing()
