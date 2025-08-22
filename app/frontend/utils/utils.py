# app/frontend/utils/utils.py
# Frontend utility functions

import streamlit as st

def show_footer():
    """Display the application footer"""
    st.markdown("""
        <div style="
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f0f2f6;
            border-top: 1px solid #e0e0e0;
            padding: 0.5rem;
            text-align: center;
            font-size: 0.8rem;
            color: #666;
            z-index: 1000;
        ">
            <div style="display: flex; justify-content: flex-end; align-items: center; width: 100%; padding-right: 1rem;">
                <div>© 2025 El Moussaoui Khalid – All rights reserved.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def add_bottom_spacing():
    """Add bottom spacing to prevent content from being hidden by footer"""
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

def show_success_message(message: str, icon: str = "✅"):
    """Display a styled success message"""
    st.markdown(f"""
        <div style="
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            color: #155724;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="font-size: 1.2rem;">{icon}</span>
            <span>{message}</span>
        </div>
    """, unsafe_allow_html=True)

def show_error_message(message: str, icon: str = "❌"):
    """Display a styled error message"""
    st.markdown(f"""
        <div style="
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            color: #721c24;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="font-size: 1.2rem;">{icon}</span>
            <span>{message}</span>
        </div>
    """, unsafe_allow_html=True)

def show_info_message(message: str, icon: str = "ℹ️"):
    """Display a styled info message"""
    st.markdown(f"""
        <div style="
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            color: #0c5460;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="font-size: 1.2rem;">{icon}</span>
            <span>{message}</span>
        </div>
    """, unsafe_allow_html=True)

def show_warning_message(message: str, icon: str = "⚠️"):
    """Display a styled warning message"""
    st.markdown(f"""
        <div style="
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            color: #856404;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="font-size: 1.2rem;">{icon}</span>
            <span>{message}</span>
        </div>
    """, unsafe_allow_html=True)

def create_card(title: str, content: str, icon: str = "📋", color: str = "#1f77b4"):
    """Create a styled card component"""
    st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid {color};
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 1rem;
            ">
                <span style="font-size: 1.5rem;">{icon}</span>
                <h3 style="margin: 0; color: {color}; font-weight: bold;">{title}</h3>
            </div>
            <div style="color: #333; line-height: 1.6;">
                {content}
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, subtitle: str = "", icon: str = "📊", color: str = "#1f77b4"):
    """Create a styled metric card"""
    st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid {color};
            text-align: center;
        ">
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 0.5rem;
            ">
                <span style="font-size: 1.5rem;">{icon}</span>
                <h4 style="margin: 0; color: {color}; font-weight: bold;">{title}</h4>
            </div>
            <div style="
                font-size: 2rem;
                font-weight: bold;
                color: #333;
                margin-bottom: 0.5rem;
            ">
                {value}
            </div>
            {f'<div style="color: #666; font-size: 0.9rem;">{subtitle}</div>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)
