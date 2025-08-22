# app/frontend/pages/settings/schedules/__init__.py
# Module de gestion des horaires

import streamlit as st

def schedules_router():
    """Router pour la gestion des horaires"""
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
            <h2 style='margin: 0; font-weight: bold;'>🕐 Configuration des horaires</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("Configurez les horaires de travail et les plannings du laboratoire.", icon="ℹ️")
    
    # Contenu temporaire
    st.markdown("### 🚧 **Fonctionnalité en cours de développement**")
    st.info("La configuration des horaires sera bientôt disponible dans cette section.", icon="ℹ️")
    
    # Bouton retour
    st.divider()
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Back", key="back_to_main_config", use_container_width=True):
            st.session_state["current_config_page"] = None
            st.rerun()
    
    # Ajouter de l'espace en bas de page
    from app.frontend.utils import add_bottom_spacing
    add_bottom_spacing()
