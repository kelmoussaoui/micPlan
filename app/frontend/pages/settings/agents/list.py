# app/frontend/pages/settings/agents/list.py
# Affichage de la liste des agents

import streamlit as st

def show_agents_list():
    """Show agents list and management interface"""
    agent_database = st.session_state.agent_database
    
    # Section pour ajouter un nouvel agent
    st.markdown("### ➕ Ajouter un nouvel agent")
    
    col_add, col_mid, col_right = st.columns([1, 4, 1])
    with col_add:
        if st.button("➕ Nouvel agent", use_container_width=True, key="add_new_agent"):
            st.session_state["current_config_page"] = "new_agent"
            st.rerun()
    
    st.markdown("---")
    
    # Section pour afficher et modifier les agents existants
    st.markdown("### 📋 Liste des agents configurés")
    
    if not agent_database:
        st.info("Aucun agent configuré. Veuillez ajouter des agents.")
    else:
        # Préparer les données pour le dataframe
        agents_data = []
        selected_sector = st.session_state.get("selected_sector")
        
        for agent_name, agent_info in agent_database.items():
            # Filtrer par secteur si un secteur est sélectionné (sauf pour "Service" qui voit tout)
            if selected_sector and selected_sector != "Service" and agent_info.get("secteur") != selected_sector:
                continue
                
            # Extraire prénom et nom depuis le nom complet
            name_parts = agent_name.split(" ", 1)
            firstname = name_parts[0] if len(name_parts) > 0 else ""
            lastname = name_parts[1] if len(name_parts) > 1 else ""
            
            agents_data.append({
                "Prénom": firstname,
                "Nom": lastname,
                "Matricule": agent_info.get("matricule", ""),
                "Secteur": agent_info.get("secteur", "Non défini")
            })
        
        if agents_data:
            df = st.dataframe(
                agents_data,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key="agents_table",
                column_config={
                    "Prénom": st.column_config.TextColumn(
                        "Prénom",
                        help="Prénom de l'agent",
                        width="medium"
                    ),
                    "Nom": st.column_config.TextColumn(
                        "Nom",
                        help="Nom de famille de l'agent",
                        width="medium"
                    ),
                    "Matricule": st.column_config.TextColumn(
                        "Matricule",
                        help="Numéro de matricule unique de l'agent",
                        width="medium"
                    ),
                    "Secteur": st.column_config.TextColumn(
                        "Secteur",
                        help="Secteur d'activité de l'agent",
                        width="medium"
                    )
                }
            )
            
            # Check if a row is selected
            if df is not None and hasattr(df, 'selection') and df.selection:
                selected_rows = df.selection.get("rows", [])
                if selected_rows:
                    selected_row_index = selected_rows[0]
                    selected_firstname = agents_data[selected_row_index]["Prénom"]
                    selected_lastname = agents_data[selected_row_index]["Nom"]
                    selected_agent_name = f"{selected_firstname} {selected_lastname}".strip()
                    
                    # Button to modify selected agent
                    col_modify, col_mid, col_right = st.columns([1, 4, 1])
                    with col_modify:
                        if st.button("✏️ Modifier fiche agent", use_container_width=True, key="modify_agent"):
                            st.session_state["selected_agent_to_modify"] = selected_agent_name
                            st.session_state["current_config_page"] = "agent_detail"
                            st.rerun()
    
    # Divider and back button
    st.divider()
    
    # Bouton retour
    col_back, col_mid, col_right = st.columns([1, 4, 1])
    with col_back:
        if st.button("⬅️ Back", key="back_to_main_config", use_container_width=True):
            st.session_state["current_config_page"] = None
            st.rerun()
    
    # Ajouter de l'espace en bas de page
    from app.frontend.utils import add_bottom_spacing
    add_bottom_spacing()
