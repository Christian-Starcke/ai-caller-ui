"""
Styling utilities for custom CSS injection and theme management.
"""
import streamlit as st
import os
from pathlib import Path


def load_css(file_path: str) -> None:
    """
    Load and inject custom CSS from file.
    
    Args:
        file_path: Path to CSS file
    """
    try:
        css_path = Path(__file__).parent.parent / file_path
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        else:
            st.warning(f"CSS file not found: {css_path}")
    except Exception as e:
        st.warning(f"Error loading CSS: {e}")


def apply_theme() -> None:
    """Apply professional theme by loading custom CSS."""
    # Try to load custom CSS if it exists
    css_file = "assets/style.css"
    load_css(css_file)
    
    # Apply basic theme if CSS file doesn't exist yet
    if not (Path(__file__).parent.parent / css_file).exists():
        apply_basic_theme()


def apply_basic_theme() -> None:
    """Apply basic professional theme using inline CSS."""
    st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Professional color scheme */
    :root {
        --primary: #2563eb;
        --primary-dark: #1e40af;
        --secondary: #64748b;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --background: #f8fafc;
        --surface: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border: #e2e8f0;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 6px;
        border: 1px solid var(--border);
    }
    
    /* Cards */
    .card {
        background: var(--surface);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)


def hide_streamlit_branding() -> None:
    """Hide Streamlit default branding elements."""
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
    """, unsafe_allow_html=True)

