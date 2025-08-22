# app/frontend/pages/settings/positions/list.py
# Liste des postes avec base SQLite centralisée

import streamlit as st
import json
from app.backend.database import db

def show_positions_list():
    """Afficher la liste des postes depuis la base SQLite"""
    
    # Initialiser la base de données si nécessaire
    try:
        if not hasattr(db, 'is_initialized') or not db.is_initialized:
            db.initialize()
            st.success("✅ Base de données initialisée avec succès")
    except Exception as e:
        st.error(f"❌ Erreur d'initialisation de la base de données: {e}")
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
            <h2 style='margin: 0; font-weight: bold;'>🎯 Configuration des postes</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("Configurez les postes de travail, leurs exigences et leurs contraintes.", icon="ℹ️")
    
    # Récupérer les postes depuis la base SQLite
    try:
        positions_data = db.execute_query("""
            SELECT 
                p.id,
                p.name,
                p.secteur,
                p.priority,
                p.description,
                pfc.week_frequency,
                pfc.weekdays,
                pfc.morning,
                pfc.afternoon,
                pfc.evening
            FROM positions p
            LEFT JOIN position_frequency_config pfc ON p.id = pfc.position_id
            WHERE p.is_active = 1
            ORDER BY p.id
        """)
        
        if not positions_data:
            st.warning("⚠️ Aucun poste configuré. Créez votre premier poste !")
            if st.button("➕ Créer le premier poste", type="primary"):
                st.session_state["current_config_page"] = "new_position"
                st.rerun()
            return
            
    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des postes: {e}")
        return
    
    # Bouton pour créer un nouveau poste
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Nouveau poste", type="primary", use_container_width=True):
            st.session_state["current_config_page"] = "new_position"
            st.rerun()
    
    # Affichage de la liste des postes
    st.markdown("### Liste des postes configurés")
    
    # Préparer les données pour le dataframe
    df_data = []
    for position in positions_data:
        # Traitement des données de fréquence
        weekdays = json.loads(position['weekdays']) if position['weekdays'] else []
        weekdays_str = ", ".join(weekdays[:3]) if weekdays else "Non défini"
        if len(weekdays) > 3:
            weekdays_str += f" (+{len(weekdays)-3})"
        
        # Créneaux horaires
        creneaux = []
        if position['morning']:
            creneaux.append("Matin")
        if position['afternoon']:
            creneaux.append("Après-midi")
        if position['evening']:
            creneaux.append("Soirée")
        creneaux_str = " + ".join(creneaux) if creneaux else "Aucun créneau"
        
        # Fréquence
        frequency_display = f"{position['week_frequency']} - {weekdays_str} - {creneaux_str}"
        
        # Priorité avec conversion en label
        priority_label = get_priority_label(position['priority'])
        
        df_data.append({
            "ID Poste": position['id'],
            "Nom": position['name'],
            "Secteur": position['secteur'],
            "Fréquence": frequency_display,
            "Priorité": priority_label,
            "Description": position['description'] or ""
        })
    
    # Créer le dataframe avec sélection
    import pandas as pd
    df = pd.DataFrame(df_data)
    
    # Affichage du dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=400,
        key="positions_dataframe"
    )
    
    # Sélection d'un poste pour modification
    st.markdown("---")
    st.markdown("### 🔧 Modifier un poste")
    
    if df_data:
        selected_position_id = st.selectbox(
            "Sélectionner un poste à modifier",
            options=[pos["ID Poste"] for pos in df_data],
            format_func=lambda x: f"{x} - {next(pos['Nom'] for pos in df_data if pos['ID Poste'] == x)}"
        )
        
        if selected_position_id:
            col_modify, col_delete = st.columns([1, 1])
            
            with col_modify:
                if st.button("✏️ Modifier", key=f"modify_{selected_position_id}", use_container_width=True):
                    st.session_state["selected_position_to_modify"] = selected_position_id
                    st.session_state["current_config_page"] = "position_detail"
                    st.rerun()
            
            with col_delete:
                if st.button("🗑️ Supprimer", key=f"delete_{selected_position_id}", use_container_width=True, type="secondary"):
                    if delete_position(selected_position_id):
                        st.success(f"✅ Poste {selected_position_id} supprimé avec succès !")
                        st.rerun()
                    else:
                        st.error(f"❌ Erreur lors de la suppression du poste {selected_position_id}")
    else:
        st.info("Aucun poste disponible pour modification")

def get_priority_label(priority):
    """Convertir la priorité numérique en label lisible"""
    try:
        priority_num = int(priority)
        if 1 <= priority_num <= 3:
            return "Faible"
        elif 4 <= priority_num <= 7:
            return "Normal"
        elif 8 <= priority_num <= 10:
            return "Élevée"
        else:
            return str(priority)
    except (ValueError, TypeError):
        return str(priority)

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
