# app/frontend/pages/settings/__init__.py
# Package principal pour la configuration du système

import streamlit as st

def run():
    """Main configuration page - Point d'entrée principal"""
    # Imports locaux pour éviter les imports circulaires
    from .main_menu import show_main_menu
    from .positions import positions_router
    from .schedules import schedules_router
    from .global_settings import global_router
    
    # Vérifier l'authentification
    from app.frontend.auth import check_authentication
    is_authenticated, message = check_authentication()
    if not is_authenticated:
        st.error(f"❌ {message}")
        st.info("🔐 Veuillez vous connecter pour accéder à cette page")
        st.stop()
    
    # Importer les utilitaires
    from app.frontend.utils import show_footer, add_bottom_spacing
    show_footer()
    
    # Router vers la page appropriée
    current_page = st.session_state.get("current_config_page", None)
    
    if current_page == "positions":
        positions_router()
    elif current_page == "schedules":
        schedules_router()
    elif current_page == "global":
        global_router()
    elif current_page == "position_detail":
        from .positions.edit import show_position_detail_config
        show_position_detail_config()
    elif current_page == "new_position":
        from .positions.new import show_new_position_form
        show_new_position_form()
    elif current_page == "users":
        try:
            import sys
            import os
            # Ajouter le chemin parent pour accéder au module user_management
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            sys.path.insert(0, parent_dir)
            
            import user_management
            
            # Vérifier que l'utilisateur est admin
            user_role = st.session_state.get("role")
            
            if user_role != "admin":
                st.error("❌ Accès refusé. Rôle administrateur requis.")
                st.info("Vous devez être administrateur pour accéder à cette page.")
                st.stop()
            
            user_management.show_users_config()
            
        except Exception as e:
            st.error(f"❌ Erreur lors de l'import: {str(e)}")
            import traceback
            st.write(f"🔍 Debug - Traceback: {traceback.format_exc()}")
    elif current_page == "new_user":
        import sys
        sys.path.append("app/frontend/pages")
        import user_management
        # Vérifier que l'utilisateur est admin
        user_role = st.session_state.get("role")
        if user_role != "admin":
            st.error("❌ Accès refusé. Rôle administrateur requis.")
            st.info("Vous devez être administrateur pour accéder à cette page.")
            st.stop()
        user_management.show_new_user()
    elif current_page == "user_detail":
        import sys
        sys.path.append("app/frontend/pages")
        import user_management
        # Vérifier que l'utilisateur est admin
        user_role = st.session_state.get("role")
        if user_role != "admin":
            st.error("❌ Accès refusé. Rôle administrateur requis.")
            st.info("Vous devez être administrateur pour accéder à cette page.")
            st.stop()
        user_management.show_user_detail_config()
    elif current_page == "reset_password":
        import sys
        sys.path.append("app/frontend/pages")
        import user_management
        # Vérifier que l'utilisateur est admin
        user_role = st.session_state.get("role")
        if user_role != "admin":
            st.error("❌ Accès refusé. Rôle administrateur requis.")
            st.info("Vous devez être administrateur pour accéder à cette page.")
            st.stop()
        user_management.show_reset_password()
    elif current_page == "user_availability":
        import sys
        sys.path.append("app/frontend/pages")
        import user_management
        # Vérifier que l'utilisateur est admin
        user_role = st.session_state.get("role")
        if user_role != "admin":
            st.error("❌ Accès refusé. Rôle administrateur requis.")
            st.info("Vous devez être administrateur pour accéder à cette page.")
            st.stop()
        user_management.show_user_availability_config()
    else:
        # Show main configuration menu
        show_main_menu()
