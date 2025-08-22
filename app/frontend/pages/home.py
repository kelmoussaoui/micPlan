# app/frontend/pages/home.py
# Home page for micPlan

import streamlit as st
from app.frontend.utils import show_footer, add_bottom_spacing

def run():
    show_footer()
    st.set_page_config(page_title="micPlan", layout="wide")
    first_name = st.session_state.get("name", "User").split()[0]
    
    # Page header avec style moderne
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
            <h2 style='margin: 0; font-weight: bold;'>Welcome back, {first_name}!</h2>
        </div>
        """, unsafe_allow_html=True)

    # Placeholder for home image
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #e0effd 0%, #fff5e8 100%);
            padding: 4rem 2rem;
            border-radius: 12px;
            border-left: 5px solid #2994f2;
            border-right: 5px solid #fbbf5d;
            margin-bottom: 2rem;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        ">
            <h2 style='margin: 0; font-weight: bold; color: #1f77b4;'>🧬 micPlan</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='
        font-size: 1.6rem;
        line-height: 1.5;
        font-family: "Segoe UI", sans-serif;
        background-color: #f9f9f9;
        padding: 2rem 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        width: 100%;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
        text-align: center;
        color: #333;
    '>
        🧬 <strong>micPlan</strong> is your comprehensive platform for microbial genomics planning and analysis.<br><br>
        <span style='
            font-size: 1.3rem;
            font-style: italic;
            color: #555;
        '>
            Streamline your research workflows with intuitive tools for experimental design, sample management, and data analysis — from project conception to publication-ready results.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns(2, border=True)
    
    with col1:
        st.markdown("### 🚀 Getting Started")
        st.markdown("""
        - 📋 **Project Planning**: Design your research workflows
        - 🧫 **Sample Management**: Organize and track your samples
        - 📊 **Data Analysis**: Process and analyze your genomic data
        - 📈 **Reporting**: Generate comprehensive reports
        """)
        
        if st.button("🚀 Start New Project", use_container_width=True, type="primary"):
            st.info("🚀 New project functionality coming soon...")
    
    with col2:
        st.markdown("### 📚 Need Help?")
        st.markdown(f"""
            - 📄 Documentation (coming soon)  
            - 📧 Contact: `kelmoussaoui@chuliege.be`  
            - ⚙️ Version: `v1.0.0`
            """)
        
        if st.button("📖 View Documentation", use_container_width=True, type="secondary"):
            st.info("📖 Documentation coming soon...")
    
    # System Status
    st.subheader("📊 System Status", divider="rainbow")
    
    col_status1, col_status2, col_status3, col_status4 = st.columns(4)
    
    with col_status1:
        st.metric("System Status", "Online", "✅")
    
    with col_status2:
        st.metric("Active Users", "1", "You")
    
    with col_status3:
        st.metric("Projects", "0", "None yet")
    
    with col_status4:
        st.metric("Last Update", "Today", "v1.0.0")
    
    # Recent Activity
    st.subheader("🕦 Recent Activity", divider="rainbow")
    
    st.info("""
        **Welcome to micPlan!** 
        
        This is a new installation. As you use the system, your recent activities will appear here.
        
        - ✅ System initialized successfully
        - 🔐 Authentication system active
        - 🧬 Ready for your first project
    """)
    
    # Add bottom spacing
    add_bottom_spacing()
