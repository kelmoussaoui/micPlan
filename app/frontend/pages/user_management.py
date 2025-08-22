import streamlit as st
from datetime import datetime
import json
import os
import time

def format_date(date_string):
    """Formate une date au format JJ/MM/AAAA"""
    if not date_string or date_string == "Jamais":
        return date_string
    
    try:
        # Si c'est déjà un objet datetime
        if isinstance(date_string, datetime):
            return date_string.strftime("%d/%m/%Y")
        
        # Si c'est une chaîne au format YYYY-MM-DD
        if isinstance(date_string, str) and "-" in date_string and len(date_string) == 10:
            date_obj = datetime.strptime(date_string, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        
        # Si c'est une chaîne au format DD/MM/YYYY (déjà formatée)
        if isinstance(date_string, str) and "/" in date_string:
            return date_string
            
        return date_string
    except Exception as e:
        return date_string

def save_users_database():
    """Save users database to JSON file"""
    try:
        if "users_database" in st.session_state:
            # Créer le dossier data s'il n'existe pas
            os.makedirs("data", exist_ok=True)
            
            # Sauvegarder dans un fichier JSON
            with open("data/users_database.json", "w", encoding="utf-8") as f:
                json.dump(st.session_state.users_database, f, ensure_ascii=False, indent=2)
            
            st.success("✅ Base de données des utilisateurs sauvegardée avec succès !")
            return True
    except Exception as e:
        st.error(f"❌ Erreur lors de la sauvegarde : {str(e)}")
        return False

def load_users_database():
    """Load users database from JSON file"""
    try:
        file_path = "data/users_database.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Erreur lors du chargement de la base de données : {str(e)}")
    
    return None

def init_users_database():
    """Initialize the users database if it doesn't exist"""
    if "users_database" not in st.session_state:
        # Essayer de charger depuis le fichier
        loaded_db = load_users_database()
        
        if loaded_db:
            st.session_state.users_database = loaded_db
            st.success("✅ Base de données des utilisateurs chargée depuis le fichier")
        else:
            # Créer la base par défaut si aucun fichier n'existe
            st.session_state.users_database = {
                            "admin": {
                "username": "admin",
                "password": "admin123",  # En production, utiliser un hash sécurisé
                "role": "admin",
                "full_name": "Administrateur Système",
                "matricule": "c221246",
                "email": "admin@micplan.com",
                "secteur": "Service",
                "created_date": "01/01/2024",
                "last_login": None,
                "is_active": True
            },
                "superviseur_bm": {
                    "username": "superviseur_bm",
                    "password": "bm123",
                    "role": "superviseur",
                    "full_name": "Marie Dubois",
                    "email": "m.dubois@micplan.com",
                    "secteur": "Biologie moléculaire",
                    "created_date": "01/01/2024",
                    "last_login": None,
                    "is_active": True,
                    "availability": {
                        "work_days": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
                        "work_hours": {"start": "08:00", "end": "17:00"},
                        "break_time": "12:00-13:00",
                        "max_hours_per_day": 8,
                        "max_hours_per_week": 40,
                        "preferred_shifts": ["Matin"],
                        "unavailable_dates": [],
                        "notes": ""
                    }
                },
                "superviseur_bact": {
                    "username": "superviseur_bact",
                    "password": "bact123",
                    "role": "superviseur",
                    "full_name": "Pierre Martin",
                    "email": "p.martin@micplan.com",
                    "secteur": "Bactériologie",
                    "created_date": "01/01/2024",
                    "last_login": None,
                    "is_active": True
                },
                "superviseur_sero": {
                    "username": "superviseur_sero",
                    "password": "sero123",
                    "role": "superviseur",
                    "full_name": "Sophie Bernard",
                    "email": "s.bernard@micplan.com",
                    "secteur": "Sérologie infectieuse",
                    "created_date": "01/01/2024",
                    "last_login": None,
                    "is_active": True,
                    "availability": {
                        "work_days": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
                        "work_hours": {"start": "08:00", "end": "17:00"},
                        "break_time": "12:00-13:00",
                        "max_hours_per_day": 8,
                        "max_hours_per_week": 40,
                        "preferred_shifts": ["Matin"],
                        "unavailable_dates": [],
                        "notes": ""
                    }
                },
                "utilisateur_bm": {
                    "username": "utilisateur_bm",
                    "password": "user123",
                    "role": "utilisateur",
                    "full_name": "Jean Dupont",
                    "email": "j.dupont@micplan.com",
                    "secteur": "Biologie moléculaire",
                    "created_date": "01/01/2024",
                    "last_login": None,
                    "is_active": True,
                    "availability": {
                        "work_days": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
                        "work_hours": {"start": "08:00", "end": "17:00"},
                        "break_time": "12:00-13:00",
                        "max_hours_per_day": 8,
                        "max_hours_per_week": 40,
                        "preferred_shifts": ["Matin"],
                        "unavailable_dates": [],
                        "notes": ""
                    }
                }
            }
            st.info("ℹ️ Base de données des utilisateurs initialisée avec les valeurs par défaut")
            
            # Sauvegarder automatiquement la base par défaut
            save_users_database()

def show_users_config():
    """Show users configuration page"""
    # Vérifier que st.session_state est initialisé
    if not hasattr(st, 'session_state'):
        st.error("❌ Erreur : session_state non initialisé")
        return
    
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
            <h2 style='margin: 0; font-weight: bold;'>👤 Gestion des utilisateurs</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("Gérez les comptes utilisateurs, les rôles et les permissions du système.", icon="ℹ️")
    
    # Initialiser la base de données des utilisateurs
    init_users_database()
    # Section pour afficher et modifier les utilisateurs existants
    col_add, col_mid, col_right = st.columns([1, 4, 1])
    with col_right:
        if st.button("➕ Nouvel utilisateur", use_container_width=True, key="add_new_user"):
            st.session_state["current_config_page"] = "new_user"
            st.rerun()
        
    
    users_database = st.session_state.users_database
    
    if not users_database:
        st.info("Aucun utilisateur configuré. Veuillez ajouter des utilisateurs.")
    else:
        # Filtres pour le rôle et le secteur
        st.markdown("#### 🔍 Filtres")
        
        # Extraire les valeurs uniques pour les filtres
        all_roles = list(set([user_info.get("role", "").title() for user_info in users_database.values()]))
        all_sectors = list(set([user_info.get("secteur", "") for user_info in users_database.values()]))
        
        # Créer des abréviations pour les secteurs
        sector_abbreviations = {
            "Biologie moléculaire": "MBM",
            "Sérologie infectieuse": "MSE", 
            "Bactériologie": "BACT",
            "Service": "Service"
        }
        
        # Initialiser les filtres dans la session state
        if "user_role_filter" not in st.session_state:
            st.session_state.user_role_filter = all_roles
        if "user_sector_filter" not in st.session_state:
            st.session_state.user_sector_filter = all_sectors
        
        # Gérer les changements de filtres
        col_filter1, col_filter2 = st.columns([1, 1])
        
        with col_filter1:
            selected_roles = st.multiselect(
                "🎭 Filtrer par rôle",
                options=all_roles,
                default=st.session_state.user_role_filter,
                help="Sélectionnez un ou plusieurs rôles à afficher",
                key="role_filter_multiselect"
            )
            # Mettre à jour la session state seulement si les filtres ont changé
            if selected_roles != st.session_state.user_role_filter:
                st.session_state.user_role_filter = selected_roles
                st.rerun()
        
        with col_filter2:
            # Utiliser les abréviations pour l'affichage mais garder les noms complets pour la logique
            sector_options = [sector_abbreviations.get(sector, sector) for sector in all_sectors]
            selected_sector_abbrevs = st.multiselect(
                "🏢 Filtrer par secteur",
                options=sector_options,
                default=[sector_abbreviations.get(sector, sector) for sector in st.session_state.user_sector_filter],
                help="Sélectionnez un ou plusieurs secteurs à afficher",
                key="sector_filter_multiselect"
            )
            
            # Convertir les abréviations sélectionnées en noms complets pour la logique
            selected_sectors = []
            for abbrev in selected_sector_abbrevs:
                for full_name, short_name in sector_abbreviations.items():
                    if short_name == abbrev:
                        selected_sectors.append(full_name)
                        break
                else:
                    # Si pas trouvé dans le mapping, utiliser l'abréviation telle quelle
                    selected_sectors.append(abbrev)
            
            # Mettre à jour la session state seulement si les filtres ont changé
            if selected_sectors != st.session_state.user_sector_filter:
                st.session_state.user_sector_filter = selected_sectors
                st.rerun()
        
        st.markdown("---")
        
        # Préparer les données pour le dataframe (avec filtres)
        users_data = []
        for username, user_info in users_database.items():
            role = user_info.get("role", "").title()
            secteur = user_info.get("secteur", "")
            
            # Appliquer les filtres
            if (not selected_roles or role in selected_roles) and (not selected_sectors or secteur in selected_sectors):
                users_data.append({
                    "Nom d'utilisateur": username,
                    "Nom complet": user_info.get("full_name", ""),
                    "Rôle": role,
                    "Secteur": secteur,
                    "Email": user_info.get("email", ""),
                    "Statut": "🟢 Actif" if user_info.get("is_active", True) else "🔴 Inactif",
                    "Dernière connexion": format_date(user_info.get("last_login", "Jamais"))
                })
        
        if users_data:
            df = st.dataframe(
                users_data,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key="users_table",
                column_config={
                    "Nom d'utilisateur": st.column_config.TextColumn(
                        "Nom d'utilisateur",
                        help="Identifiant de connexion unique",
                        width="medium"
                    ),
                    "Nom complet": st.column_config.TextColumn(
                        "Nom complet",
                        help="Nom et prénom de l'utilisateur",
                        width="medium"
                    ),
                    "Rôle": st.column_config.SelectboxColumn(
                        "Rôle",
                        help="Niveau d'accès de l'utilisateur",
                        options=["Admin", "Superviseur", "Utilisateur"],
                        width="small"
                    ),
                    "Secteur": st.column_config.SelectboxColumn(
                        "Secteur",
                        help="Secteur d'activité de l'utilisateur",
                        options=["Service", "Biologie moléculaire", "Bactériologie", "Sérologie infectieuse"],
                        width="medium"
                    ),
                    "Email": st.column_config.TextColumn(
                        "Email",
                        help="Adresse email de contact",
                        width="medium"
                    ),
                    "Statut": st.column_config.TextColumn(
                        "Statut",
                        help="État du compte utilisateur",
                        width="small"
                    ),
                    "Dernière connexion": st.column_config.TextColumn(
                        "Dernière connexion",
                        help="Date de la dernière connexion",
                        width="medium"
                    )
                }
            )
            
            # Check if a row is selected
            if df is not None and hasattr(df, 'selection') and df.selection:
                selected_rows = df.selection.get("rows", [])
                if selected_rows:
                    selected_row_index = selected_rows[0]
                    selected_username = users_data[selected_row_index]["Nom d'utilisateur"]
                    
                    # Buttons to modify or delete selected user
                    col_modify, col_delete, col_reset, col_avail, col_mid, col_right = st.columns([1, 1, 1, 1, 1, 1])
                    with col_modify:
                        if st.button("✏️ Modifier", use_container_width=True, key="modify_user"):
                            st.session_state["selected_user_to_modify"] = selected_username
                            st.session_state["current_config_page"] = "user_detail"
                            st.rerun()
                    
                    with col_delete:
                        if st.button("🗑️ Supprimer", use_container_width=True, key="delete_user", type="secondary"):
                            st.session_state["selected_user_to_delete"] = selected_username
                            st.rerun()
                    
                    with col_reset:
                        # Vérifier les permissions pour la réinitialisation du mot de passe
                        current_user_role = st.session_state.get("role", "utilisateur")
                        current_user_secteur = st.session_state.get("user_secteur", "")
                        selected_user_info = users_database.get(selected_username)
                        
                        can_reset_password = False
                        
                        if selected_user_info:
                            selected_user_role = selected_user_info.get("role", "")
                            selected_user_secteur = selected_user_info.get("secteur", "")
                            
                            # Règles de sécurité pour la réinitialisation
                            if current_user_role == "admin":
                                # Admin peut réinitialiser tout le monde
                                can_reset_password = True
                            elif current_user_role == "superviseur":
                                # Superviseur peut réinitialiser uniquement les utilisateurs de son secteur
                                can_reset_password = (selected_user_role == "utilisateur" and 
                                                   current_user_secteur == selected_user_secteur)
                            # Les utilisateurs ne peuvent réinitialiser personne
                        
                        if can_reset_password:
                            if st.button("🔑 Reset MDP", use_container_width=True, key="reset_password", type="secondary"):
                                st.session_state["selected_user_to_reset"] = selected_username
                                st.session_state["current_config_page"] = "reset_password"
                                st.rerun()
                        else:
                            # Bouton désactivé avec tooltip explicatif
                            st.button("🔑 Reset MDP", use_container_width=True, key="reset_password_disabled", 
                                    disabled=True, help="Vous n'avez pas les permissions pour réinitialiser ce mot de passe")
                    
                    with col_avail:
                        # Vérifier que l'utilisateur n'est pas admin
                        if selected_user_info and selected_user_info.get("role") != "admin":
                            if st.button("⚙️ Disponibilités", use_container_width=True, key="user_availability", type="secondary"):
                                st.session_state["selected_user_for_availability"] = selected_username
                                st.session_state["current_config_page"] = "user_availability"
                                st.rerun()
                        else:
                            # Bouton désactivé pour les admins
                            st.button("⚙️ Disponibilités", use_container_width=True, key="user_availability_disabled", 
                                    disabled=True, help="Les administrateurs n'ont pas de disponibilités configurables")
            else:
                st.info("Aucune ligne sélectionnée. Cochez une ligne dans le tableau pour voir les boutons d'action.")
    
    # Gestion de la suppression d'utilisateur
    if "selected_user_to_delete" in st.session_state and st.session_state["selected_user_to_delete"]:
        username_to_delete = st.session_state["selected_user_to_delete"]
        user_to_delete = users_database.get(username_to_delete)
        
        if user_to_delete:
            st.warning(f"⚠️ Êtes-vous sûr de vouloir supprimer l'utilisateur **{user_to_delete['full_name']}** ?")
            st.info(f"**Détails de l'utilisateur :**\n- Nom d'utilisateur: {username_to_delete}\n- Rôle: {user_to_delete['role']}\n- Secteur: {user_to_delete['secteur']}")
            
            # Checkbox de confirmation avec warning
            st.markdown("---")
            st.markdown("**⚠️ ATTENTION : Cette action est irréversible !**")
            confirm_checkbox = st.checkbox(
                "Je comprends que la suppression de cet utilisateur est définitive et irréversible",
                key="confirm_delete_checkbox",
                help="Cochez cette case pour confirmer que vous comprenez les conséquences de cette action"
            )
            
            col_confirm, col_cancel, col_mid, col_right = st.columns([1, 1, 3, 1])
            
            with col_confirm:
                if st.button("✅ Confirmer", use_container_width=True, key="confirm_delete", type="primary", disabled=not confirm_checkbox):
                    # Supprimer l'utilisateur de la base de données
                    del st.session_state.users_database[username_to_delete]
                    
                    # Sauvegarder la base de données
                    save_users_database()
                    
                    # Afficher le message de succès
                    st.success(f"✅ Utilisateur {user_to_delete['full_name']} supprimé avec succès !")
                    
                    # Nettoyer la session et rediriger
                    del st.session_state["selected_user_to_delete"]
                    time.sleep(1)
                    st.rerun()
            
            with col_cancel:
                if st.button("❌ Annuler", use_container_width=True, key="cancel_delete", type="secondary"):
                    del st.session_state["selected_user_to_delete"]
                    st.rerun()
    
    # Divider and back button
    st.divider()
    
    # Bouton retour
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Back", key="back_to_main_config", use_container_width=True):
            st.session_state["current_config_page"] = None
            st.rerun()

def show_new_user():
    """Show new user creation page"""
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
            <h2 style='margin: 0; font-weight: bold;'>👤 Créer un nouvel utilisateur</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("Remplissez le formulaire ci-dessous pour créer un nouvel utilisateur dans le système.", icon="ℹ️")
    
    # Formulaire de création d'utilisateur
    with st.form("new_user_form", clear_on_submit=True):
        st.markdown("### 📝 Informations de base")
        
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input(
                "Nom d'utilisateur *",
                placeholder="Ex: première lettre du prénom + nom de l'agent",
                help="Identifiant unique de connexion"
            )
            
            firstname = st.text_input(
                "Prénom *",
                placeholder="Ex: Marie...",
                help="Prénom de l'utilisateur"
            )
            
            lastname = st.text_input(
                "Nom *",
                placeholder="Ex: Dubois...",
                help="Nom de famille de l'utilisateur (peut contenir des espaces)"
            )
            
            matricule = st.text_input(
                "Matricule *",
                placeholder="Ex: c221246...",
                help="Numéro de matricule unique de l'utilisateur"
            )
            
            email = st.text_input(
                "Email *",
                placeholder="Ex: m.dubois@micplan.com",
                help="Adresse email de contact"
            )
        
        with col2:
            role = st.selectbox(
                "Rôle *",
                options=["utilisateur", "superviseur", "admin"],
                help="Niveau d'accès de l'utilisateur"
            )
            
            secteur = st.selectbox(
                "Secteur *",
                options=["Service", "Biologie moléculaire", "Bactériologie", "Sérologie infectieuse"],
                help="Secteur d'activité de l'utilisateur. 'Service' donne accès à tous les secteurs."
            )
            
            password = st.text_input(
                "Mot de passe *",
                type="password",
                placeholder="Ex: MotDePasse123",
                help="Mot de passe de connexion"
            )
        
        # Bouton de soumission
        if st.form_submit_button("💾 Créer l'utilisateur", use_container_width=True, type="primary"):
            # Validation des champs obligatoires
            if not username or not username.strip():
                st.error("❌ Le nom d'utilisateur est obligatoire.")
                st.stop()
            
            if not lastname or not lastname.strip():
                st.error("❌ Le nom est obligatoire.")
                st.stop()
            
            if not firstname or not firstname.strip():
                st.error("❌ Le prénom est obligatoire.")
                st.stop()
            
            if not matricule or not matricule.strip():
                st.error("❌ Le matricule est obligatoire.")
                st.stop()
            
            if not email or not email.strip():
                st.error("❌ L'email est obligatoire.")
                st.stop()
            
            if not password or not password.strip():
                st.error("❌ Le mot de passe est obligatoire.")
                st.stop()
            
            # Vérifier que le nom d'utilisateur est unique
            if "users_database" in st.session_state:
                if username in st.session_state.users_database:
                    st.error(f"❌ Le nom d'utilisateur '{username}' existe déjà. Veuillez choisir un nom unique.")
                    st.stop()
            
            # Reconstituer le nom complet à partir du prénom et nom (ordre correct)
            full_name = f"{firstname.strip()} {lastname.strip()}".strip()
            
            # Créer le nouvel utilisateur
            if "users_database" not in st.session_state:
                st.session_state.users_database = {}
            
            st.session_state.users_database[username] = {
                "username": username,
                "password": password,
                "role": role,
                "full_name": full_name,
                "matricule": matricule,
                "email": email,
                "secteur": secteur,
                "created_date": datetime.now().strftime("%d/%m/%Y"),
                "last_login": None,
                "is_active": True,
                "availability": {
                    "work_days": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
                    "work_hours": {"start": "08:00", "end": "17:00"},
                    "break_time": "12:00-13:00",
                    "max_hours_per_day": 8,
                    "max_hours_per_week": 40,
                    "preferred_shifts": ["Matin"],
                    "unavailable_dates": [],
                    "notes": ""
                }
            }
            
            st.success(f"✅ Utilisateur {full_name} (Rôle: {role}) créé avec succès !")
            
            # Sauvegarder automatiquement la base de données
            save_users_database()
            
            # Rediriger vers la page des utilisateurs après un délai
            import time
            time.sleep(1)
            st.session_state["current_config_page"] = "users"
            st.rerun()
    
    st.divider()
    
    # Bouton retour
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Retour", use_container_width=True, key="back_new_user"):
            st.session_state["current_config_page"] = "users"
            st.rerun()

def show_user_detail_config():
    """Show user detail configuration page for editing"""
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
            <h2 style='margin: 0; font-weight: bold;'>✏️ Modification d'utilisateur</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Récupérer l'utilisateur sélectionné depuis la session
    selected_username = st.session_state.get("selected_user_to_modify")
    
    if not selected_username:
        st.error("❌ Aucun utilisateur sélectionné pour modification.")
        st.info("Veuillez retourner à la liste des utilisateurs et sélectionner un utilisateur à modifier.")
        
        # Bouton retour
        col_back, col_mid, col_right = st.columns([1, 4, 1])
        with col_back:
            if st.button("⬅️ Back", key="back_to_users", use_container_width=True):
                st.session_state["current_config_page"] = "users"
                st.rerun()
        return
    
    # Récupérer les données de l'utilisateur sélectionné
    users_database = st.session_state.users_database
    if selected_username not in users_database:
        st.error(f"❌ Utilisateur {selected_username} non trouvé dans la base de données.")
        return
    
    user_info = users_database[selected_username]
    
    # Extraire prénom et nom du nom complet existant
    full_name_parts = user_info.get('full_name', '').split(' ', 1)
    existing_firstname = full_name_parts[0] if len(full_name_parts) > 0 else ''
    existing_lastname = full_name_parts[1] if len(full_name_parts) > 1 else ''
    
    st.info(f"Modification de l'utilisateur : **{user_info['full_name']}**", icon="ℹ️")
    
    # Formulaire de modification
    with st.form(key=f"edit_user_{selected_username}"):
        st.markdown("### 📝 Informations de base")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input(
                "Nom d'utilisateur *",
                value=user_info.get("username", ""),
                placeholder="Ex: superviseur_bm",
                help="Identifiant unique de connexion"
            )
            
            new_firstname = st.text_input(
                "Prénom *",
                value=existing_firstname,
                placeholder="Ex: Marie",
                help="Prénom de l'utilisateur"
            )
            
            new_lastname = st.text_input(
                "Nom *",
                value=existing_lastname,
                placeholder="Ex: El Moussaoui, Dubois...",
                help="Nom de famille de l'utilisateur (peut contenir des espaces)"
            )
            
            new_matricule = st.text_input(
                "Matricule *",
                value=user_info.get("matricule", ""),
                placeholder="Ex: c221246...",
                help="Numéro de matricule unique de l'utilisateur"
            )
            
            new_email = st.text_input(
                "Email *",
                value=user_info.get("email", ""),
                placeholder="Ex: m.dubois@micplan.com",
                help="Adresse email de contact"
            )
        
        with col2:
            new_role = st.selectbox(
                "Rôle *",
                options=["utilisateur", "superviseur", "admin"],
                index=["utilisateur", "superviseur", "admin"].index(user_info.get("role", "utilisateur")),
                help="Niveau d'accès de l'utilisateur"
            )
            
            new_secteur = st.selectbox(
                "Secteur *",
                options=["Service", "Biologie moléculaire", "Bactériologie", "Sérologie infectieuse"],
                index=["Service", "Biologie moléculaire", "Bactériologie", "Sérologie infectieuse"].index(
                    user_info.get("secteur", "Service")
                ) if user_info.get("secteur") in ["Service", "Biologie moléculaire", "Bactériologie", "Sérologie infectieuse"] else 0,
                help="Secteur d'activité de l'utilisateur. 'Service' donne accès à tous les secteurs."
            )
            

        
        st.markdown("### ⚙️ Paramètres avancés")
        
        col3, col4 = st.columns(2)
        
        with col3:
            is_active = st.checkbox(
                "Compte actif",
                value=user_info.get("is_active", True),
                help="Désactiver pour bloquer l'accès"
            )
        
        with col4:
            # Afficher la date de création (non modifiable)
            st.info(f"**Date de création :** {format_date(user_info.get('created_date', 'Non définie'))}")
            
        # Afficher la dernière connexion
        st.info(f"**Dernière connexion :** {format_date(user_info.get('last_login', 'Jamais'))}")
        
        # Bouton de soumission
        if st.form_submit_button("💾 Sauvegarder les modifications", use_container_width=True, type="primary"):
            # Validation des champs obligatoires
            if not new_username or not new_username.strip():
                st.error("❌ Le nom d'utilisateur est obligatoire.")
                st.stop()
            
            if not new_lastname or not new_lastname.strip():
                st.error("❌ Le nom est obligatoire.")
                st.stop()
            
            if not new_firstname or not new_firstname.strip():
                st.error("❌ Le prénom est obligatoire.")
                st.stop()
            
            if not new_matricule or not new_matricule.strip():
                st.error("❌ Le matricule est obligatoire.")
                st.stop()
            
            if not new_email or not new_email.strip():
                st.error("❌ L'email est obligatoire.")
                st.stop()
            
            # Vérifier que le nom d'utilisateur est unique (sauf pour l'utilisateur en cours de modification)
            if "users_database" in st.session_state:
                for username, user_data in st.session_state.users_database.items():
                    if username != selected_username and user_data.get("username") == new_username:
                        st.error(f"❌ Le nom d'utilisateur {new_username} existe déjà. Veuillez choisir un nom unique.")
                        st.stop()
            
            # Reconstituer le nom complet à partir du prénom et nom (ordre correct)
            new_full_name = f"{new_firstname.strip()} {new_lastname.strip()}".strip()
            
            # Mettre à jour l'utilisateur dans la base de données
            if new_username != selected_username:
                # Si le nom d'utilisateur a changé, créer une nouvelle entrée et supprimer l'ancienne
                st.session_state.users_database[new_username] = {
                    "username": new_username,
                    "password": user_info.get("password"),  # Conserver l'ancien mot de passe
                    "role": new_role,
                    "full_name": new_full_name,
                    "matricule": new_matricule,
                    "email": new_email,
                    "secteur": new_secteur,
                    "created_date": user_info.get("created_date"),
                    "last_login": user_info.get("last_login"),
                    "is_active": is_active,
                    "availability": user_info.get("availability", {
                        "work_days": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
                        "work_hours": {"start": "08:00", "end": "17:00"},
                        "break_time": "12:00-13:00",
                        "max_hours_per_day": 8,
                        "max_hours_per_week": 40,
                        "preferred_shifts": ["Matin"],
                        "unavailable_dates": [],
                        "notes": ""
                    })
                }
                # Supprimer l'ancienne entrée
                del st.session_state.users_database[selected_username]
            else:
                # Mettre à jour l'entrée existante
                st.session_state.users_database[selected_username].update({
                    "username": new_username,
                    "password": user_info.get("password"),  # Conserver l'ancien mot de passe
                    "role": new_role,
                    "full_name": new_full_name,
                    "matricule": new_matricule,
                    "email": new_email,
                    "secteur": new_secteur,
                    "is_active": is_active
                })
            
            st.success(f"✅ Utilisateur {new_full_name} (Rôle: {new_role}) modifié avec succès !")
            
            # Sauvegarder automatiquement la base de données
            save_users_database()
            
            # Rediriger vers la page des utilisateurs après un délai
            import time
            time.sleep(1)
            st.session_state["current_config_page"] = "users"
            st.rerun()
    
    st.divider()
    
    
    # Bouton retour
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Retour", use_container_width=True, key="back_user_detail"):
            st.session_state["current_config_page"] = "users"
            st.rerun()
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)


def show_user_availability_config():
    """Show user availability and preferences configuration page"""
    
    # Récupérer l'utilisateur sélectionné depuis la session
    selected_username = st.session_state.get("selected_user_for_availability")
    
    if not selected_username:
        st.error("❌ Aucun utilisateur sélectionné pour la configuration des disponibilités.")
        st.info("Veuillez retourner à la liste des utilisateurs et sélectionner un utilisateur.")
        
        # Bouton retour
        col_back, col_mid, col_right = st.columns([1, 4, 1])
        with col_back:
            if st.button("⬅️ Retour", key="back_to_users_availability", use_container_width=True):
                st.session_state["current_config_page"] = "users"
                st.rerun()
        return
    
    # Récupérer les données de l'utilisateur sélectionné
    users_database = st.session_state.users_database
    if selected_username not in users_database:
        st.error(f"❌ Utilisateur {selected_username} non trouvé dans la base de données.")
        return
    
    user_info = users_database[selected_username]
    
    # Vérifier que l'utilisateur n'est pas admin
    if user_info.get("role") == "admin":
        st.error("❌ Les administrateurs n'ont pas de disponibilités configurables.")
        st.info("Seuls les superviseurs et utilisateurs peuvent avoir des disponibilités configurées.")
        
        # Bouton retour
        col_back, col_mid, col_right = st.columns([1, 4, 1])
        with col_back:
            if st.button("⬅️ Retour", key="back_to_users_admin", use_container_width=True):
                st.session_state["current_config_page"] = "users"
                st.rerun()
        return
    
    # Afficher le titre avec le nom et prénom de l'utilisateur
    st.markdown(f"""
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
            <h2 style='margin: 0; font-weight: bold;'>⚙️ Configuration des disponibilités pour {user_info['full_name']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.info(f"Configuration des disponibilités pour : **{user_info['full_name']}** ({user_info.get('role', '').title()})", icon="ℹ️")
    
    # Initialiser les disponibilités si elles n'existent pas
    if "availability" not in user_info:
        user_info["availability"] = {
            "work_days": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
            "work_hours": {
                "start": "08:00",
                "end": "17:00"
            },
            "break_time": "12:00-13:00",
            "max_hours_per_day": 8,
            "max_hours_per_week": 40,
            "preferred_shifts": ["Matin"],
            "unavailable_dates": [],
            "notes": ""
        }
    
    # Formulaire de configuration des disponibilités
    with st.form(key=f"user_availability_{selected_username}"):
        st.markdown("### 📅 Jours et horaires de travail")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Jours de travail
            work_days = st.multiselect(
                "Jours de travail *",
                options=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"],
                default=user_info["availability"].get("work_days", ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]),
                help="Sélectionnez les jours où l'utilisateur est disponible"
            )
            
            # Horaires de travail
            work_start = st.time_input(
                "Heure de début *",
                value=user_info["availability"]["work_hours"].get("start", "08:00"),
                help="Heure de début de la journée de travail"
            )
            
            work_end = st.time_input(
                "Heure de fin *",
                value=user_info["availability"]["work_hours"].get("end", "17:00"),
                help="Heure de fin de la journée de travail"
            )
            
            # Pause déjeuner
            break_time = st.text_input(
                "Pause déjeuner",
                value=user_info["availability"].get("break_time", "12:00-13:00"),
                placeholder="Ex: 12:00-13:00",
                help="Plage horaire de la pause déjeuner"
            )
        
        with col2:
            # Heures maximales
            max_hours_day = st.number_input(
                "Heures max/jour",
                min_value=1,
                max_value=12,
                value=user_info["availability"].get("max_hours_per_day", 8),
                help="Nombre maximum d'heures de travail par jour"
            )
            
            max_hours_week = st.number_input(
                "Heures max/semaine",
                min_value=1,
                max_value=60,
                value=user_info["availability"].get("max_hours_per_week", 40),
                help="Nombre maximum d'heures de travail par semaine"
            )
            
            # Shifts préférés
            preferred_shifts = st.multiselect(
                "Shifts préférés",
                options=["Matin", "Après-midi", "Nuit", "Flexible"],
                default=user_info["availability"].get("preferred_shifts", ["Matin"]),
                help="Sélectionnez les types de shifts préférés"
            )
        
        st.markdown("### 📝 Notes et contraintes")
        
        notes = st.text_area(
            "Notes et contraintes particulières",
            value=user_info["availability"].get("notes", ""),
            placeholder="Ex: Préfère ne pas travailler le vendredi après-midi, Contraintes familiales...",
            help="Ajoutez des informations importantes sur les disponibilités"
        )
        
        # Bouton de soumission
        if st.form_submit_button("💾 Sauvegarder les disponibilités", use_container_width=True, type="primary"):
            # Validation des champs obligatoires
            if not work_days:
                st.error("❌ Au moins un jour de travail doit être sélectionné.")
                st.stop()
            
            # Mettre à jour les disponibilités
            user_info["availability"].update({
                "work_days": work_days,
                "work_hours": {
                    "start": work_start.strftime("%H:%M") if hasattr(work_start, 'strftime') else str(work_start),
                    "end": work_end.strftime("%H:%M") if hasattr(work_end, 'strftime') else str(work_end)
                },
                "break_time": break_time,
                "max_hours_per_day": max_hours_day,
                "max_hours_per_week": max_hours_week,
                "preferred_shifts": preferred_shifts,
                "notes": notes
            })
            
            st.success(f"✅ Disponibilités de {user_info['full_name']} sauvegardées avec succès !")
            
            # Sauvegarder automatiquement la base de données
            save_users_database()
            
            # Rediriger vers la page des utilisateurs après un délai
            import time
            time.sleep(1)
            st.session_state["current_config_page"] = "users"
            st.rerun()
    
    st.divider()
    
    # Bouton retour
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Retour", key="back_user_availability", use_container_width=True):
            st.session_state["current_config_page"] = "users"
            st.rerun()
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)


def show_reset_password():
    """Show password reset page"""
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
            <h2 style='margin: 0; font-weight: bold;'>🔑 Réinitialisation du mot de passe</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Récupérer l'utilisateur sélectionné depuis la session
    selected_username = st.session_state.get("selected_user_to_reset")
    
    if not selected_username:
        st.error("❌ Aucun utilisateur sélectionné pour la réinitialisation du mot de passe.")
        st.info("Veuillez retourner à la liste des utilisateurs et sélectionner un utilisateur.")
        
        # Bouton retour
        col_back, col_mid, col_right = st.columns([1, 4, 1])
        with col_back:
            if st.button("⬅️ Back", key="back_to_users_reset", use_container_width=True):
                st.session_state["current_config_page"] = "users"
                st.rerun()
        return
    
    # Récupérer les données de l'utilisateur sélectionné
    users_database = st.session_state.users_database
    if selected_username not in users_database:
        st.error(f"❌ Utilisateur {selected_username} non trouvé dans la base de données.")
        return
    
    user_info = users_database[selected_username]
    
    st.info(f"Réinitialisation du mot de passe pour l'utilisateur : **{user_info['full_name']}**", icon="ℹ️")
    
    # Afficher les informations de l'utilisateur
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.info(f"**Nom d'utilisateur :** {selected_username}")
        st.info(f"**Rôle :** {user_info.get('role', '').title()}")
    
    with col_info2:
        st.info(f"**Secteur :** {user_info.get('secteur', '')}")
        st.info(f"**Email :** {user_info.get('email', '')}")
    
    st.markdown("---")
    
    # Section de réinitialisation
    st.markdown("### 🔑 Nouveau mot de passe")
    
    # Générer le nouveau mot de passe
    new_password = f"{selected_username}123"
    
    st.success(f"**Nouveau mot de passe qui sera généré :** `{new_password}`")
    
    st.warning("⚠️ **Attention :** Cette action réinitialisera le mot de passe de l'utilisateur. Le nouveau mot de passe sera visible ici et devra être communiqué à l'utilisateur.")
    
    # Checkbox de confirmation
    confirm_reset_checkbox = st.checkbox(
        "Je confirme vouloir réinitialiser le mot de passe de cet utilisateur",
        key="confirm_reset_checkbox",
        help="Cochez cette case pour confirmer la réinitialisation"
    )
    
    # Boutons d'action
    col_confirm, col_cancel, col_mid, col_right = st.columns([1, 1, 2, 1])
    
    with col_confirm:
        if st.button("✅ Confirmer", use_container_width=True, key="confirm_reset", 
                   type="primary", disabled=not confirm_reset_checkbox):
            # Réinitialiser le mot de passe
            st.session_state.users_database[selected_username]["password"] = new_password
            
            # Sauvegarder la base de données
            save_users_database()
            
            # Afficher le message de succès
            st.success(f"✅ Mot de passe de {user_info['full_name']} réinitialisé avec succès !")
            st.info(f"**Nouveau mot de passe :** `{new_password}`")
            
            # Nettoyer la session et rediriger vers la gestion des utilisateurs
            del st.session_state["selected_user_to_reset"]
            st.session_state["current_config_page"] = "users"
            time.sleep(2)
            st.rerun()
    
    with col_cancel:
        if st.button("❌ Annuler", use_container_width=True, key="cancel_reset", type="secondary"):
            del st.session_state["selected_user_to_reset"]
            st.rerun()
    
    st.divider()
    
    # Bouton retour
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Retour", use_container_width=True, key="back_reset_password"):
            st.session_state["current_config_page"] = "users"
            st.rerun()
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)

