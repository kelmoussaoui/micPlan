# app/frontend/pages/planning.py
# Planning page for micPlan

import streamlit as st
from app.frontend.utils import show_footer, add_bottom_spacing
import pandas as pd
import datetime
from datetime import date, timedelta

def run():
    show_footer()
    st.set_page_config(page_title="Planning - micPlan", layout="wide")
    
    # Get current date
    today = date.today()
    
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
            <h2 style='margin: 0; font-weight: bold;'>📅 Planning - Filtrage par dates</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Date range selector
    st.markdown("### 📅 Sélection de la période")
    
    col_date1, col_date2, col_week = st.columns([1, 1, 1])
    
    with col_date1:
        # Initialize start_date from session state or default
        if "start_date" not in st.session_state:
            st.session_state.start_date = today - timedelta(days=7)
        
        start_date = st.date_input(
            "📅 Date de début",
            value=st.session_state.start_date,
            format="DD/MM/YYYY",
            key="start_date_input"
        )
        # Update session state when user changes the date
        if start_date != st.session_state.start_date:
            st.session_state.start_date = start_date
    
    with col_date2:
        # Initialize end_date from session state or default
        if "end_date" not in st.session_state:
            st.session_state.end_date = today + timedelta(days=7)
        
        end_date = st.date_input(
            "📅 Date de fin",
            value=st.session_state.end_date,
            format="DD/MM/YYYY",
            key="end_date_input"
        )
        # Update session state when user changes the date
        if end_date != st.session_state.end_date:
            st.session_state.end_date = end_date
    
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
    
    # Auto-switch to compact view for periods > 7 days
    if period_days > 7:
        view_mode = "🎨 Vue compacte (icônes)"
        st.info("🔄 **Mode compact automatique** : Plus de 7 jours détectés - Affichage optimisé avec icônes")
    else:
        view_mode = "📝 Vue détaillée (texte)"
        st.info("📝 **Mode détaillé** : 7 jours ou moins - Affichage complet avec descriptions")
    
    # Quick week navigation buttons
    st.markdown("**🔍 Navigation rapide**")
    col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns(5)
    
    with col_nav1:
        if st.button("📅 Semaine précédente", use_container_width=True, key="prev_week"):
            # Calculate previous week
            current_week_start = today - timedelta(days=today.weekday())
            start_date = current_week_start - timedelta(days=7)
            end_date = start_date + timedelta(days=6)
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.rerun()
    
    with col_nav2:
        if st.button("📅 Semaine actuelle", use_container_width=True, key="current_week"):
            # Calculate current week
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.rerun()
    
    with col_nav3:
        if st.button("📅 Semaine prochaine", use_container_width=True, key="next_week"):
            # Calculate next week
            current_week_start = today - timedelta(days=today.weekday())
            start_date = current_week_start + timedelta(days=7)
            end_date = start_date + timedelta(days=6)
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.rerun()
    
    with col_nav4:
        if st.button("📅 Mois actuel", use_container_width=True, key="current_month"):
            # Calculate current month
            start_date = date(today.year, today.month, 1)
            if today.month == 12:
                end_date = date(today.year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(today.year, today.month + 1, 1) - timedelta(days=1)
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.rerun()
    
    with col_nav5:
        if st.button("📅 Mois suivant", use_container_width=True, key="next_month"):
            # Calculate next month
            if today.month == 12:
                start_date = date(today.year + 1, 1, 1)
                end_date = date(today.year + 1, 2, 1) - timedelta(days=1)
            else:
                start_date = date(today.year, today.month + 1, 1)
                if today.month + 1 == 12:
                    end_date = date(today.year + 1, 1, 1) - timedelta(days=1)
                else:
                    end_date = date(today.year, today.month + 2, 1) - timedelta(days=1)
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.rerun()
    
    # Generate dates between selected range
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Real technicians from the team
    technician_options = [
        "Melissa",
        "Laetitia", 
        "Michaël",
        "Olivier",
        "Patrick",
        "Caroline",
        "Fabrice",
        "Giuseppina"
    ]
    
    # Define the 9 possible positions
    positions = [
        "P1 : Tri & urgences",
        "P2 : Extraction", 
        "P3 : PCR & détection",
        "P4 : Génotypage HCV",
        "P5 : NGS HIV",
        "P6 : Alinity",
        "P7 : C6800",
        "P8 : QC & maintenances",
        "P9 : Mycoses"
    ]
    
    # Define the 5 possible schedules
    schedules = [
        "8h00-16h00",
        "8h30-16h30", 
        "9h00-17h00",
        "9h30-17h30",
        "10h00-18h00"
    ]
    
    # Agent database with rules and constraints
    agent_database = {
        "Melissa": {
            "unavailable_days": ["Monday"],  # Never available on Monday
            "preferred_positions": ["P1", "P2", "P3"],  # Prefers front-end positions
            "max_weekdays_per_week": 4,  # Maximum 4 weekdays per week
            "specialization": "Front-end processing"
        },
        "Laetitia": {
            "unavailable_days": [],
            "preferred_positions": ["P4", "P5", "P6"],  # Prefers molecular biology
            "max_weekdays_per_week": 5,
            "specialization": "Molecular biology"
        },
        "Michaël": {
            "unavailable_days": [],
            "preferred_positions": ["P7", "P8"],  # Prefers equipment and QC
            "max_weekdays_per_week": 5,
            "specialization": "Equipment and QC"
        },
        "Olivier": {
            "unavailable_days": [],
            "preferred_positions": ["P1", "P2", "P8"],  # Flexible, can do multiple types
            "max_weekdays_per_week": 5,
            "specialization": "Generalist"
        },
        "Patrick": {
            "unavailable_days": [],
            "preferred_positions": ["P3", "P4", "P5"],  # Prefers molecular biology
            "max_weekdays_per_week": 5,
            "specialization": "Molecular biology"
        },
        "Caroline": {
            "unavailable_days": [],
            "preferred_positions": ["P9"],  # ONLY position 9 (Mycoses)
            "max_weekdays_per_week": 5,
            "specialization": "Mycoses specialist"
        },
        "Fabrice": {
            "unavailable_days": ["Friday"],  # Never available on Friday
            "preferred_positions": ["P6", "P7"],  # Prefers equipment positions
            "max_weekdays_per_week": 4,
            "specialization": "Equipment specialist"
        },
        "Giuseppina": {
            "unavailable_days": [],
            "preferred_positions": ["P1", "P2", "P3"],  # Prefers front-end
            "max_weekdays_per_week": 5,
            "specialization": "Front-end processing"
        }
    }
    
    # Position constraints and rules
    position_rules = {
        "P1 : Tri & urgences": {
            "min_agents_per_day": 1,
            "max_agents_per_day": 1,
            "priority": "High",  # Critical position
            "required_skills": ["Front-end processing"]
        },
        "P2 : Extraction": {
            "min_agents_per_day": 1,
            "max_agents_per_day": 2,
            "priority": "High",
            "required_skills": ["Front-end processing"]
        },
        "P3 : PCR & détection": {
            "min_agents_per_day": 1,
            "max_agents_per_day": 1,
            "priority": "High",
            "required_skills": ["Molecular biology"]
        },
        "P4 : Génotypage HCV": {
            "min_agents_per_day": 1,
            "max_agents_per_day": 1,
            "priority": "Medium",
            "required_skills": ["Molecular biology"]
        },
        "P5 : NGS HIV": {
            "min_agents_per_day": 1,
            "max_agents_per_day": 1,
            "priority": "Medium",
            "required_skills": ["Molecular biology"]
        },
        "P6 : Alinity": {
            "min_agents_per_day": 1,
            "max_agents_per_day": 1,
            "priority": "Medium",
            "required_skills": ["Equipment specialist"]
        },
        "P7 : C6800": {
            "min_agents_per_day": 1,
            "max_agents_per_day": 1,
            "priority": "Medium",
            "required_skills": ["Equipment specialist"]
        },
        "P8 : QC & maintenances": {
            "min_agents_per_day": 1,
            "max_agents_per_day": 1,
            "priority": "Low",
            "required_skills": ["Equipment and QC", "Generalist"]
        },
        "P9 : Mycoses": {
            "min_agents_per_day": 1,
            "max_agents_per_day": 1,
            "priority": "Low",
            "required_skills": ["Mycoses specialist"],  # Only Caroline
            "exclusive_agent": "Caroline"  # This position is exclusive to Caroline
        }
    }
    
    # Create multi-level column headers
    columns = [("Technicien", "")]
    
    # Add date columns with multi-level headers
    for day_date in dates:
        # French day names - full and abbreviated
        french_days_full = {
            'Mon': 'Lundi', 'Tue': 'Mardi', 'Wed': 'Mercredi', 'Thu': 'Jeudi',
            'Fri': 'Vendredi', 'Sat': 'Samedi', 'Sun': 'Dimanche'
        }
        
        french_days_abbr = {
            'Mon': 'Lu', 'Tue': 'Ma', 'Wed': 'Me', 'Thu': 'Je',
            'Fri': 'Ve', 'Sat': 'Sa', 'Sun': 'Di'
        }
        
        day_name_en = day_date.strftime("%a")  # English abbreviated day name
        day_name_fr_full = french_days_full.get(day_name_en, day_name_en)
        day_name_fr_abbr = french_days_abbr.get(day_name_en, day_name_en)
        date_str = day_date.strftime('%d/%m')
        
        # Create multi-level column: (Day, Date) - use abbreviated in compact mode
        if period_days > 7:
            columns.append((day_name_fr_abbr, date_str))  # Compact: 2 letters
        else:
            columns.append((day_name_fr_full, date_str))  # Detailed: full names
    
    # Create sample data for the dataframe
    data = {}
    
    # Force clean session state for technicians to avoid old values
    if "selected_technicians" in st.session_state:
        # Check if there are any old format values and clean them
        old_values = [val for val in st.session_state.selected_technicians if "🔬" in str(val) or "PCR" in str(val) or "(" in str(val)]
        if old_values:
            st.session_state.selected_technicians = technician_options.copy()
    
    # Initialize selected technicians in session state (must be done before using them)
    if "selected_technicians" not in st.session_state:
        st.session_state.selected_technicians = technician_options
    
    # Handle select all/deselect all clicks
    if st.session_state.get("select_all_clicked", False):
        st.session_state.selected_technicians = technician_options.copy()
        st.session_state.select_all_clicked = False
    
    if st.session_state.get("deselect_all_clicked", False):
        st.session_state.selected_technicians = []
        st.session_state.deselect_all_clicked = False
    
    # Safety check: ensure default values are valid
    safe_default = []
    for tech in st.session_state.selected_technicians:
        if tech in technician_options:
            safe_default.append(tech)
    
    # If no safe defaults, use first technician
    if not safe_default:
        safe_default = ["Melissa"]
    
    # Multiselect for technicians
    selected_technicians = st.multiselect(
        "Sélectionner les techniciens à afficher :",
        options=technician_options,
        default=safe_default,
        key="technician_multiselect"
    )
    
    # Update session state with current selection
    st.session_state.selected_technicians = selected_technicians
    
    # Ensure selected_technicians is never empty
    if not selected_technicians:
        selected_technicians = ["Melissa"]  # Default to at least one technician
    
    # Extract technician names from selected options (now they are just names)
    filtered_technicians = selected_technicians.copy()
    
    # Function to automatically assign positions based on rules
    def auto_assign_positions(start_date, end_date, selected_technicians):
        """Automatically assign positions based on agent rules and constraints"""
        from datetime import timedelta
        
        # Clear existing assignments for the period
        current_date = start_date
        while current_date <= end_date:
            for tech in selected_technicians:
                day_key = f"{tech}_{current_date.strftime('%Y-%m-%d')}"
                if day_key in st.session_state:
                    del st.session_state[day_key]
            current_date += timedelta(days=1)
        
        # Reset to start date
        current_date = start_date
        
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Weekdays only
                day_name = current_date.strftime("%A")
                
                # Get available agents for this day
                available_agents = []
                for tech in selected_technicians:
                    agent_info = agent_database.get(tech, {})
                    unavailable_days = agent_info.get("unavailable_days", [])
                    
                    # Check if agent is available on this day
                    if day_name not in unavailable_days:
                        # Check if agent hasn't exceeded weekly limit
                        week_start = current_date - timedelta(days=current_date.weekday())
                        week_end = week_start + timedelta(days=4)
                        
                        weekly_assignments = 0
                        check_date = week_start
                        while check_date <= week_end:
                            check_key = f"{tech}_{check_date.strftime('%Y-%m-%d')}"
                            if check_key in st.session_state and st.session_state[check_key]:
                                weekly_assignments += 1
                            check_date += timedelta(days=1)
                        
                        max_weekdays = agent_info.get("max_weekdays_per_week", 5)
                        if weekly_assignments < max_weekdays:
                            available_agents.append(tech)
                
                # Assign positions by priority
                priority_order = ["High", "Medium", "Low"]
                
                for priority in priority_order:
                    for position in positions:
                        if position_rules[position]["priority"] == priority:
                            # Check if position needs assignment
                            position_assigned = False
                            
                            # Check for exclusive agents first
                            if "exclusive_agent" in position_rules[position]:
                                exclusive_agent = position_rules[position]["exclusive_agent"]
                                if exclusive_agent in available_agents:
                                    # Assign exclusive agent to this position
                                    day_key = f"{exclusive_agent}_{current_date.strftime('%Y-%m-%d')}"
                                    st.session_state[day_key] = position
                                    available_agents.remove(exclusive_agent)
                                    position_assigned = True
                                    continue
                            
                            # Regular assignment based on skills and preferences
                            if not position_assigned:
                                required_skills = position_rules[position]["required_skills"]
                                
                                # Find best matching agent
                                best_agent = None
                                best_score = -1
                                
                                for agent in available_agents:
                                    agent_info = agent_database.get(agent, {})
                                    agent_specialization = agent_info.get("specialization", "")
                                    preferred_positions = agent_info.get("preferred_positions", [])
                                    
                                    # Calculate compatibility score
                                    score = 0
                                    
                                    # Skill match
                                    if agent_specialization in required_skills:
                                        score += 10
                                    
                                    # Position preference
                                    position_code = position.split(":")[0]
                                    if position_code in preferred_positions:
                                        score += 5
                                    
                                    # Availability (lower weekly count = higher priority)
                                    week_start = current_date - timedelta(days=current_date.weekday())
                                    week_end = week_start + timedelta(days=4)
                                    
                                    weekly_assignments = 0
                                    check_date = week_start
                                    while check_date <= week_end:
                                        check_key = f"{agent}_{check_date.strftime('%Y-%m-%d')}"
                                        if check_key in st.session_state and st.session_state[check_key]:
                                            weekly_assignments += 1
                                        check_date += timedelta(days=1)
                                    
                                    # Prefer agents with fewer weekly assignments
                                    score += (5 - weekly_assignments)
                                    
                                    if score > best_score:
                                        best_score = score
                                        best_agent = agent
                                
                                # Assign position to best agent
                                if best_agent and best_score > 0:
                                    day_key = f"{best_agent}_{current_date.strftime('%Y-%m-%d')}"
                                    st.session_state[day_key] = position
                                    available_agents.remove(best_agent)
            
            current_date += timedelta(days=1)
        
        return True
    
    # Add auto-assignment button
    st.markdown("### 🤖 Affectation automatique des postes")
    
    col_auto1, col_auto2 = st.columns(2)
    
    with col_auto1:
        if st.button("🚀 Affectation automatique", use_container_width=True, key="auto_assign"):
            success = auto_assign_positions(start_date, end_date, filtered_technicians)
            if success:
                st.success("✅ Affectation automatique terminée !")
                st.rerun()
    
    with col_auto2:
        if st.button("🗑️ Effacer toutes les affectations", use_container_width=True, key="clear_all"):
            # Clear all assignments for the period
            current_date = start_date
            while current_date <= end_date:
                for tech in filtered_technicians:
                    day_key = f"{tech}_{current_date.strftime('%Y-%m-%d')}"
                    if day_key in st.session_state:
                        del st.session_state[day_key]
                current_date += timedelta(days=1)
            st.success("🗑️ Toutes les affectations ont été effacées !")
            st.rerun()
    
    # Add auto-assignment for schedules
    st.markdown("### ⏰ Affectation automatique des horaires")
    
    col_schedule1, col_schedule2 = st.columns(2)
    
    with col_schedule1:
        if st.button("⏰ Affectation horaires automatique", use_container_width=True, key="auto_schedule"):
            # Simple auto-assignment of schedules
            current_date = start_date
            while current_date <= end_date:
                if current_date.weekday() < 5:  # Weekdays only
                    # Assign schedules in rotation to available agents
                    available_agents = []
                    for tech in filtered_technicians:
                        agent_info = agent_database.get(tech, {})
                        unavailable_days = agent_info.get("unavailable_days", [])
                        day_name = current_date.strftime("%A")
                        
                        if day_name not in unavailable_days:
                            available_agents.append(tech)
                    
                    # Assign schedules in rotation
                    for i, tech in enumerate(available_agents):
                        schedule_index = i % len(schedules)
                        day_key = f"{tech}_{current_date.strftime('%Y-%m-%d')}_schedule"
                        st.session_state[day_key] = schedules[schedule_index]
                
                current_date += timedelta(days=1)
            
            st.success("⏰ Affectation des horaires terminée !")
            st.rerun()
    
    with col_schedule2:
        if st.button("🗑️ Effacer tous les horaires", use_container_width=True, key="clear_schedules"):
            # Clear all schedule assignments for the period
            current_date = start_date
            while current_date <= end_date:
                for tech in filtered_technicians:
                    day_key = f"{tech}_{current_date.strftime('%Y-%m-%d')}_schedule"
                    if day_key in st.session_state:
                        del st.session_state[day_key]
                current_date += timedelta(days=1)
            st.success("🗑️ Tous les horaires ont été effacés !")
            st.rerun()
    
    st.markdown("---")
    
    # Create tabs for the planning dataframe
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Horaire", "Postes AM", "Postes PM"])
    
    # Tab 1 - Horaire
    with tab1:
        # Create the planning dataframe for schedules
        planning_data = {}
        
        # Add technician names as first column
        planning_data["Agents"] = filtered_technicians
        
        # Add columns for each day
        for day_date in dates:
            french_days = {
                'Mon': 'Lundi', 'Tue': 'Mardi', 'Wed': 'Mercredi', 'Thu': 'Jeudi',
                'Fri': 'Vendredi', 'Sat': 'Samedi', 'Sun': 'Dimanche'
            }
            day_name_en = day_date.strftime("%a")
            day_name_fr = french_days.get(day_name_en, day_name_en)
            date_str = day_date.strftime('%d/%m')
            
            # Create the exact column name that matches the dataframe
            if period_days > 7:  # Compact view - use abbreviated names
                day_name_fr = french_days.get(day_name_en, day_name_en)[:2]  # First 2 letters
                column_name = f"{day_name_fr} {date_str}"
            else:  # Detailed view - use full names with date
                day_name_fr = french_days.get(day_name_en, day_name_en)
                column_name = f"{day_name_fr} {date_str}"
            
            # Initialize activities for each technician
            activities = []
            
            for tech in filtered_technicians:
                if day_date.weekday() < 5:  # Weekdays
                    # Get assigned schedule for this technician for this specific day
                    day_key = f"{tech}_{day_date.strftime('%Y-%m-%d')}_schedule"
                    assigned_schedule = st.session_state.get(day_key, "")
                    
                    if assigned_schedule:
                        activities.append(assigned_schedule)
                    else:
                        activities.append("")  # No schedule assigned yet
                else:  # Weekends
                    activities.append("🏖️")  # Weekend indicator
            
            planning_data[column_name] = activities
        
        # Create DataFrame
        planning_df = pd.DataFrame(planning_data)
        
        # Create column configuration for editable selectbox columns (schedules)
        column_config = {}
        
        # Configure technician column (read-only)
        column_config["Agents"] = st.column_config.TextColumn(
            "👨‍⚕️ Agents",
            help="Nom de l'agent",
            width="medium",
            disabled=True
        )
        
        # Configure date columns with selectbox for schedule assignment
        for day_date in dates:
            french_days = {
                'Mon': 'Lundi', 'Tue': 'Mardi', 'Wed': 'Mercredi', 'Thu': 'Jeudi',
                'Fri': 'Vendredi', 'Sat': 'Samedi', 'Sun': 'Dimanche'
            }
            day_name_en = day_date.strftime("%a")
            day_name_fr = french_days.get(day_name_en, day_name_en)
            date_str = day_date.strftime('%d/%m')
            
            # Create the exact column name that matches the dataframe
            if period_days > 7:  # Compact view - use abbreviated names
                day_name_fr = french_days.get(day_name_en, day_name_en)[:2]  # First 2 letters
                column_name = f"{day_name_fr} {date_str}"
            else:  # Detailed view - use full names with date
                day_name_fr = french_days.get(day_name_en, day_name_en)
                column_name = f"{day_name_fr} {date_str}"
            
            # Adjust column width based on period length
            if period_days > 7:  # Compact view - use narrow columns
                column_width = "small"
            else:  # Detailed view - use normal columns
                column_width = "medium"
            
            if day_date.weekday() < 5:  # Weekdays only
                # Configure editable column with dropdown for schedules
                column_config[column_name] = st.column_config.SelectboxColumn(
                    label=column_name,  # Use the full column name as label
                    help=f"Sélectionner l'horaire pour le {day_name_fr} {date_str}",
                    width=column_width,
                    options=[""] + schedules,  # Empty option + all schedules
                    required=False
                )
            else:  # Weekends
                # Configure read-only column for weekends
                column_config[column_name] = st.column_config.TextColumn(
                    label=f"🏖️ {column_name}",  # Add weekend icon to label
                    help=f"Activités pour le {day_name_fr} {date_str} (Weekend)",
                    width=column_width,
                    disabled=True,
                    max_chars=None
                )
        
        # Display the dataframe with editing capabilities
        edited_df = st.data_editor(
            planning_df,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config=column_config,
            key="schedule_dataframe_tab1"
        )
        
        # Handle schedule changes from the dataframe
        if edited_df is not None:
            # Check for changes and update session state
            changes_made = False
            
            for index, row in edited_df.iterrows():
                tech_name = row['Agents']
                
                for day_date in dates:
                    french_days = {
                        'Mon': 'Lundi', 'Tue': 'Mardi', 'Wed': 'Mercredi', 'Thu': 'Jeudi',
                        'Fri': 'Vendredi', 'Sat': 'Samedi', 'Sun': 'Dimanche'
                    }
                    day_name_en = day_date.strftime("%a")
                    day_name_fr = french_days.get(day_name_en, day_name_en)
                    date_str = day_date.strftime('%d/%m')
                    
                    # Create the exact column name that matches the dataframe
                    if period_days > 7:  # Compact view - use abbreviated names
                        day_name_fr = french_days.get(day_name_en, day_name_en)[:2]  # First 2 letters
                        column_name = f"{day_name_fr} {date_str}"
                    else:  # Detailed view - use full names with date
                        day_name_fr = french_days.get(day_name_en, day_name_en)
                        column_name = f"{day_name_fr} {date_str}"
                    
                    if day_date.weekday() < 5:  # Weekdays only
                        new_value = row.get(column_name, "")
                        if pd.notna(new_value) and new_value != "":
                            day_key = f"{tech_name}_{day_date.strftime('%Y-%m-%d')}_schedule"
                            old_value = st.session_state.get(day_key, "")
                            
                            if new_value != old_value:
                                st.session_state[day_key] = new_value
                                changes_made = True
            
            # Rerun if changes were made
            if changes_made:
                st.rerun()
    
    # Tab 2
    with tab2:
        # Duplicate the same dataframe for tab 2
        planning_data2 = {}
        planning_data2["Technicien"] = filtered_technicians
        
        for day_date in dates:
            french_days = {
                'Mon': 'Lundi', 'Tue': 'Mardi', 'Wed': 'Mercredi', 'Thu': 'Jeudi',
                'Fri': 'Vendredi', 'Sat': 'Samedi', 'Sun': 'Dimanche'
            }
            day_name_en = day_date.strftime("%a")
            day_name_fr = french_days.get(day_name_en, day_name_en)
            date_str = day_date.strftime('%d/%m')
            
            if period_days > 7:
                day_name_fr = french_days.get(day_name_en, day_name_en)[:2]
                column_name = f"{day_name_fr} {date_str}"
            else:
                day_name_fr = french_days.get(day_name_en, day_name_en)
                column_name = f"{day_name_fr} {date_str}"
            
            activities = []
            for tech in filtered_technicians:
                if day_date.weekday() < 5:
                    day_key = f"{tech}_{day_date.strftime('%Y-%m-%d')}"
                    assigned_position = st.session_state.get(day_key, "")
                    
                    if assigned_position:
                        if period_days > 7:
                            position_num = assigned_position.split(":")[0]
                            activities.append(position_num)
                        else:
                            activities.append(assigned_position)
                    else:
                        activities.append("")
                else:
                    activities.append("🏖️")
            
            planning_data2[column_name] = activities
        
        planning_df2 = pd.DataFrame(planning_data2)
        
        # Same column configuration for tab 2
        column_config2 = {}
        column_config2["Technicien"] = st.column_config.TextColumn(
            "👨‍⚕️ Technicien",
            help="Nom du technicien",
            width="medium",
            disabled=True
        )
        
        for day_date in dates:
            french_days = {
                'Mon': 'Lundi', 'Tue': 'Mardi', 'Wed': 'Mercredi', 'Thu': 'Jeudi',
                'Fri': 'Vendredi', 'Sat': 'Samedi', 'Sun': 'Dimanche'
            }
            day_name_en = day_date.strftime("%a")
            day_name_fr = french_days.get(day_name_en, day_name_en)
            date_str = day_date.strftime('%d/%m')
            
            if period_days > 7:
                day_name_fr = french_days.get(day_name_en, day_name_en)[:2]
                column_name = f"{day_name_fr} {date_str}"
            else:
                day_name_fr = french_days.get(day_name_en, day_name_en)
                column_name = f"{day_name_fr} {date_str}"
            
            if period_days > 7:
                column_width = "small"
            else:
                column_width = "medium"
            
            if day_date.weekday() < 5:
                column_config2[column_name] = st.column_config.SelectboxColumn(
                    label=column_name,
                    help=f"Sélectionner le poste pour le {day_name_fr} {date_str}",
                    width=column_width,
                    options=[""] + positions,
                    required=False
                )
            else:
                column_config2[column_name] = st.column_config.TextColumn(
                    label=f"🏖️ {column_name}",  # Add weekend icon to label
                    help=f"Activités pour le {day_name_fr} {date_str} (Weekend)",
                    width=column_width,
                    disabled=True,
                    max_chars=None
                )
        
        edited_df2 = st.data_editor(
            planning_df2,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config=column_config2,
            key="planning_dataframe_tab2"
        )
        
        # Handle changes for tab 2
        if edited_df2 is not None:
            changes_made = False
            for index, row in edited_df2.iterrows():
                tech_name = row['Technicien']
                for day_date in dates:
                    french_days = {
                        'Mon': 'Lundi', 'Tue': 'Mardi', 'Wed': 'Mercredi', 'Thu': 'Jeudi',
                        'Fri': 'Vendredi', 'Sat': 'Samedi', 'Sun': 'Dimanche'
                    }
                    day_name_en = day_date.strftime("%a")
                    day_name_fr = french_days.get(day_name_en, day_name_en)
                    date_str = day_date.strftime('%d/%m')
                    
                    if period_days > 7:
                        day_name_fr = french_days.get(day_name_en, day_name_en)[:2]
                        column_name = f"{day_name_fr} {date_str}"
                    else:
                        day_name_fr = french_days.get(day_name_en, day_name_en)
                        column_name = f"{day_name_fr} {date_str}"
                    
                    if day_date.weekday() < 5:
                        new_value = row.get(column_name, "")
                        if pd.notna(new_value) and new_value != "":
                            day_key = f"{tech_name}_{day_date.strftime('%Y-%m-%d')}"
                            old_value = st.session_state.get(day_key, "")
                            
                            if new_value != old_value:
                                st.session_state[day_key] = new_value
                                changes_made = True
            
            if changes_made:
                st.rerun()
    
    # Tab 3
    with tab3:
        # Duplicate the same dataframe for tab 3
        planning_data3 = {}
        planning_data3["Technicien"] = filtered_technicians
        
        for day_date in dates:
            french_days = {
                'Mon': 'Lundi', 'Tue': 'Mardi', 'Wed': 'Mercredi', 'Thu': 'Jeudi',
                'Fri': 'Vendredi', 'Sat': 'Samedi', 'Sun': 'Dimanche'
            }
            day_name_en = day_date.strftime("%a")
            day_name_fr = french_days.get(day_name_en, day_name_en)
            date_str = day_date.strftime('%d/%m')
            
            if period_days > 7:
                day_name_fr = french_days.get(day_name_en, day_name_en)[:2]
                column_name = f"{day_name_fr} {date_str}"
            else:
                day_name_fr = french_days.get(day_name_en, day_name_en)
                column_name = f"{day_name_fr} {date_str}"
            
            activities = []
            for tech in filtered_technicians:
                if day_date.weekday() < 5:
                    day_key = f"{tech}_{day_date.strftime('%Y-%m-%d')}"
                    assigned_position = st.session_state.get(day_key, "")
                    
                    if assigned_position:
                        if period_days > 7:
                            position_num = assigned_position.split(":")[0]
                            activities.append(position_num)
                        else:
                            activities.append(assigned_position)
                    else:
                        activities.append("")
                else:
                    activities.append("🏖️")
            
            planning_data3[column_name] = activities
        
        planning_df3 = pd.DataFrame(planning_data3)
        
        # Same column configuration for tab 3
        column_config3 = {}
        column_config3["Technicien"] = st.column_config.TextColumn(
            "👨‍⚕️ Technicien",
            help="Nom du technicien",
            width="medium",
            disabled=True
        )
        
        for day_date in dates:
            french_days = {
                'Mon': 'Lundi', 'Tue': 'Mardi', 'Wed': 'Mercredi', 'Thu': 'Jeudi',
                'Fri': 'Vendredi', 'Sat': 'Samedi', 'Sun': 'Dimanche'
            }
            day_name_en = day_date.strftime("%a")
            day_name_fr = french_days.get(day_name_en, day_name_en)
            date_str = day_date.strftime('%d/%m')
            
            if period_days > 7:
                day_name_fr = french_days.get(day_name_en, day_name_en)[:2]
                column_name = f"{day_name_fr} {date_str}"
            else:
                day_name_fr = french_days.get(day_name_en, day_name_en)
                column_name = f"{day_name_fr} {date_str}"
            
            if period_days > 7:
                column_width = "small"
            else:
                column_width = "medium"
            
            if day_date.weekday() < 5:
                column_config3[column_name] = st.column_config.SelectboxColumn(
                    label=column_name,
                    help=f"Sélectionner le poste pour le {day_name_fr} {date_str}",
                    width=column_width,
                    options=[""] + positions,
                    required=False
                )
            else:
                column_config3[column_name] = st.column_config.TextColumn(
                    label=f"🏖️ {column_name}",  # Add weekend icon to label
                    help=f"Activités pour le {day_name_fr} {date_str} (Weekend)",
                    width=column_width,
                    disabled=True,
                    max_chars=None
                )
        
        edited_df3 = st.data_editor(
            planning_df3,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config=column_config3,
            key="planning_dataframe_tab3"
        )
        
        # Handle changes for tab 3
        if edited_df3 is not None:
            changes_made = False
            for index, row in edited_df3.iterrows():
                tech_name = row['Technicien']
                for day_date in dates:
                    french_days = {
                        'Mon': 'Lundi', 'Tue': 'Mardi', 'Wed': 'Mercredi', 'Thu': 'Jeudi',
                        'Fri': 'Vendredi', 'Sat': 'Samedi', 'Sun': 'Dimanche'
                    }
                    day_name_en = day_date.strftime("%a")
                    day_name_fr = french_days.get(day_name_en, day_name_en)
                    date_str = day_date.strftime('%d/%m')
                    
                    if period_days > 7:
                        day_name_fr = french_days.get(day_name_en, day_name_en)[:2]
                        column_name = f"{day_name_fr} {date_str}"
                    else:
                        day_name_fr = french_days.get(day_name_en, day_name_en)
                        column_name = f"{day_name_fr} {date_str}"
                    
                    if day_date.weekday() < 5:
                        new_value = row.get(column_name, "")
                        if pd.notna(new_value) and new_value != "":
                            day_key = f"{tech_name}_{day_date.strftime('%Y-%m-%d')}"
                            old_value = st.session_state.get(day_key, "")
                            
                            if new_value != old_value:
                                st.session_state[day_key] = new_value
                                changes_made = True
            
            if changes_made:
                st.rerun()
    
    st.markdown("---")
    
    # Add some statistics below the table
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Nombre de techniciens", len(technician_options))
    
    with col2:
        st.metric("Jours dans la période", len(dates))
    
    with col3:
        working_days = len([d for d in dates if d.weekday() < 5])
        st.metric("Jours ouvrables", working_days)
    
    with col4:
        weekend_days = len([d for d in dates if d.weekday() >= 5])
        st.metric("Weekends", weekend_days)
    
    # Add bottom spacing
    add_bottom_spacing()
    
    # Divider and back button
    st.divider()
    
    # Bouton retour
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Back", key="back_planning", use_container_width=True):
            st.session_state['selected_page'] = '🏠 Accueil'
            st.rerun()
    
    # Ajouter de l'espace en bas de page
    add_bottom_spacing()
