import streamlit as st
from datetime import datetime

def init_auth():
    """Initialize authentication system"""
    if "authenticated_user" not in st.session_state:
        st.session_state.authenticated_user = None
    
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    
    if "user_secteur" not in st.session_state:
        st.session_state.user_secteur = None

def show_login_page():
    """Show login page"""
    st.markdown("""
        <div style='
            background: linear-gradient(90deg, #e0effd 0%, #fff5e8 100%);
            padding: 2rem;
            border-radius: 1rem;
            border-left: 5px solid #2994f2;
            border-right: 5px solid #fbbf5d;
            margin: 2rem auto;
            max-width: 500px;
            text-align: center;
        '>
            <h1 style='margin: 0; font-weight: bold; color: #1f4e79;'>🔐 micPlan</h1>
            <p style='margin: 1rem 0; color: #666;'>Système de planification des laboratoires</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Initialiser la base de données des utilisateurs
    # Note: Cette fonction sera appelée depuis le module principal
    # pour éviter les imports circulaires
    
    # Formulaire de connexion
    with st.form("login_form", clear_on_submit=False):
        st.markdown("### 🔑 Connexion")
        
        username = st.text_input(
            "Nom d'utilisateur",
            placeholder="Entrez votre nom d'utilisateur",
            help="Votre identifiant de connexion"
        )
        
        password = st.text_input(
            "Mot de passe",
            type="password",
            placeholder="Entrez votre mot de passe",
            help="Votre mot de passe"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("🚀 Se connecter", use_container_width=True, type="primary"):
                if authenticate_user(username, password):
                    st.success("✅ Connexion réussie !")
                    # Rediriger vers la page d'accueil
                    import time
                    time.sleep(1)
                    st.session_state['selected_page'] = 'Accueil'
                    st.rerun()
                else:
                    st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")
    
    # Informations de connexion pour les tests
    st.markdown("---")
    st.markdown("### 📋 **Comptes de test disponibles :**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👑 Administrateur :**")
        st.code("admin / admin123")
        
        st.markdown("**👨‍💼 Superviseur Biologie Moléculaire :**")
        st.code("superviseur_bm / bm123")
        
        st.markdown("**👨‍💼 Superviseur Bactériologie :**")
        st.code("superviseur_bact / bact123")
    
    with col2:
        st.markdown("**👨‍💼 Superviseur Sérologie :**")
        st.code("superviseur_sero / sero123")
        
        st.markdown("**👤 Utilisateur Biologie Moléculaire :**")
        st.code("utilisateur_bm / user123")

def authenticate_user(username, password):
    """Authenticate user with username and password"""
    if not username or not password:
        return False
    
    users_database = st.session_state.get("users_database", {})
    
    if username in users_database:
        user_info = users_database[username]
        
        # Vérifier le mot de passe
        if user_info.get("password") == password:
            # Vérifier que le compte est actif
            if user_info.get("is_active", True):
                # Connexion réussie
                st.session_state.authenticated_user = username
                st.session_state.user_role = user_info.get("role")
                st.session_state.user_secteur = user_info.get("secteur")
                
                # Mettre à jour la dernière connexion
                users_database[username]["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                return True
            else:
                st.error("❌ Ce compte utilisateur est désactivé.")
                return False
        else:
            return False
    
    return False

def require_auth():
    """Require authentication to access the page"""
    init_auth()
    
    if not st.session_state.authenticated_user:
        st.error("❌ Vous devez être connecté pour accéder à cette page.")
        st.info("Veuillez vous connecter pour continuer.")
        
        if st.button("🔑 Aller à la connexion"):
            st.session_state['selected_page'] = '🔐 Connexion'
            st.rerun()
        
        st.stop()
    
    return True

def require_role(required_role):
    """Require specific role to access the page"""
    require_auth()
    
    user_role = st.session_state.get("user_role")
    
    if user_role != required_role and user_role != "admin":
        st.error(f"❌ Accès refusé. Rôle requis : {required_role}")
        st.info("Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
        
        if st.button("⬅️ Retour à l'accueil"):
            st.session_state['selected_page'] = 'Accueil'
            st.rerun()
        
        st.stop()
    
    return True

def require_admin():
    """Require admin role to access the page"""
    return require_role("admin")

def require_supervisor():
    """Require supervisor role to access the page"""
    return require_role("superviseur")

def get_current_user_info():
    """Get current authenticated user information"""
    if not st.session_state.authenticated_user:
        return None
    
    users_database = st.session_state.get("users_database", {})
    username = st.session_state.authenticated_user
    
    if username in users_database:
        return users_database[username]
    
    return None

def show_user_info():
    """Show current user information in sidebar"""
    if st.session_state.authenticated_user:
        user_info = get_current_user_info()
        if user_info:
            with st.sidebar:
                st.markdown("### 👤 **Utilisateur connecté**")
                st.info(f"**{user_info['full_name']}**")
                st.caption(f"Rôle: {user_info['role'].title()}")
                st.caption(f"Secteur: {user_info['secteur']}")
                
                if st.button("Se déconnecter", use_container_width=True):
                    logout_user()
                    st.rerun()

def logout_user():
    """Logout current user"""
    st.session_state.authenticated_user = None
    st.session_state.user_role = None
    st.session_state.user_secteur = None
    
    # Rediriger vers la page de connexion
    st.session_state['selected_page'] = '🔐 Connexion'
    st.rerun()

def check_permissions(resource_secteur):
    """Check if user has permission to access a specific sector resource"""
    require_auth()
    
    user_role = st.session_state.get("user_role")
    user_secteur = st.session_state.get("user_secteur")
    
    # Les admins ont accès à tout
    if user_role == "admin":
        return True
    
    # Le secteur "Service" a accès à tout
    if user_secteur == "Service":
        return True
    
    # Les superviseurs et utilisateurs ont accès uniquement à leur secteur
    if user_secteur == resource_secteur:
        return True
    
    return False

def filter_by_user_sector(data_dict, sector_key="secteur"):
    """Filter data by user's sector"""
    require_auth()
    
    user_role = st.session_state.get("user_role")
    user_secteur = st.session_state.get("user_secteur")
    
    # Les admins voient tout
    if user_role == "admin":
        return data_dict
    
    # Le secteur "Service" voit tout
    if user_secteur == "Service":
        return data_dict
    
    # Filtrer par secteur pour les autres rôles
    filtered_data = {}
    for key, value in data_dict.items():
        if isinstance(value, dict) and value.get(sector_key) == user_secteur:
            filtered_data[key] = value
    
    return filtered_data
