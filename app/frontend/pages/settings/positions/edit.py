# app/frontend/pages/settings/positions/edit.py
# Module de modification des postes avec base SQLite centralisée

import streamlit as st
import json
from datetime import datetime
from app.backend.database import db

def show_position_detail_config():
    """Afficher la configuration détaillée d'un poste pour modification"""
    
    # Initialiser la base de données si nécessaire
    try:
        if not hasattr(db, 'is_initialized') or not db.is_initialized:
            db.initialize()
            st.success("✅ Base de données initialisée avec succès")
    except Exception as e:
        st.error(f"❌ Erreur d'initialisation de la base de données: {e}")
        return
    
    # Récupérer l'ID du poste sélectionné
    selected_position_id = st.session_state.get("selected_position_to_modify")
    
    if not selected_position_id:
        st.error("❌ Aucun poste sélectionné pour modification.")
        st.info("Veuillez sélectionner un poste depuis la liste.")
        if st.button("⬅️ Retour à la liste", key="back_to_positions_list"):
            st.session_state["current_config_page"] = "positions"
            st.rerun()
        return
    
    # Récupérer les informations du poste depuis la base SQLite
    try:
        position_data = db.execute_query("""
            SELECT 
                p.*,
                pfc.week_frequency,
                pfc.weekdays,
                pfc.morning,
                pfc.afternoon,
                pfc.evening,
                pfc.weeks
            FROM positions p
            LEFT JOIN position_frequency_config pfc ON p.id = pfc.position_id
            WHERE p.id = ?
        """, (selected_position_id,))
        
        if not position_data:
            st.error(f"❌ Poste {selected_position_id} non trouvé dans la base de données.")
            if st.button("⬅️ Retour à la liste", key="back_to_positions_list_2"):
                st.session_state["current_config_page"] = "positions"
                st.rerun()
            return
        
        position_info = position_data[0]
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération du poste: {e}")
        return
    
    # Header de la page
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
            <h2 style='margin: 0; font-weight: bold;'>✏️ Modification du poste {}</h2>
        </div>
        """.format(selected_position_id), unsafe_allow_html=True)
    
    st.info(f"Modifiez les paramètres du poste {selected_position_id}", icon="ℹ️")
    
    # Formulaire de modification
    with st.form(f"edit_position_{selected_position_id}", clear_on_submit=False):
        # Informations générales du poste
        col_info1, col_info2 = st.columns(2, border=True)
        
        with col_info1:
            st.markdown("#### 📋 **Informations générales**")
            position_name = st.text_input(
                "Nom du poste",
                value=position_info.get("name", ""),
                key=f"name_{selected_position_id}"
            )
            
            # Gestion des secteurs
            current_sector = position_info.get("secteur", "Biologie moléculaire")
            sector_options = ["Biologie moléculaire", "Sérologie infectieuse", "Bactériologie"]
            
            position_sector = st.selectbox(
                "Secteur",
                options=sector_options,
                index=sector_options.index(current_sector),
                key=f"sector_{selected_position_id}"
            )
        
        with col_info2:
            st.markdown("#### 🆔 **Identifiant**")
            st.text_input(
                "ID du poste",
                value=selected_position_id,
                disabled=True,
                help="Identifiant unique du poste (non modifiable)"
            )
            
            # Gestion de la priorité
            current_priority = position_info.get("priority", 5)
            try:
                if isinstance(current_priority, str):
                    current_priority = int(current_priority)
                elif not isinstance(current_priority, int):
                    current_priority = 5
            except (ValueError, TypeError):
                current_priority = 5
            
            position_priority = st.number_input(
                "Priorité",
                min_value=1,
                max_value=10,
                value=current_priority,
                key=f"priority_{selected_position_id}"
            )
        
        # Configuration de la planification
        col_planning1, col_planning2 = st.columns(2, border=True)
        
        with col_planning1:
            st.markdown("#### 📅 **Configuration de la planification**")
            
            # 1. Fréquence des semaines
            st.markdown("**Fréquence des semaines :**")
            week_frequency = st.selectbox(
                "Selectionnez les semaines où ce poste doit être planifié",
                options=[
                    "Toutes les semaines",
                    "Une semaine sur deux", 
                    "Une semaine sur trois",
                    "Une semaine sur quatre"
                ],
                index=["Toutes les semaines", "Une semaine sur deux", "Une semaine sur trois", "Une semaine sur quatre"].index(
                    position_info.get("week_frequency", "Toutes les semaines")
                ),
                key=f"week_frequency_{selected_position_id}",
                help="Choisissez la fréquence de planification hebdomadaire"
            )
            
            # 2. Sélection des jours de la semaine
            st.markdown("**Jours de la semaine :**")
            current_weekdays = json.loads(position_info.get("weekdays", '["lundi", "mardi", "mercredi", "jeudi", "vendredi"]'))
            selected_weekdays = st.multiselect(
                "Sélectionner les jours où ce poste doit être planifié",
                options=["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
                default=current_weekdays,
                key=f"weekdays_{selected_position_id}"
            )
        
        with col_planning2:
            st.markdown("#### ⏰ **Configuration des créneaux horaires**")
            
            # 3. Sélection des créneaux horaires
            st.markdown("**Créneaux horaires :**")

            morning = st.checkbox(
                "En matinée",
                value=position_info.get("morning", True),
                key=f"morning_{selected_position_id}"
            )
            
            afternoon = st.checkbox(
                "En après-midi",
                value=position_info.get("afternoon", True),
                key=f"afternoon_{selected_position_id}"
            )
            
            evening = st.checkbox(
                "En soirée",
                value=position_info.get("evening", False),
                key=f"evening_{selected_position_id}"
            )
            
            # Espace pour équilibrer la colonne
            st.markdown("")
            st.markdown("")
            st.markdown("")
        
        position_description = st.text_area(
            "Description",
            value=position_info.get("description", ""),
            height=100,
            key=f"description_{selected_position_id}"
        )
        
        # Boutons d'action du formulaire
        col_save, col_cancel, col_delete = st.columns([1, 1, 1])
        
        with col_save:
            if st.form_submit_button("💾 Sauvegarder", use_container_width=True):
                if save_position_changes(selected_position_id, position_name, position_sector, 
                                      position_priority, position_description, week_frequency, 
                                      selected_weekdays, morning, afternoon, evening):
                    st.success(f"✅ Poste {selected_position_id} modifié avec succès !")
                    st.balloons()
                    
                    # Retour à la liste après un délai
                    import time
                    time.sleep(2)
                    st.session_state["current_config_page"] = "positions"
                    st.rerun()
        
        with col_cancel:
            if st.form_submit_button("❌ Annuler", use_container_width=True):
                st.session_state["current_config_page"] = "positions"
                st.rerun()
        
        with col_delete:
            if st.form_submit_button("🗑️ Supprimer", use_container_width=True, type="secondary"):
                if delete_position(selected_position_id):
                    st.success(f"✅ Poste {selected_position_id} supprimé avec succès !")
                    st.balloons()
                    
                    # Retour à la liste après un délai
                    import time
                    time.sleep(2)
                    st.session_state["current_config_page"] = "positions"
                    st.rerun()
                else:
                    st.error(f"❌ Erreur lors de la suppression du poste {selected_position_id}")
    
    # Boutons d'action supplémentaires (hors formulaire)
    st.markdown("---")
    
    col_back, col_mid, col_add_rule = st.columns([1, 4, 1])
    
    with col_back:
        if st.button("⬅️ Retour", key=f"back_to_positions_list_outside_{selected_position_id}"):
            st.session_state["current_config_page"] = "positions"
            st.rerun()
    
    # Ajouter de l'espace en bas de page
    st.markdown("<br><br><br>", unsafe_allow_html=True)

def save_position_changes(position_id, name, secteur, priority, description, week_frequency, 
                        weekdays, morning, afternoon, evening):
    """Sauvegarder les modifications du poste dans la base SQLite"""
    try:
        # Mettre à jour le poste
        db.execute_query("""
            UPDATE positions 
            SET name = ?, secteur = ?, priority = ?, description = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (name, secteur, priority, description, position_id), fetch=False)
        
        # Mettre à jour ou créer la configuration de fréquence
        weekdays_json = json.dumps(weekdays)
        
        # Vérifier si la configuration existe déjà
        existing_config = db.execute_query("""
            SELECT id FROM position_frequency_config WHERE position_id = ?
        """, (position_id,))
        
        if existing_config:
            # Mettre à jour la configuration existante
            db.execute_query("""
                UPDATE position_frequency_config 
                SET week_frequency = ?, weekdays = ?, morning = ?, afternoon = ?, evening = ?, updated_at = CURRENT_TIMESTAMP
                WHERE position_id = ?
            """, (week_frequency, weekdays_json, morning, afternoon, evening, position_id), fetch=False)
        else:
            # Créer une nouvelle configuration
            db.execute_query("""
                INSERT INTO position_frequency_config 
                (position_id, week_frequency, weekdays, morning, afternoon, evening)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (position_id, week_frequency, weekdays_json, morning, afternoon, evening), fetch=False)
        
        return True
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def delete_position(position_id):
    """Supprimer un poste de la base de données"""
    try:
        # Supprimer d'abord la configuration de fréquence
        db.execute_query(
            "DELETE FROM position_frequency_config WHERE position_id = ?",
            (position_id,),
            fetch=False
        )
        
        # Supprimer le poste
        db.execute_query(
            "DELETE FROM positions WHERE id = ?",
            (position_id,),
            fetch=False
        )
        
        return True
    except Exception as e:
        st.error(f"❌ Erreur lors de la suppression: {e}")
        return False
