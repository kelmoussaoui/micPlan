# app/frontend/pages/settings/positions/new.py
# Module de création de nouveaux postes avec base SQLite centralisée

import streamlit as st
import json
from app.backend.database import db

def get_next_position_id():
    """Générer automatiquement le prochain ID de poste disponible"""
    try:
        # Récupérer tous les IDs existants
        existing_ids = db.execute_query("SELECT id FROM positions ORDER BY id")
        
        if not existing_ids:
            return "P1"
        
        # Extraire les numéros des IDs existants
        used_numbers = []
        for row in existing_ids:
            try:
                number = int(row['id'][1:])  # P1 -> 1, P2 -> 2, etc.
                used_numbers.append(number)
            except (ValueError, IndexError):
                continue
        
        if not used_numbers:
            return "P1"
        
        # Trouver le prochain numéro disponible
        used_numbers.sort()
        expected_number = 1
        
        for used_num in used_numbers:
            if used_num == expected_number:
                expected_number += 1
            else:
                break
        
        return f"P{expected_number}"
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la génération de l'ID: {e}")
        return "P1"

def show_new_position_form():
    """Afficher le formulaire de création d'un nouveau poste"""
    
    # Initialiser la base de données si nécessaire
    try:
        if not hasattr(db, 'is_initialized') or not db.is_initialized:
            db.initialize()
            st.success("✅ Base de données initialisée avec succès")
    except Exception as e:
        st.error(f"❌ Erreur d'initialisation de la base de données: {e}")
        return
    
    # Générer automatiquement le prochain ID
    suggested_id = get_next_position_id()
    
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
            <h2 style='margin: 0; font-weight: bold;'>➕ Créer un nouveau poste</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.info(f"Créez un nouveau poste de travail. ID suggéré : **{suggested_id}**", icon="ℹ️")
    
    # Formulaire de création
    with st.form("new_position_form", clear_on_submit=True):
        st.markdown("### 📝 Informations générales")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_id = st.text_input(
                "ID du poste *",
                value=suggested_id,
                placeholder=f"Ex: {suggested_id}",
                disabled=True,
                help=f"Identifiant unique du poste. Suggestion automatique : {suggested_id} (non modifiable)"
            )
            
            new_name = st.text_input(
                "Nom du poste *",
                placeholder="Ex: Poste 3 - PCR",
                help="Nom descriptif du poste (obligatoire)"
            )
            
            new_secteur = st.selectbox(
                "Secteur *",
                options=["Biologie moléculaire", "Sérologie infectieuse", "Bactériologie"],
                help="Secteur d'activité du poste (obligatoire)"
            )
            
            new_min_agents = st.number_input(
                "Nombre minimum d'agents *",
                min_value=1,
                max_value=10,
                value=1,
                help="Nombre minimum d'agents requis (obligatoire)"
            )
        
        with col2:
            new_max_agents = st.number_input(
                "Nombre maximum d'agents *",
                min_value=new_min_agents,
                max_value=10,
                value=1,
                help="Nombre maximum d'agents autorisés (obligatoire)"
            )
            
            new_priority = st.number_input(
                "Priorité *",
                min_value=1,
                max_value=10,
                value=5,
                help="Niveau de priorité du poste de 1 (très basse) à 10 (très élevée)"
            )
        
        new_description = st.text_area(
            "Description",
            placeholder="Description détaillée du poste et de ses responsabilités...",
            height=100,
            help="Description détaillée du poste (optionnel)"
        )
        
        st.markdown("### ⚙️ Configuration de la planification")
        
        col_freq1, col_freq2 = st.columns(2)
        
        with col_freq1:
            week_frequency = st.selectbox(
                "Fréquence des semaines *",
                options=[
                    "Toutes les semaines",
                    "Une semaine sur deux", 
                    "Une semaine sur trois",
                    "Une semaine sur quatre"
                ],
                help="Fréquence de planification hebdomadaire (obligatoire)"
            )
            
            selected_weekdays = st.multiselect(
                "Jours de la semaine *",
                options=["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
                default=["lundi", "mardi", "mercredi", "jeudi", "vendredi"],
                help="Jours où ce poste doit être planifié (obligatoire)"
            )
        
        with col_freq2:
            morning = st.checkbox(
                "En matinée",
                value=True,
                help="Le poste est nécessaire le matin"
            )
            
            afternoon = st.checkbox(
                "En après-midi",
                value=True,
                help="Le poste est nécessaire l'après-midi"
            )
            
            evening = st.checkbox(
                "En soirée",
                value=False,
                help="Le poste est nécessaire en soirée"
            )
        
        # Boutons d'action
        col_save, col_cancel = st.columns([1, 1])
        
        with col_save:
            if st.form_submit_button("💾 Créer le poste", use_container_width=True):
                if create_new_position(new_id, new_name, new_secteur, new_min_agents, 
                                     new_max_agents, new_priority, new_description,
                                     week_frequency, selected_weekdays, morning, afternoon, evening):
                    st.success(f"✅ Poste '{new_id}' créé avec succès !")
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
    
    # Bouton retour
    st.divider()
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Retour à la liste", use_container_width=True, key="back_to_positions_list_new"):
            st.session_state["current_config_page"] = "positions"
            st.rerun()
    
    # Ajouter de l'espace en bas de page
    st.markdown("<br><br><br>", unsafe_allow_html=True)

def create_new_position(position_id, name, secteur, min_agents, max_agents, priority, 
                      description, week_frequency, weekdays, morning, afternoon, evening):
    """Créer un nouveau poste dans la base SQLite"""
    try:
        # Validation des données
        if not name.strip():
            st.error("❌ Le nom du poste est obligatoire")
            return False
        
        if not weekdays:
            st.error("❌ Veuillez sélectionner au moins un jour de la semaine")
            return False
        
        if not (morning or afternoon or evening):
            st.error("❌ Veuillez sélectionner au moins un créneau horaire")
            return False
        
        # Vérifier que l'ID n'existe pas déjà
        existing_position = db.execute_query(
            "SELECT id FROM positions WHERE id = ?",
            (position_id,)
        )
        
        if existing_position:
            st.error(f"❌ L'ID '{position_id}' existe déjà. Veuillez choisir un autre ID.")
            return False
        
        # Créer le poste
        db.execute_query("""
            INSERT INTO positions (id, name, secteur, min_agents, max_agents, priority, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (position_id, name, secteur, min_agents, max_agents, priority, description), fetch=False)
        
        # Créer la configuration de fréquence
        weekdays_json = json.dumps(weekdays)
        
        db.execute_query("""
            INSERT INTO position_frequency_config 
            (position_id, week_frequency, weekdays, morning, afternoon, evening)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (position_id, week_frequency, weekdays_json, morning, afternoon, evening), fetch=False)
        
        return True
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la création du poste: {e}")
        return False
