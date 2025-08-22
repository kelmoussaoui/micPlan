# app.py
# micPlan - Main application file

import streamlit as st
from pathlib import Path
import base64
import mimetypes

# Initialisation de la base de données
try:
    from app.backend.database import init_database
    init_database()
    print("✅ Base de données initialisée avec succès")
except Exception as e:
    print(f"❌ Erreur d'initialisation de la base de données: {e}")

from app.frontend.auth import check_authentication, show_login_page
from app.frontend.auth import show_user_info
from app.frontend.pages import home, planning, settings, my_availability, notifications, my_planning

# Page mapping - home, planning and configuration pages
PAGE_MAP = {
    "Accueil": home,
    "Mon planning": my_planning,
    "Mes disponibilités": my_availability, 
    "Centre de notifications": notifications,
    "Planning de l'équipe": planning,
    "⚙️ Configuration": settings,
    "🔧 Configuration détaillée d'un agent": "pages/agent_detail_config.py",
}

def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
        mime = mimetypes.guess_type(image_path)[0] or "image/png"
        return f"data:{mime};base64,{encoded}"

def show_sidebar():
    """Displays the sidebar with navigation and user information"""
    # Vérifier l'authentification AVANT d'afficher la sidebar
    auth_status = st.session_state.get("authentication_status")
    username = st.session_state.get("username")
    
    # Si pas authentifié, ne rien afficher
    if auth_status is not True or not username:
        return "Accueil"  # Retourner une valeur par défaut
    
    with st.sidebar:
        # Logo et version
        try:
            logo_base64 = get_base64_image("resources/images/logo.png")
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: 1rem;">
                    <img src="{logo_base64}" style="width: 100%; max-width: 200px; height: auto;">
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            # Fallback si le logo ne peut pas être chargé
            st.markdown(
                """
                <div style="text-align: center; margin-bottom: 1rem; padding: 1rem; background-color: #f0f2f6; border-radius: 8px;">
                    <h3 style="margin: 0; color: #1f77b4;">🧬 micPlan</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Application version right below the logo
        st.markdown(
            """
            <div style='margin-top: 0.4rem; margin-bottom: 0.4rem; font-size: 0.9rem; color: #666; text-align: center; line-height: 1.3;'>
                micPlan v1.0.0
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Built in Liège, Belgium
        st.markdown(
            """
            <div style="
                text-align: center;
                margin-bottom: 1rem;
                font-size: 0.8rem;
                color: #666;
                border-bottom: 1px solid #e0e0e0;
                padding-bottom: 0.5rem;
            ">
                Built in Liège, Belgium 🇧🇪
            </div>
            """,
            unsafe_allow_html=True
        )
            
        # === SECTION 1: AUTHENTICATION ===
        show_user_info()  # Remis en haut, après le logo
        
        # === SECTION 2: NAVIGATION ===
        secb = st.columns(1, border=True)[0]
        with secb:
            # Titre NAVIGATION comme bouton avec couleur différente
            st.markdown(
                """
                <div style="
                    background: rgba(120, 198, 163, 0.15);
                    color: #1f77b4;
                    padding: 0.25em 1em;
                    border-radius: 8px;
                    margin: 5px 0;
                    font-weight: bold;
                    text-align: center;
                    border: 0px;
                    margin-bottom: 0.9rem;
                ">
                    🧭
                </div>
                """,
                unsafe_allow_html=True
            )
            
            selected = st.session_state.get("selected_page", "Accueil")
            
            # Navigation menu options
            menu_options = {
                "Accueil": "home",
                "Mon planning": "my_planning",
                "Planning de l'équipe": "planning",
                "Mes disponibilités": "my_availability",
                "Centre de notifications": "notifications",
            }
            
            # Compter les notifications en attente pour l'utilisateur actuel
            pending_notifications = 0
            try:
                import json
                import os
                file_path = "data/user_availability.json"
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        availability_data = json.load(f)
                    
                    current_username = st.session_state.get("username")
                    current_user_role = st.session_state.get("role")
                    current_user_secteur = st.session_state.get("user_secteur")
                    
                    for username, user_data in availability_data.items():
                        # Vérifier si l'utilisateur actuel peut valider ces demandes
                        can_validate = False
                        if current_user_role == "admin":
                            can_validate = True
                        elif current_user_role == "superviseur" and user_data.get("secteur") == current_user_secteur:
                            can_validate = True
                        
                        if can_validate:
                            # Compter les demandes en attente
                            for request in user_data.get("leave_requests", []):
                                if request.get("status") == "En attente":
                                    pending_notifications += 1
                            
                            for absence in user_data.get("absences", []):
                                if absence.get("status") == "En attente":
                                    pending_notifications += 1
            except Exception:
                pass  # En cas d'erreur, on continue sans compter
            
            for label, identifier in menu_options.items():
                button_style = """
                    display: block;
                    width: 100%;
                    text-align: left;
                    padding: 0.5em 1em;
                    border: none;
                    background-color: #f0f2f6;
                    color: black;
                    border-radius: 5px;
                    margin: 5px 0;
                    font-weight: bold;
                """
                active = selected == label
                active_style = button_style + "background-color: #cce5ff;" if active else button_style
                
                # Ajouter le compteur de notifications pour le bouton "Centre de notifications"
                if label == "Centre de notifications" and pending_notifications > 0:
                    display_label = f"{label} 🔔 ({pending_notifications})"
                else:
                    display_label = label
                
                if st.button(display_label, key=label, use_container_width=True):
                    st.session_state["selected_page"] = label
            
            # Flexible space to push content to the bottom
            st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)
        
        # === SECTION 3: SETTINGS ===
        secc = st.columns(1, border=True)[0]
        with secc:
            # Titre SETTINGS comme bouton avec couleur différente
            st.markdown(
                """
                <div style="
                    background: rgba(255, 111, 89, 0.10);
                    color: #1f77b4;
                    padding: 0.25em 1em;
                    border-radius: 8px;
                    margin: 5px 0;
                    font-weight: bold;
                    text-align: center;
                    border: 0px;
                    margin-bottom: 0.9rem;
                ">
                    ⚙️
                </div>
                """,
                unsafe_allow_html=True
            )
        
            # User Settings button (accessible to all)
            if st.button("Configuration", use_container_width=True, key="user_settings_btn"):
                st.session_state["selected_page"] = "⚙️ Configuration"
                # Réinitialiser la page de configuration pour atterrir sur l'accueil
                if "current_config_page" in st.session_state:
                    del st.session_state["current_config_page"]
        
            # Database Management button (accessible to all users)
            if st.button("Database Management", use_container_width=True, key="database_management_btn"):
                st.info("🗄️ Database management coming soon...")
        
            # Bouton de déconnexion en bas
            if st.button("Se déconnecter", use_container_width=True, key="sidebar_logout"):
                from app.frontend.auth import logout_user
                success, message = logout_user()
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        # === SECTION 4: PARTNERS ===
        secd = st.columns(1, border=True)[0]
        with secc:
            # Titre PARTNERS comme bouton avec couleur différente
            st.markdown(
                """
                <div style="
                    background: rgba(100, 149, 237, 0.15);
                    color: #1f77b4;
                    padding: 0.25em 1em;
                    border-radius: 8px;
                    margin: 5px 0;
                    font-weight: bold;
                    text-align: center;
                    border: 0px;
                    margin-bottom: 0.2rem;
                ">
                    🏥
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Créer deux colonnes pour les logos partenaires
            col1, col2 = st.columns(2, border=False)
            
            # Logo CHU dans la première colonne
            with col1:
                try:
                    chu_logo_path = "resources/images/img/logo_chu.png"
                    if Path(chu_logo_path).exists():
                        # Centrer le logo avec du CSS personnalisé et hauteur fixe
                        st.markdown(
                            f"""
                            <div style="
                                display: flex; 
                                justify-content: center; 
                                align-items: center; 
                                height: 80px;
                                width: 100%;
                            ">
                                <img src="data:image/png;base64,{base64.b64encode(Path(chu_logo_path).read_bytes()).decode()}" 
                                     width="85" 
                                     style="display: block; margin: 0 auto;">
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.info("Logo CHU not found")
                except Exception as e:
                    st.info("Logo CHU not available")
            
            # Logo SBIM dans la deuxième colonne
            with col2:
                try:
                    sbim_logo_path = "resources/images/img/logo_sbim.png"
                    if Path(sbim_logo_path).exists():
                        # Centrer le logo avec du CSS personnalisé et hauteur fixe
                        st.markdown(
                            f"""
                            <div style="
                                display: flex; 
                                justify-content: center; 
                                align-items: center; 
                                height: 80px;
                                width: 100%;
                            ">
                                <img src="data:image/png;base64,{base64.b64encode(Path(sbim_logo_path).read_bytes()).decode()}" 
                                     width="100" 
                                     style="display: block; margin: 0 auto;">
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.info("Logo SBIM not found")
                except Exception as e:
                    st.info("Logo SBIM not available")
        
        return st.session_state.get("selected_page", "Accueil")

def main():
    # Configure session state persistence
    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None
    
    # Initialize persistent session keys
    persistent_keys = [
        "authentication_status", "username", "name", "role", 
        "session_token", "user_data", "selected_page"
    ]
    
    for key in persistent_keys:
        if key not in st.session_state:
            st.session_state[key] = None
    
    # Initialize users database if not exists
    try:
        from app.frontend.pages.user_management import init_users_database
        init_users_database()
    except Exception as e:
        st.error(f"❌ Erreur lors de l'initialisation de la base de données : {e}")
    
    # Remove native Streamlit elements and unnecessary margins
    st.markdown("""
        <style>
        #MainMenu, header, footer, [data-testid="stToolbar"] {
            display: none !important;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Check authentication - More strict check
    auth_status = st.session_state.get("authentication_status")
    username = st.session_state.get("username")
    
    # Login page - Show login if not authenticated or no username
    if auth_status is not True or not username:
        show_login_page()
        return
    
    # Additional authentication check
    is_authenticated, message = check_authentication()
    if not is_authenticated:
        st.error(f"❌ {message}")
        st.info("🔐 Please reconnect")
        st.session_state.clear()
        st.rerun()
        return
    
    # Page configuration - Ensure selected_page is always set
    if "selected_page" not in st.session_state or st.session_state["selected_page"] is None:
                    st.session_state["selected_page"] = "Accueil"
    
    # Apply sidebar CSS only after authentication
    st.markdown("""
        <style>
        /* Fixed sidebar width */
        .css-1d391kg {
            width: 320px !important;
            min-width: 320px !important;
            max-width: 320px !important;
        }
        
        /* Ensure main content area adjusts */
        .main .block-container {
            margin-left: 340px !important;
            max-width: calc(100vw - 360px) !important;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .css-1d391kg {
                width: 280px !important;
                min-width: 280px !important;
                max-width: 280px !important;
            }
            .main .block-container {
                margin-left: 300px !important;
                max-width: calc(100vw - 320px) !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display sidebar and selected page
    selected_label = show_sidebar()
    
    page_module = PAGE_MAP.get(selected_label)
    
    if page_module:
        page_module.run()
    else:
        st.error(f"❌ Unknown page: {selected_label}")
        st.info(f"Available pages: {list(PAGE_MAP.keys())}")

if __name__ == "__main__":
    main()
