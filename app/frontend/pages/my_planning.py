# app/frontend/pages/my_planning.py
# Mon planning page - Planning filtré par l'agent connecté

import streamlit as st
from datetime import date, timedelta
import pandas as pd

def run():
    """Main function to run the my planning page"""
    # Vérifier l'authentification
    if not st.session_state.get("authentication_status") or not st.session_state.get("username"):
        st.error("❌ Vous devez être connecté pour accéder à cette page.")
        st.info("Veuillez vous connecter pour continuer.")
        st.stop()
    
    # Récupérer les informations de l'utilisateur connecté
    current_username = st.session_state.get("username")
    current_user_role = st.session_state.get("role")
    current_user_secteur = st.session_state.get("user_secteur")
    
    # Page header avec style moderne
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
            <h2 style='margin: 0; font-weight: bold;'>📅 Mon Planning</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.info(f"👤 **Utilisateur :** {current_username} | **Rôle :** {current_user_role.title()} | **Secteur :** {current_user_secteur}", icon="ℹ️")
    
    # Date range selector
    st.markdown("### 📅 Sélection de la période")
    
    # Get current date
    today = date.today()
    
    col_date1, col_date2, col_week = st.columns([1, 1, 1])
    
    with col_date1:
        # Initialize start_date from session state or default
        if "my_planning_start_date" not in st.session_state:
            st.session_state.my_planning_start_date = today - timedelta(days=7)
        
        start_date = st.date_input(
            "📅 Date de début",
            value=st.session_state.my_planning_start_date,
            format="DD/MM/YYYY",
            key="my_planning_start_date_input"
        )
        # Update session state when user changes the date
        if start_date != st.session_state.my_planning_start_date:
            st.session_state.my_planning_start_date = start_date
    
    with col_date2:
        # Initialize end_date from session state or default
        if "my_planning_end_date" not in st.session_state:
            st.session_state.my_planning_end_date = today + timedelta(days=7)
        
        end_date = st.date_input(
            "📅 Date de fin",
            value=st.session_state.my_planning_end_date,
            format="DD/MM/YYYY",
            key="my_planning_end_date_input"
        )
        # Update session state when user changes the date
        if end_date != st.session_state.my_planning_end_date:
            st.session_state.my_planning_end_date = end_date
    
    with col_week:
        st.markdown("**Semaine actuelle**")
        current_week = f"{today.strftime('%d/%m')} - {(today + timedelta(days=6)).strftime('%d/%m')}"
        st.info(f"📅 {current_week}")
    
    # Validate date range
    if start_date > end_date:
        st.error("❌ La date de début doit être antérieure à la date de fin")
        start_date, end_date = end_date, start_date
        st.info("🔄 Les dates ont été inversées automatiquement")
    
    # Calculate period days
    period_days = (end_date - start_date).days + 1
    
    # Quick week navigation buttons
    st.markdown("**🔍 Navigation rapide**")
    col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns(5)
    
    with col_nav1:
        if st.button("📅 Semaine précédente", use_container_width=True, key="my_planning_prev_week"):
            # Calculate previous week
            current_week_start = today - timedelta(days=today.weekday())
            start_date = current_week_start - timedelta(days=7)
            end_date = start_date + timedelta(days=6)
            st.session_state.my_planning_start_date = start_date
            st.session_state.my_planning_end_date = end_date
            st.rerun()
    
    with col_nav2:
        if st.button("📅 Cette semaine", use_container_width=True, key="my_planning_current_week"):
            # Calculate current week
            current_week_start = today - timedelta(days=today.weekday())
            start_date = current_week_start
            end_date = start_date + timedelta(days=6)
            st.session_state.my_planning_start_date = start_date
            st.session_state.my_planning_end_date = end_date
            st.rerun()
    
    with col_nav3:
        if st.button("📅 Semaine prochaine", use_container_width=True, key="my_planning_next_week"):
            # Calculate next week
            current_week_start = today - timedelta(days=today.weekday())
            start_date = current_week_start + timedelta(days=7)
            end_date = start_date + timedelta(days=6)
            st.session_state.my_planning_start_date = start_date
            st.session_state.my_planning_end_date = end_date
            st.rerun()
    
    with col_nav4:
        if st.button("📅 Ce mois", use_container_width=True, key="my_planning_current_month"):
            # Calculate current month
            start_date = today.replace(day=1)
            if today.month == 12:
                end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
            st.session_state.my_planning_start_date = start_date
            st.session_state.my_planning_end_date = end_date
            st.rerun()
    
    with col_nav5:
        if st.button("📅 Prochain mois", use_container_width=True, key="my_planning_next_month"):
            # Calculate next month
            if today.month == 12:
                start_date = today.replace(year=today.year + 1, month=1, day=1)
                end_date = today.replace(year=today.year + 1, month=2, day=1) - timedelta(days=1)
            else:
                start_date = today.replace(month=today.month + 1, day=1)
                if today.month == 11:
                    end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
                else:
                    end_date = today.replace(month=today.month + 2, day=1) - timedelta(days=1)
            st.session_state.my_planning_start_date = start_date
            st.session_state.my_planning_end_date = end_date
            st.rerun()
    
    st.markdown("---")
    
    # Afficher le planning filtré pour l'utilisateur connecté
    st.markdown(f"### 📋 Mon planning du {start_date.strftime('%d/%m/%Y')} au {end_date.strftime('%d/%m/%Y')}")
    
    # Simuler un planning (à remplacer par les vraies données)
    # Pour l'instant, on affiche un planning fictif basé sur le nom d'utilisateur
    
    # Créer des données de planning fictives pour l'exemple
    planning_data = create_sample_planning(current_username, start_date, end_date)
    
    if planning_data:
        # Créer un tableau avec les jours en colonnes et 3 lignes
        display_planning_table(planning_data)
        
        # Statistiques personnelles
        st.markdown("### 📊 Mes Statistiques")
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        total_days = len(planning_data)
        working_days = len([d for d in planning_data if d['Jour'] not in ['Samedi', 'Dimanche']])
        weekend_days = total_days - working_days
        
        with col_stats1:
            st.metric("Total jours", total_days)
        with col_stats2:
            st.metric("Jours ouvrés", working_days)
        with col_stats3:
            st.metric("Weekends", weekend_days)
        with col_stats4:
            st.metric("Période", f"{period_days} jour(s)")
        
    else:
        st.info("📝 Aucun planning disponible pour cette période.", icon="ℹ️")
    
    # Bouton retour
    st.divider()
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Accueil", use_container_width=True, key="my_planning_back_to_home"):
            st.session_state['selected_page'] = 'Accueil'
            st.rerun()
    
    # Ajouter de l'espace en bas de page
    st.markdown("<br><br><br>", unsafe_allow_html=True)

def display_planning_table(planning_data):
    """Afficher le planning sous forme de tableau ligne par ligne avec 3 colonnes"""
        
    # Créer un DataFrame pour l'affichage ligne par ligne
    table_data = []
    date_mapping = {}  # Mapping pour garder la référence aux dates originales
    
    for day_data in planning_data:
        date_str = day_data['Date'].strftime('%d/%m/%Y')
        day_name = day_data['Jour']
        
        # Stocker le mapping pour le styling
        date_mapping[date_str] = day_data['Date']
        
        # Déterminer le type de jour
        if day_data['Jour'] in ['Samedi', 'Dimanche']:
            type_jour = "WE"  # Weekend
        elif is_holiday(day_data['Date']):
            type_jour = "Férié"   # Férié
        else:
            type_jour = ""   # Jour ouvré - rien affiché
        
        if day_data['Jour'] in ['Samedi', 'Dimanche']:
            # Weekend
            row = {
                "Date": date_str,
                "T": type_jour,
                "Jour": day_name,
                "Poste en matinée": "Repos",
                "Poste l'après-midi": "Repos"
            }
        else:
            # Jour ouvré
            position = day_data['Position']
            
            # Diviser la position en AM et PM (pour l'exemple)
            if ":" in position:
                # Si la position contient ":", on la divise
                parts = position.split(":")
                poste_am = parts[0].strip()
                poste_pm = parts[1].strip() if len(parts) > 1 else parts[0].strip()
            else:
                # Sinon on utilise la même position pour AM et PM
                poste_am = position
                poste_pm = position
            
            row = {
                "Date": date_str,
                "T": type_jour,
                "Jour": day_name,
                "Poste en matinée": poste_am,
                "Poste l'après-midi": poste_pm
            }
        
        table_data.append(row)
    
    # Créer le DataFrame
    df = pd.DataFrame(table_data)
    
    # Configuration des colonnes
    column_config = {
        "Date": st.column_config.TextColumn(
            "Date",
            help="Date au format JJ/MM/AAAA",
            width="medium",
            disabled=True
        ),
        "T": st.column_config.TextColumn(
            "T",
            help="Type de jour (WE: Week-end, Férié: Férié, vide: Ouverture)",
            width="small",
            disabled=True
        ),
        "Jour": st.column_config.TextColumn(
            "Jour",
            help="Jour de la semaine",
            width="small",
            disabled=True
        ),
        "Poste en matinée": st.column_config.TextColumn(
            "Poste en matinée",
            help="Position de travail le matin",
            width="large",
            disabled=True
        ),
        "Poste l'après-midi": st.column_config.TextColumn(
            "Poste l'après-midi",
            help="Position de travail l'après-midi",
            width="large",
            disabled=True
        )
    }
    
    # Afficher le dataframe avec styling conditionnel
    st.markdown("#### 📅 Planning détaillé")
    
    # Créer une version stylisée du dataframe
    styled_df = df.copy()
    
    # Ajouter des indicateurs visuels
    def style_row(row):
        # Griser les jours où le laboratoire n'est pas ouvert (weekends + jours fériés)
        type_jour = row['T']
        
        if type_jour in ['WE', 'Férié']:  # Weekend ou Férié
            return ['background-color: #e9ecef; color: #495057; font-style: italic; opacity: 0.7'] * len(row)
        else:
            return ['background-color: #ffffff'] * len(row)
    
    # Appliquer le styling
    styled_df = styled_df.style.apply(style_row, axis=1)
    
    # Afficher le dataframe stylisé avec des colonnes de proportions forcées
    st.markdown("""
    <style>
    .planning-table {
        width: 100%;
        table-layout: fixed;
    }
    .planning-table th:nth-child(1) { width: 15%; }  /* Date */
    .planning-table th:nth-child(2) { width: 5%; }   /* T */
    .planning-table th:nth-child(3) { width: 12%; }  /* Jour */
    .planning-table th:nth-child(4) { width: 34%; }  /* Poste matinée */
    .planning-table th:nth-child(5) { width: 34%; }  /* Poste après-midi */
    </style>
    """, unsafe_allow_html=True)
    
    # Afficher le dataframe avec proportions forcées
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Légende
    st.markdown("""
    <div style='margin-top: 1rem; padding: 1rem; background-color: #f8f9fa; border-radius: 5px; border-left: 4px solid #007bff;'>
        <strong>📋 Légende :</strong><br>
        • <strong>Date :</strong> Date au format JJ/MM/AAAA<br>
        • <strong>T :</strong> Type de jour (WE: Week-end, Férié: Férié, vide: Ouverture)<br>
        • <strong>Jour :</strong> Jour de la semaine (Lundi, Mardi, etc.)<br>
        • <strong>Poste en matinée :</strong> Position de travail le matin<br>
        • <strong>Poste l'après-midi :</strong> Position de travail l'après-midi<br>
        <br>
        <strong>🎨 Codes couleur :</strong><br>
        • <span style='background-color: #e9ecef; padding: 2px 6px; border-radius: 3px;'>Gris</span> : Weekends et jours fériés belges (laboratoire fermé)<br>
        • <span style='background-color: #ffffff; padding: 2px 6px; border-radius: 3px; border: 1px solid #dee2e6;'>Blanc</span> : Jours d'ouverture du laboratoire
    </div>
    """, unsafe_allow_html=True)

def is_holiday(date_obj):
    """Vérifier si une date est un jour férié belge"""
    year = date_obj.year
    
    # Jours fériés fixes belges
    fixed_holidays = [
        (1, 1),    # 1er janvier - Nouvel An
        (5, 1),    # 1er mai - Fête du travail
        (7, 21),   # 21 juillet - Fête nationale belge
        (8, 15),   # 15 août - Assomption
        (11, 1),   # 1er novembre - Toussaint
        (11, 11),  # 11 novembre - Armistice 1918
        (12, 25),  # 25 décembre - Noël
    ]
    
    # Jours fériés variables (calculés)
    # Pâques (dimanche après la première pleine lune du printemps)
    # Simplification : utiliser des dates approximatives pour les années courantes
    easter_dates = {
        2024: (3, 31),  # 31 mars 2024
        2025: (4, 20),  # 20 avril 2025
        2026: (4, 5),   # 5 avril 2026
        2027: (3, 28),  # 28 mars 2027
        2028: (4, 16),  # 16 avril 2028
        2029: (4, 1),   # 1er avril 2029
        2030: (4, 21),  # 21 avril 2030
    }
    
    # Vérifier les jours fériés fixes
    if (date_obj.month, date_obj.day) in fixed_holidays:
        return True
    
    # Vérifier Pâques et les jours associés
    if year in easter_dates:
        easter_month, easter_day = easter_dates[year]
        easter_date = date(year, easter_month, easter_day)
        
        # Lundi de Pâques (jour suivant Pâques)
        easter_monday = easter_date + timedelta(days=1)
        # Jeudi de l'Ascension (39 jours après Pâques)
        ascension = easter_date + timedelta(days=39)
        # Lundi de Pentecôte (50 jours après Pâques)
        pentecote = easter_date + timedelta(days=50)
        
        if date_obj in [easter_monday, ascension, pentecote]:
            return True
    
    return False

def create_sample_planning(username, start_date, end_date):
    """Créer un planning fictif pour l'exemple (à remplacer par les vraies données)"""
    planning_data = []
    current_date = start_date
    
    # Positions possibles basées sur le nom d'utilisateur
    positions = {
        "admin": ["P1 : Tri & urgences", "P2 : Extraction", "P3 : PCR & détection", "P4 : Génotypage HCV", "P5 : NGS HIV", "P6 : Alinity", "P7 : C6800", "P8 : QC & maintenances", "P9 : Mycoses"],
        "superviseur": ["P1 : Tri & urgences", "P2 : Extraction", "P3 : PCR & détection", "P4 : Génotypage HCV", "P5 : NGS HIV"],
        "utilisateur": ["P1 : Tri & urgences", "P2 : Extraction", "P3 : PCR & détection"]
    }
    
    # Récupérer le rôle de l'utilisateur
    user_role = st.session_state.get("role", "utilisateur")
    available_positions = positions.get(user_role, positions["utilisateur"])
    
    while current_date <= end_date:
        # Déterminer le jour de la semaine
        day_name = current_date.strftime('%A')
        french_days = {
            'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
            'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'Dimanche'
        }
        french_day = french_days.get(day_name, day_name)
        
        # Générer une position aléatoire pour ce jour
        import random
        if french_day not in ['Samedi', 'Dimanche']:
            position = random.choice(available_positions)
            horaire = "08:00-17:00"
            statut = "Planifié"
        else:
            position = "Repos"
            horaire = "-"
            statut = "Weekend"
        
        planning_data.append({
            "Date": current_date,
            "Jour": french_day,
            "Position": position,
            "Horaire": horaire,
            "Statut": statut
        })
        
        current_date += timedelta(days=1)
    
    return planning_data
