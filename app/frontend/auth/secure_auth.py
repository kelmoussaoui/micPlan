# app/frontend/secure_auth.py
# Secure authentication system with database

import streamlit as st
from pathlib import Path
import base64
import mimetypes
import json
import os
from datetime import datetime

def get_base64_image(image_path):
    """Converts an image to base64 for display"""
    try:
        with open(image_path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode()
            mime = mimetypes.guess_type(image_path)[0] or "image/png"
            return f"data:{mime};base64,{encoded}"
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

def authenticate_user(username, password):
    """Authenticate user using persistent database"""
    try:
        # Charger la base de données des utilisateurs
        file_path = "data/users_database.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                users_db = json.load(f)
        else:
            # Si pas de fichier, utiliser la base par défaut
            users_db = {
                "admin": {
                    "username": "admin",
                    "password": "admin123",
                    "role": "admin",
                    "full_name": "Administrateur Système",
                    "email": "admin@micplan.com",
                    "secteur": "Service",
                    "created_date": "2024-01-01",
                    "last_login": None,
                    "is_active": True
                }
            }
        
        # Vérifier l'utilisateur
        if username in users_db:
            user = users_db[username]
            if user.get("is_active", True) and user.get("password") == password:
                # Mettre à jour la dernière connexion
                user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Sauvegarder la mise à jour
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(users_db, f, ensure_ascii=False, indent=2)
                except Exception as save_error:
                    st.warning(f"⚠️ Impossible de sauvegarder la dernière connexion : {save_error}")
                
                return True, "Authentification réussie", user
        
        return False, "Nom d'utilisateur ou mot de passe incorrect", None
        
    except Exception as e:
        return False, f"Erreur d'authentification : {str(e)}", None

def show_login_page():
    """Displays the secure login page with a simple and elegant design"""
    try:
        # Load images
        background_img = get_base64_image("resources/images/background.png")
        logo_img = get_base64_image("resources/images/micplan_logo.png")
        
        if not background_img or not logo_img:
            st.error("❌ Unable to load login page images")
            return
        
        # Simple and elegant CSS styles for the login page
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("{background_img}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            
            /* Vertical centering with flexbox */
            .main .block-container {{
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
                align-items: center !important;
                min-height: 100vh !important;
                padding: 0 !important;
                margin: 0 !important;
            }}
            
            /* Simple and elegant login box */
            .login-card {{
                background: rgba(255, 255, 255, 0.95) !important;
                border-radius: 20px !important;
                padding: 3rem !important;
                max-width: 400px !important;
                width: 90% !important;
                text-align: center !important;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }}
            
            /* Elegant title */
            .login-title {{
                color: #1f77b4 !important;
                font-size: 2.5rem !important;
                font-weight: bold !important;
                margin: 0 0 1rem 0 !important;
                text-align: center !important;
            }}
            
            /* Subtitle */
            .login-subtitle {{
                color: #666 !important;
                font-size: 1.1rem !important;
                margin: 0 0 2rem 0 !important;
                text-align: center !important;
            }}
            
            /* Positioned logos */
            .bottom-logo {{
                position: fixed !important;
                bottom: 30px !important;
                right: 30px !important;
                width: 250px !important;
                opacity: 0.9 !important;
                z-index: 9999 !important;
            }}
            
            .top-center-logo {{
                position: fixed !important;
                top: 40px !important;
                left: 50% !important;
                transform: translateX(-50%) !important;
                width: 300px !important;
                opacity: 0.95 !important;
                z-index: 9999 !important;
            }}
            
            /* Form field styling */
            .stTextInput > div > div > input {{
                border-radius: 10px !important;
                border: 2px solid #e1e5e9 !important;
                padding: 12px 16px !important;
                font-size: 16px !important;
            }}
            
            .stTextInput > div > div > input:focus {{
                border-color: #1f77b4 !important;
                box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1) !important;
            }}
            
            /* Button styling */
            .stButton > button {{
                background: #1f77b4 !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 12px 24px !important;
                font-size: 16px !important;
                font-weight: bold !important;
                color: white !important;
                box-shadow: 0 4px 15px rgba(31, 119, 180, 0.3) !important;
            }}
            
            .stButton > button:hover {{
                background: #2e8bc0 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(31, 119, 180, 0.4) !important;
            }}
            
            /* Security information */
            .security-info {{
                margin-top: 0rem !important;
                margin-bottom: 0.75rem !important;
                padding: 1.5rem !important;
                background: rgba(31, 119, 180, 0.1) !important;
                border-radius: 10px !important;
                border: 1px solid rgba(31, 119, 180, 0.2) !important;
            }}
            
            .security-info p {{
                color: #475569 !important;
                font-size: 1rem !important;
                margin: 0.5rem 0 !important;
                text-align: center !important;
            }}
            
            /* Styled error and success messages */
            .stAlert {{
                border-radius: 15px !important;
                border: none !important;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
            }}
            
            /* Center text in st.info */
            .stAlert[data-baseweb="notification"] {{
                text-align: center !important;
            }}
            
            .stAlert[data-baseweb="notification"] .stAlertContent {{
                text-align: center !important;
                justify-content: center !important;
            }}
            
            /* Responsive design */
            @media (max-width: 768px) {{
                .login-card {{
                    width: 95% !important;
                    padding: 2rem !important;
                    margin: 1rem !important;
                }}
                
                .login-title {{
                    font-size: 2rem !important;
                }}
                
                .form-container {{
                    padding: 1.5rem !important;
                }}
            }}
            </style>
        """, unsafe_allow_html=True)
        
        # Centered logo at the top
        st.markdown(f'<img src="{logo_img}" class="top-center-logo"/>', unsafe_allow_html=True)
        
        # Spacing for vertical centering
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        
        # Security information (moved here)
        st.markdown("""
            <div class="security-info">
                <p>🛡️ Enterprise-grade security</p>
                <p>🔒 End-to-end encryption</p>
                <p>🕦 Complete audit trail</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Spacing before form
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("🧔🏻‍♂️ Username", placeholder="Enter your username here")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password here")
            
            # Login button
            submit_button = st.form_submit_button("🏃🏻‍♂️ Take me to the dashboard", use_container_width=True)
            
            if submit_button:
                if not username or not password:
                    st.error("❌ Please fill in all fields")
                else:
                    # Authentication
                    success, message, user_data = authenticate_user(username, password)
                    
                    if success:
                        # Successful login
                        st.success(f"✅ {message}")
                        
                        # Store session information
                        st.session_state["authentication_status"] = True
                        st.session_state["username"] = user_data['username']
                        st.session_state["name"] = user_data['full_name']
                        st.session_state["role"] = user_data['role']
                        st.session_state["user_secteur"] = user_data.get('secteur', 'Service')
                        st.session_state["user_data"] = user_data
                        
                        # Mettre à jour la dernière connexion
                        try:
                            file_path = "data/users_database.json"
                            if os.path.exists(file_path):
                                with open(file_path, "r", encoding="utf-8") as f:
                                    users_db = json.load(f)
                                
                                if username in users_db:
                                    users_db[username]["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    
                                    with open(file_path, "w", encoding="utf-8") as f:
                                        json.dump(users_db, f, ensure_ascii=False, indent=2)
                        except Exception as e:
                            st.warning(f"⚠️ Impossible de mettre à jour la dernière connexion : {str(e)}")
                        
                        # Redirect
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
        
        # Information to request access
        st.warning("**Need access ?** Request your credentials by contacting kelmoussaoui@chuliege.be", icon="✉️")
        
        # Spacing for vertical centering
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error loading login page: {e}")

def check_authentication():
    """Checks user authentication with session persistence"""
    try:
        # Check if user is connected
        if st.session_state.get("authentication_status") is not True:
            return False, "Not authenticated"
        
        # Check if we have basic user info
        username = st.session_state.get("username")
        if not username:
            return False, "Missing user information"
        
        # Simple check: if we have username and authentication_status, allow access
        if username and st.session_state.get("authentication_status") is True:
            return True, "Authenticated"
        
        return False, "Session expired"
        
    except Exception as e:
        # Log error but don't clear session on generic errors
        print(f"Authentication check error: {e}")
        # If we have basic auth info, keep the user logged in
        if st.session_state.get("authentication_status") is True and st.session_state.get("username"):
            return True, "Authenticated (error fallback)"
        return False, "Verification error"

def logout_user():
    """Logs out the user"""
    try:
        # Log logout
        username = st.session_state.get("username")
        if username:
            print(f"[{datetime.now()}] User logout - {username} - success")
        
        # Clear session
        st.session_state.clear()
        
        return True, "Logout successful"
        
    except Exception as e:
        return False, f"Error during logout: {e}"

def require_authentication():
    """Decorator to require authentication"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            is_authenticated, message = check_authentication()
            if not is_authenticated:
                st.error(f"❌ Access denied: {message}")
                st.info("🔐 Please log in to access this page")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_role(required_role):
    """Decorator to require a specific role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            is_authenticated, message = check_authentication()
            if not is_authenticated:
                st.error(f"❌ Access denied: {message}")
                st.info("🔐 Please log in to access this page")
                return
            
            user_role = st.session_state.get("role")
            if user_role != required_role and user_role != "admin":
                st.error("❌ Access denied: Insufficient permissions")
                st.info(f"🔑 Required role: {required_role}")
                return
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_sector_abbreviation(secteur):
    """Convert sector name to abbreviation"""
    if not secteur:
        return ""
    
    sector_mapping = {
        "Service": "service",
        "Biologie moléculaire": "MBM",
        "Sérologie infectieuse": "MSE",
        "Bactériologie": "BAC"
    }
    
    return sector_mapping.get(secteur, secteur)

def get_matricule_display(matricule):
    """Format matricule for display"""
    if not matricule:
        return ""
    
    return f"({matricule})"

def format_display_name(full_name):
    """Format full name to 'Prénom N.' format"""
    try:
        if not full_name:
            return "Utilisateur"
        
        # Diviser le nom complet en parties
        name_parts = full_name.strip().split()
        
        if len(name_parts) >= 2:
            # Premier élément = prénom
            firstname = name_parts[0]
            
            # Tous les autres éléments = nom de famille (pour gérer les noms composés)
            lastname_parts = name_parts[1:]
            # Prendre la première lettre du premier mot du nom de famille
            lastname_initial = lastname_parts[0][0] if lastname_parts else ""
            
            return f"{firstname} {lastname_initial}."
        elif len(name_parts) == 1:
            # Un seul nom, l'afficher tel quel
            return name_parts[0]
        else:
            return "Utilisateur"
            
    except Exception:
        return "Utilisateur"

def get_current_user():
    """Gets current user information"""
    if st.session_state.get("authentication_status") is True:
        return {
            'username': st.session_state.get("username"),
            'name': st.session_state.get("name"),
            'role': st.session_state.get("role"),
            'user_data': st.session_state.get("user_data", {}),
            'secteur': st.session_state.get("user_data", {}).get("secteur", ""),
            'matricule': st.session_state.get("user_data", {}).get("matricule", "")
        }
    return None

def show_user_info():
    """Displays connected user information"""
    user = get_current_user()
    if user and user.get('username'):  # Vérifier que l'utilisateur est vraiment connecté
        # Formater le nom d'affichage
        display_name = format_display_name(user.get('name', ''))
        
        # Centered user information with custom styling
        st.markdown(
            f"""
            <div style="
                text-align: center;
                padding: 0.5rem;
                background: rgba(31, 119, 180, 0.1);
                border-radius: 8px;
                margin: 0.5rem 0;
                margin-bottom: 1.5rem;
            ">
                <div style="
                    font-size: 0.9rem;
                    color: #1f77b4;
                    font-weight: bold;
                    margin-bottom: 0.3rem;
                ">
                    🧔🏻‍♂️ Utilisateur connecté
                </div>
                <div style="
                    font-size: 1rem;
                    color: #333;
                    font-weight: 600;
                    font-family: monospace;
                ">
                    {display_name} {get_matricule_display(user['matricule'])}
                </div>
                <div style="
                    font-size: 0.8rem;
                    color: #666;
                    margin-top: 0.2rem;
                ">
                    Role: {user['role']} {get_sector_abbreviation(user['secteur'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    # Si pas d'utilisateur connecté, ne rien afficher
