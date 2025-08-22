# app/frontend/pages/my_availability.py
# Page de gestion des disponibilités personnelles

import streamlit as st
from datetime import datetime, timedelta
import json
import os
# Pas d'import d'auth pour éviter les conflits

def save_availability_data():
    """Sauvegarder les données de disponibilité dans un fichier JSON"""
    try:
        if "user_availability" in st.session_state:
            # Créer le dossier data s'il n'existe pas
            os.makedirs("data", exist_ok=True)
            
            # Sauvegarder dans un fichier JSON
            with open("data/user_availability.json", "w", encoding="utf-8") as f:
                json.dump(st.session_state.user_availability, f, ensure_ascii=False, indent=2)
            
            return True
    except Exception as e:
        st.error(f"❌ Erreur lors de la sauvegarde : {str(e)}")
        return False

def load_availability_data():
    """Charger les données de disponibilité depuis le fichier JSON"""
    try:
        file_path = "data/user_availability.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Erreur lors du chargement : {str(e)}")
    
    return {}

def init_availability_data():
    """Initialiser la base de données des disponibilités si elle n'existe pas"""
    if "user_availability" not in st.session_state:
        # Essayer de charger depuis le fichier
        loaded_data = load_availability_data()
        
        if loaded_data:
            st.session_state.user_availability = loaded_data
        else:
            # Créer la base par défaut si aucun fichier n'existe
            st.session_state.user_availability = {}

def run():
    """Main function to run the availability page"""
    # Vérifier l'authentification
    if not st.session_state.get("authentication_status") or not st.session_state.get("username"):
        st.error("❌ Vous devez être connecté pour accéder à cette page.")
        st.info("Veuillez vous connecter pour continuer.")
        st.stop()
    
    # Initialiser les données de disponibilité
    init_availability_data()
    
    # Récupérer les informations de l'utilisateur connecté
    username = st.session_state.get("username")
    user_role = st.session_state.get("role")
    user_secteur = st.session_state.get("user_secteur")
    
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
            <h2 style='margin: 0; font-weight: bold;'>📅 Mes disponibilités et absences</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.info(f"👤 **Utilisateur :** {username} | **Rôle :** {user_role.title()} | **Secteur :** {user_secteur}", icon="ℹ️")
    
    # Créer des onglets pour organiser les différentes fonctionnalités
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Demande de congé", "🚫 Signalement d'absence", "✅ Mes disponibilités", "📊 Historique"])
    
    with tab1:
        st.markdown("### 🏖️ Demande de congé")
        st.info("Utilisez ce formulaire pour soumettre une demande de congé. Elle sera transmise à votre superviseur pour validation.", icon="ℹ️")
        
        with st.form("leave_request_form", clear_on_submit=True):
            # Ligne 1 : Dates côte à côte
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input(
                    "Date de début *",
                    min_value=datetime.now().date(),
                    help="Date de début de votre congé",
                    format="DD/MM/YYYY"
                )
            
            with col2:
                end_date = st.date_input(
                    "Date de fin *",
                    min_value=start_date,
                    help="Date de fin de votre congé",
                    format="DD/MM/YYYY"
                )
            
            # Ligne 2 : Commentaire sur toute la largeur
            reason = st.text_area(
                "Commentaire",
                placeholder="Décrivez brièvement le motif de votre congé... (optionnel)",
                help="Commentaire sur votre demande de congé (facultatif)",
                max_chars=500
            )
            
            # Bouton de soumission
            if st.form_submit_button("📤 Soumettre la demande", use_container_width=True, type="primary"):
                # Calculer automatiquement le nombre de jours
                days_requested = (end_date - start_date).days + 1
                
                # Créer la demande de congé
                leave_request = {
                    "id": f"leave_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "username": username,
                    "type": "Demande de congé",
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "duration_days": days_requested,
                    "reason": reason.strip() if reason else "",
                    "status": "En attente",
                    "submitted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "secteur": user_secteur
                }
                
                # Ajouter à la base de données
                if username not in st.session_state.user_availability:
                    st.session_state.user_availability[username] = {
                        "leave_requests": [],
                        "absences": [],
                        "availability_preferences": []
                    }
                
                st.session_state.user_availability[username]["leave_requests"].append(leave_request)
                
                # Sauvegarder
                if save_availability_data():
                    st.success(f"✅ Demande de congé soumise avec succès ! ({days_requested} jour(s) demandé(s))")
                    st.info("📧 Votre demande a été transmise à votre superviseur pour validation.", icon="ℹ️")
                else:
                    st.error("❌ Erreur lors de la sauvegarde de la demande.")
    
    with tab2:
        st.markdown("### 🚫 Signalement d'absence")
        st.info("Signalez une absence imprévue ou une indisponibilité temporaire.", icon="ℹ️")
        
        with st.form("absence_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                absence_date = st.date_input(
                    "Date d'absence *",
                    value=datetime.now().date(),
                    help="Date de votre absence",
                    format="DD/MM/YYYY"
                )
            
            with col2:
                duration_period = st.selectbox(
                    "Période d'absence *",
                    options=["Toute la journée", "La matinée uniquement", "L'après-midi uniquement", "La soirée uniquement"],
                    help="Période de votre absence"
                )
                
            absence_reason = st.text_area(
                "Commentaire *",
                placeholder="Décrivez brièvement le motif de votre absence...",
                help="Commentaire sur votre absence",
                max_chars=300
            )
        
            # Bouton de soumission
            if st.form_submit_button("📤 Signaler l'absence", use_container_width=True, type="primary"):
                if not absence_reason.strip():
                    st.error("❌ Le commentaire est obligatoire.")
                    st.stop()
                
                # Créer le signalement d'absence
                absence = {
                    "id": f"absence_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "username": username,
                    "type": "Signalement d'absence",
                    "date": absence_date.strftime("%Y-%m-%d"),
                    "duration_period": duration_period,
                    "reason": absence_reason.strip(),
                    "status": "En attente",
                    "submitted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "secteur": user_secteur
                }
                
                # Ajouter à la base de données
                if username not in st.session_state.user_availability:
                    st.session_state.user_availability[username] = {
                        "leave_requests": [],
                        "absences": [],
                        "availability_preferences": []
                    }
                
                st.session_state.user_availability[username]["absences"].append(absence)
                
                # Sauvegarder
                if save_availability_data():
                    st.success(f"✅ Absence signalée avec succès ! ({duration_period} le {absence_date.strftime('%d/%m/%Y')})")
                else:
                    st.error("❌ Erreur lors de la sauvegarde du signalement.")
    
    with tab3:
        st.markdown("### ✅ Mes disponibilités")
        st.info("Définissez vos préférences de disponibilité pour l'attribution automatique des horaires.", icon="ℹ️")
        
        with st.form("availability_preferences_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                preferred_start_time = st.time_input(
                    "Heure de début préférée",
                    value=datetime.strptime("08:00", "%H:%M").time(),
                    help="Heure de début de travail préférée"
                )
                
                preferred_end_time = st.time_input(
                    "Heure de fin préférée",
                    value=datetime.strptime("17:00", "%H:%M").time(),
                    help="Heure de fin de travail préférée"
                )
                
                max_hours_per_day = st.number_input(
                    "Heures max par jour",
                    min_value=4,
                    max_value=12,
                    value=8,
                    help="Nombre maximum d'heures de travail par jour"
                )
            
            with col2:
                preferred_days = st.multiselect(
                    "Jours préférés",
                    options=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"],
                    default=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
                    help="Jours de la semaine où vous préférez travailler"
                )
                
                flexibility = st.selectbox(
                    "Flexibilité",
                    options=["Très flexible", "Flexible", "Peu flexible", "Pas flexible"],
                    help="Votre niveau de flexibilité pour les horaires"
                )
                
                notes = st.text_area(
                    "Notes additionnelles",
                    placeholder="Autres préférences ou contraintes...",
                    help="Informations supplémentaires sur vos disponibilités",
                    max_chars=400
                )
            
            # Bouton de soumission
            if st.form_submit_button("💾 Sauvegarder mes préférences", use_container_width=True, type="primary"):
                # Créer les préférences de disponibilité
                availability_prefs = {
                    "id": f"prefs_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "username": username,
                    "preferred_start_time": preferred_start_time.strftime("%H:%M"),
                    "preferred_end_time": preferred_end_time.strftime("%H:%M"),
                    "max_hours_per_day": max_hours_per_day,
                    "preferred_days": preferred_days,
                    "flexibility": flexibility,
                    "notes": notes.strip() if notes else "",
                    "updated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "secteur": user_secteur
                }
                
                # Ajouter à la base de données
                if username not in st.session_state.user_availability:
                    st.session_state.user_availability[username] = {
                        "leave_requests": [],
                        "absences": [],
                        "availability_preferences": []
                    }
                
                # Remplacer les anciennes préférences
                st.session_state.user_availability[username]["availability_preferences"] = [availability_prefs]
                
                # Sauvegarder
                if save_availability_data():
                    st.success("✅ Préférences de disponibilité sauvegardées avec succès !")
                    st.info("🎯 Ces informations seront prises en compte dans l'attribution automatique des horaires.", icon="ℹ️")
                else:
                    st.error("❌ Erreur lors de la sauvegarde des préférences.")
    
    with tab4:
        st.markdown("### 📊 Historique de mes demandes")
        
        if username in st.session_state.user_availability:
            user_data = st.session_state.user_availability[username]
            
            # Afficher les demandes de congé
            if user_data.get("leave_requests"):
                st.markdown("#### 🏖️ Demandes de congé")
                for request in user_data["leave_requests"]:
                    with st.expander(f"{request['type']} - {request['start_date']} au {request['end_date']} ({request['status']})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Type :** {request['type']}")
                            st.write(f"**Période :** {request['start_date']} au {request['end_date']}")
                            st.write(f"**Durée :** {request['duration_days']} jour(s)")
                        with col2:
                            st.write(f"**Statut :** {request['status']}")
                            st.write(f"**Soumis le :** {request['submitted_date']}")
                            st.write(f"**Motif :** {request['reason']}")
            else:
                st.info("Aucune demande de congé soumise.", icon="ℹ️")
            
            # Afficher les absences
            if user_data.get("absences"):
                st.markdown("#### 🚫 Signalements d'absence")
                for absence in user_data["absences"]:
                    with st.expander(f"{absence['type']} - {absence['date']} ({absence['duration_hours']}h)"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Type :** {absence['type']}")
                            st.write(f"**Date :** {absence['date']}")
                            st.write(f"**Durée :** {absence['duration_hours']} heure(s)")
                        with col2:
                            st.write(f"**Statut :** {absence['status']}")
                            st.write(f"**Signalé le :** {absence['submitted_date']}")
                            st.write(f"**Motif :** {absence['reason']}")
            else:
                st.info("Aucun signalement d'absence.", icon="ℹ️")
            
            # Afficher les préférences actuelles
            if user_data.get("availability_preferences"):
                st.markdown("#### ✅ Mes préférences actuelles")
                prefs = user_data["availability_preferences"][-1]  # Dernières préférences
                with st.expander(f"Préférences mises à jour le {prefs['updated_date']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Heure début :** {prefs['preferred_start_time']}")
                        st.write(f"**Heure fin :** {prefs['preferred_end_time']}")
                        st.write(f"**Heures max/jour :** {prefs['max_hours_per_day']}")
                    with col2:
                        st.write(f"**Jours préférés :** {', '.join(prefs['preferred_days'])}")
                        st.write(f"**Flexibilité :** {prefs['flexibility']}")
                        if prefs.get('notes'):
                            st.write(f"**Notes :** {prefs['notes']}")
        else:
            st.info("Aucune donnée de disponibilité trouvée.", icon="ℹ️")
    
    # Bouton retour
    st.divider()
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Accueil", use_container_width=True, key="back_to_home"):
            st.session_state['selected_page'] = 'Accueil'
            st.rerun()
    
    # Ajouter de l'espace en bas de page
    st.markdown("<br><br><br>", unsafe_allow_html=True)
