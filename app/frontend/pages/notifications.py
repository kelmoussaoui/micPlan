# app/frontend/pages/notifications.py
# Centre de notifications pour les demandes et signalements

import streamlit as st
from datetime import datetime
import json
import os

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

def load_users_database():
    """Charger la base de données des utilisateurs"""
    try:
        file_path = "data/users_database.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Erreur lors du chargement des utilisateurs : {str(e)}")
    
    return {}

def get_user_role_and_sector(username):
    """Récupérer le rôle et secteur d'un utilisateur"""
    users_db = load_users_database()
    if username in users_db:
        user_info = users_db[username]
        return user_info.get("role"), user_info.get("secteur")
    return None, None

def run():
    """Main function to run the notifications page"""
    # Vérifier l'authentification
    if not st.session_state.get("authentication_status") or not st.session_state.get("username"):
        st.error("❌ Vous devez être connecté pour accéder à cette page.")
        st.info("Veuillez vous connecter pour continuer.")
        st.stop()
    
    # Récupérer les informations de l'utilisateur connecté
    current_username = st.session_state.get("username")
    current_user_role = st.session_state.get("role")
    current_user_secteur = st.session_state.get("user_secteur")
    
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
            <h2 style='margin: 0; font-weight: bold;'>🔔 Centre de notifications</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.info(f"👤 **Utilisateur :** {current_username} | **Rôle :** {current_user_role.title()} | **Secteur :** {current_user_secteur}", icon="ℹ️")
    
    # Charger les données de disponibilité
    availability_data = load_availability_data()
    
    # Vérifier et mettre à jour les demandes en retard
    check_and_update_late_requests(availability_data)
    
    # Créer des onglets selon le rôle de l'utilisateur
    if current_user_role in ["admin", "superviseur"]:
        # Superviseurs et admins ont 3 onglets
        tab1, tab2, tab3 = st.tabs(["📋 Demandes à valider", "✅ Mes demandes", "📊 Toutes les notifications"])
        
        # Tab 1: Demandes à valider (pour superviseurs et admins)
        with tab1:
            st.markdown("### 📋 Demandes en attente de validation")
            
            pending_requests = []
            
            # Collecter toutes les demandes en attente
            for username, user_data in availability_data.items():
                user_role, user_secteur = get_user_role_and_sector(username)
                
                # Vérifier si l'utilisateur actuel peut valider ces demandes
                can_validate = False
                if current_user_role == "admin":
                    can_validate = True  # Admin peut tout valider
                elif current_user_role == "superviseur" and user_secteur == current_user_secteur:
                    can_validate = True  # Superviseur peut valider son secteur
                
                # Ajouter toutes les demandes en attente (pour la visibilité)
                # Demandes de congé en attente
                for request in user_data.get("leave_requests", []):
                    if request.get("status") == "En attente":
                        pending_requests.append({
                            "type": "Demande de congé",
                            "data": request,
                            "username": username,
                            "user_role": user_role,
                            "user_secteur": user_secteur,
                            "can_validate": can_validate
                        })
                
                # Signalements d'absence en attente
                for absence in user_data.get("absences", []):
                    if absence.get("status") == "En attente":
                        pending_requests.append({
                            "type": "Signalement d'absence",
                            "data": absence,
                            "username": username,
                            "user_role": user_role,
                            "user_secteur": user_secteur,
                            "can_validate": can_validate
                        })
            
            if pending_requests:
                st.info(f"🔍 **{len(pending_requests)} demande(s) en attente de validation**", icon="ℹ️")
                
                for item in pending_requests:
                    # Formater le nom de l'utilisateur
                    user_display_name = format_user_name(item['username'])
                    with st.expander(f"🔔 {item['type']} - {user_display_name} ({item['user_secteur']})"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            if item['type'] == "Demande de congé":
                                request = item['data']
                                st.write(f"**Période :** {request['start_date']} au {request['end_date']}")
                                st.write(f"**Durée :** {request['duration_days']} jour(s)")
                                if request.get('reason'):
                                    st.write(f"**Commentaire :** {request['reason']}")
                                st.write(f"**Soumis le :** {request['submitted_date']}")
                            
                            elif item['type'] == "Signalement d'absence":
                                absence = item['data']
                                st.write(f"**Date :** {absence['date']}")
                                st.write(f"**Période :** {absence.get('duration_period', 'Non spécifiée')}")
                                if absence.get('reason'):
                                    st.write(f"**Commentaire :** {absence['reason']}")
                                st.write(f"**Signalé le :** {absence['submitted_date']}")
                        
                        with col2:
                            st.write(f"**Demandeur :** {item['username']}")
                            st.write(f"**Rôle :** {item['user_role']}")
                            st.write(f"**Secteur :** {item['user_secteur']}")
                            st.write(f"**Statut :** {item['data']['status']}")
                            
                            # Boutons de validation (seulement si l'utilisateur peut valider)
                            if item.get('can_validate', False):
                                col_approve, col_reject = st.columns(2)
                                with col_approve:
                                    if st.button("✅ Approuver", key=f"approve_{item['data']['id']}", use_container_width=True):
                                        # Approuver la demande
                                        item['data']['status'] = "Approuvé"
                                        item['data']['approved_by'] = current_username
                                        item['data']['approved_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        
                                        # Sauvegarder
                                        try:
                                            with open("data/user_availability.json", "w", encoding="utf-8") as f:
                                                json.dump(availability_data, f, ensure_ascii=False, indent=2)
                                            st.success("✅ Demande approuvée !")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Erreur lors de la sauvegarde : {e}")
                                
                                with col_reject:
                                    if st.button("❌ Rejeter", key=f"reject_{item['data']['id']}", use_container_width=True):
                                        # Rejeter la demande
                                        item['data']['status'] = "Rejeté"
                                        item['data']['rejected_by'] = current_username
                                        item['data']['rejected_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        
                                        # Sauvegarder
                                        try:
                                            with open("data/user_availability.json", "w", encoding="utf-8") as f:
                                                json.dump(availability_data, f, ensure_ascii=False, indent=2)
                                            st.success("❌ Demande rejetée !")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Erreur lors de la sauvegarde : {e}")
                            else:
                                # Afficher un message pour les utilisateurs qui ne peuvent pas valider
                                st.info("🔒 Seuls les superviseurs peuvent valider cette demande", icon="ℹ️")
            else:
                st.success("🎉 Aucune demande en attente de validation !")
        
        # Tab 2: Mes demandes (pour superviseurs et admins)
        with tab2:
            show_my_requests(current_username, availability_data)
        
        # Tab 3: Toutes les notifications (pour superviseurs et admins)
        with tab3:
            show_all_notifications(availability_data, current_user_role, current_user_secteur)
            
    else:
        # Utilisateurs normaux ont 2 onglets
        tab1, tab2 = st.tabs(["✅ Mes demandes", "📊 Toutes les notifications"])
        
        # Tab 1: Mes demandes (pour utilisateurs normaux)
        with tab1:
            show_my_requests(current_username, availability_data)
        
        # Tab 2: Toutes les notifications (pour utilisateurs normaux)
        with tab2:
            show_all_notifications(availability_data, current_user_role, current_user_secteur)
    
    # Bouton retour
    st.divider()
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Accueil", use_container_width=True, key="back_to_home"):
            st.session_state['selected_page'] = 'Accueil'
            st.rerun()
    
    # Ajouter de l'espace en bas de page
    st.markdown("<br><br><br>", unsafe_allow_html=True)

def show_my_requests(username, availability_data):
    """Afficher les demandes de l'utilisateur connecté"""
    st.markdown("### ✅ Mes demandes et signalements")
    
    if username in availability_data:
        user_data = availability_data[username]
        
        # Afficher les demandes de congé
        if user_data.get("leave_requests"):
            st.markdown("#### 🏖️ Mes demandes de congé")
            for request in user_data["leave_requests"]:
                status_color = {
                    "En attente": "🟡",
                    "En retard": "🔴",
                    "Approuvé": "🟢", 
                    "Rejeté": "⚪"
                }.get(request['status'], "⚪")
                
                with st.expander(f"{status_color} {request['type']} - {format_date(request['start_date'])} au {format_date(request['end_date'])} ({request['status']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Période :** {format_date(request['start_date'])} au {format_date(request['end_date'])}")
                        st.write(f"**Durée :** {request['duration_days']} jour(s)")
                        if request.get('reason'):
                            st.write(f"**Commentaire :** {request['reason']}")
                    with col2:
                        st.write(f"**Statut :** {request['status']}")
                        st.write(f"**Soumis le :** {request['submitted_date']}")
                        if request.get('approved_by'):
                            st.write(f"**Approuvé par :** {request['approved_by']}")
                            st.write(f"**Approuvé le :** {format_date(request.get('approved_date', ''))}")
                        if request.get('rejected_by'):
                            st.write(f"**Rejeté par :** {request['rejected_by']}")
                            st.write(f"**Rejeté le :** {format_date(request.get('rejected_date', ''))}")
        else:
            st.info("Aucune demande de congé soumise.", icon="ℹ️")
        
        # Afficher les signalements d'absence
        if user_data.get("absences"):
            st.markdown("#### 🚫 Mes signalements d'absence")
            for absence in user_data["absences"]:
                status_color = {
                    "En attente": "🟡",
                    "En retard": "🔴",
                    "Approuvé": "🟢",
                    "Rejeté": "⚪"
                }.get(absence['status'], "⚪")
                
                with st.expander(f"{status_color} {absence['type']} - {format_date(absence['date'])} ({absence.get('duration_period', 'Non spécifiée')}) - {absence['status']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Date :** {format_date(absence['date'])}")
                        st.write(f"**Période :** {absence.get('duration_period', 'Non spécifiée')}")
                        if absence.get('reason'):
                            st.write(f"**Commentaire :** {absence['reason']}")
                    with col2:
                        st.write(f"**Statut :** {absence['status']}")
                        st.write(f"**Signalé le :** {absence['submitted_date']}")
                        if absence.get('approved_by'):
                            st.write(f"**Approuvé par :** {absence['approved_by']}")
                            st.write(f"**Approuvé le :** {format_date(absence.get('approved_date', ''))}")
                        if absence.get('rejected_by'):
                            st.write(f"**Rejeté par :** {absence['rejected_by']}")
                            st.write(f"**Rejeté le :** {format_date(absence.get('rejected_date', ''))}")
        else:
            st.info("Aucun signalement d'absence.", icon="ℹ️")
    else:
        st.info("Aucune donnée de disponibilité trouvée.", icon="ℹ️")

def format_date(date_str):
    """Convertir AAAA-MM-JJ en DD/MM/AAAA (format européen)"""
    try:
        if date_str and len(date_str) == 10 and date_str.count('-') == 2:
            year, month, day = date_str.split('-')
            return f"{day}/{month}/{year}"
    except:
        pass
    return date_str

def format_user_name(username):
    """Formater le nom d'utilisateur en 'Prénom + première lettre du nom' (ex: Khalid E.)"""
    try:
        users_db = load_users_database()
        if username in users_db:
            full_name = users_db[username].get('full_name', username)
            # Diviser le nom complet en prénom et nom
            name_parts = full_name.split()
            if len(name_parts) >= 2:
                first_name = name_parts[0]
                last_name = name_parts[-1]
                first_letter_last_name = last_name[0] if last_name else ''
                return f"{first_name} {first_letter_last_name}."
            else:
                return full_name
    except:
        pass
    return username

def check_and_update_late_requests(availability_data):
    """Vérifier et mettre à jour les demandes en retard (plus d'une semaine)"""
    from datetime import datetime, timedelta
    
    one_week_ago = datetime.now() - timedelta(days=7)
    updated = False
    
    for username, user_data in availability_data.items():
        # Vérifier les demandes de congé
        for request in user_data.get("leave_requests", []):
            if request.get("status") == "En attente":
                try:
                    submitted_date = datetime.strptime(request['submitted_date'], "%Y-%m-%d %H:%M:%S")
                    if submitted_date < one_week_ago:
                        request['status'] = "En retard"
                        updated = True
                except:
                    pass  # En cas d'erreur de parsing, on continue
        
        # Vérifier les signalements d'absence
        for absence in user_data.get("absences", []):
            if absence.get("status") == "En attente":
                try:
                    submitted_date = datetime.strptime(absence['submitted_date'], "%Y-%m-%d %H:%M:%S")
                    if submitted_date < one_week_ago:
                        absence['status'] = "En retard"
                        updated = True
                except:
                    pass  # En cas d'erreur de parsing, on continue
    
    # Sauvegarder si des changements ont été effectués
    if updated:
        try:
            import json
            with open("data/user_availability.json", "w", encoding="utf-8") as f:
                json.dump(availability_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            st.warning(f"⚠️ Impossible de sauvegarder les mises à jour de statut : {e}")
    
    return updated

def show_all_notifications(availability_data, current_user_role, current_user_secteur):
    """Afficher toutes les notifications"""
    st.markdown("### 📊 Vue d'ensemble des notifications")
    
    # Vérifier et mettre à jour les demandes en retard
    check_and_update_late_requests(availability_data)
    
    if availability_data:
        # Statistiques globales
        total_requests = 0
        pending_requests = 0
        late_requests = 0
        approved_requests = 0
        rejected_requests = 0
        
        for username, user_data in availability_data.items():
            for request in user_data.get("leave_requests", []):
                total_requests += 1
                if request['status'] == "En attente":
                    pending_requests += 1
                elif request['status'] == "En retard":
                    late_requests += 1
                elif request['status'] == "Approuvé":
                    approved_requests += 1
                elif request['status'] == "Rejeté":
                    rejected_requests += 1
            
            for absence in user_data.get("absences", []):
                total_requests += 1
                if absence['status'] == "En attente":
                    pending_requests += 1
                elif absence['status'] == "En retard":
                    late_requests += 1
                elif absence['status'] == "Approuvé":
                    approved_requests += 1
                elif absence['status'] == "Rejeté":
                    rejected_requests += 1
        
        # Afficher les statistiques
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total", total_requests)
        with col2:
            st.metric("En attente", pending_requests, delta=f"+{pending_requests}")
        with col3:
            st.metric("En retard", late_requests, delta=f"+{late_requests}" if late_requests > 0 else None, delta_color="inverse")
        with col4:
            st.metric("Approuvés", approved_requests)
        with col5:
            st.metric("Rejetés", rejected_requests)
        
        st.markdown("---")
        
        # Liste de toutes les notifications
        st.markdown("#### 📋 Toutes les notifications")
        all_notifications = []
        
        for username, user_data in availability_data.items():
            user_role, user_secteur = get_user_role_and_sector(username)
            
            # Ajouter les demandes de congé
            for request in user_data.get("leave_requests", []):
                # Formater le nom de l'utilisateur
                user_display_name = format_user_name(username)
                
                all_notifications.append({
                    "Type": "Demande de congé",
                    "Nom": user_display_name,
                    "Statut": request['status'],
                    "Période": f"{format_date(request['start_date'])} au {format_date(request['end_date'])}",
                    "Durée": f"{request['duration_days']} jour(s)",
                    "Commentaire": request.get('reason', ''),
                    "Date soumission": request['submitted_date'],
                    "Approuvé par": request.get('approved_by', ''),
                    "Approuvé le": format_date(request.get('approved_date', '')) if request.get('approved_date') else '',
                    "Rejeté par": request.get('rejected_by', ''),
                    "Rejeté le": format_date(request.get('rejected_date', '')) if request.get('rejected_date') else '',
                    "Peut valider": "✅ Oui" if current_user_role == "admin" or (current_user_role == "superviseur" and user_secteur == current_user_secteur) else "❌ Non"
                })
            
            # Ajouter les signalements d'absence
            for absence in user_data.get("absences", []):
                # Formater le nom de l'utilisateur
                user_display_name = format_user_name(username)
                
                all_notifications.append({
                    "Type": "Signalement d'absence",
                    "Nom": user_display_name,
                    "Statut": absence['status'],
                    "Période": format_date(absence['date']),
                    "Durée": absence.get('duration_period', 'Non spécifiée'),
                    "Commentaire": absence.get('reason', ''),
                    "Date soumission": absence['submitted_date'],
                    "Approuvé par": absence.get('approved_by', ''),
                    "Approuvé le": format_date(absence.get('approved_date', '')) if absence.get('approved_date') else '',
                    "Rejeté par": absence.get('rejected_by', ''),
                    "Rejeté le": format_date(absence.get('rejected_date', '')) if absence.get('rejected_date') else '',
                    "Peut valider": "✅ Oui" if current_user_role == "admin" or (current_user_role == "superviseur" and user_secteur == current_user_secteur) else "❌ Non"
                })
        
        # Trier par date (plus récent en premier)
        all_notifications.sort(key=lambda x: x['Date soumission'], reverse=True)
        
        # Créer le dataframe
        if all_notifications:
            import pandas as pd
            df = pd.DataFrame(all_notifications)
            
            # Ajouter des couleurs pour le statut
            def color_status(val):
                if val == "En attente":
                    return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
                elif val == "En retard":
                    return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
                elif val == "Approuvé":
                    return 'background-color: #d4edda; color: #155724; font-weight: bold;'
                elif val == "Rejeté":
                    return 'background-color: #f5c6cb; color: #721c24; font-weight: bold;'
                return ''
            
            # Appliquer le style
            styled_df = df.style.applymap(color_status, subset=['Statut'])
            
            # Afficher le dataframe avec pagination
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Type": st.column_config.TextColumn("Type", width="medium"),
                    "Nom": st.column_config.TextColumn("Nom", width="medium"),
                    "Statut": st.column_config.TextColumn("Statut", width="small"),
                    "Période": st.column_config.TextColumn("Période", width="medium"),
                    "Durée": st.column_config.TextColumn("Durée", width="small"),
                    "Commentaire": st.column_config.TextColumn("Commentaire", width="large"),
                    "Date soumission": st.column_config.TextColumn("Date soumission", width="medium"),
                    "Peut valider": st.column_config.TextColumn("Peut valider", width="small")
                }
            )
            
        else:
            st.info("Aucune notification trouvée.", icon="ℹ️")
    else:
        st.info("Aucune notification trouvée.", icon="ℹ️")
