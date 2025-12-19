"""
AI-Caller Streamlit UI - Main Application Entry Point
"""
import streamlit as st
from utils.styling import apply_theme, hide_streamlit_branding
from utils.charts import apply_professional_theme

# Page configuration
st.set_page_config(
    page_title="AI-Caller",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "AI-Caller - AI-Powered Calling Campaign Management"
    }
)

# Apply professional theme
apply_theme()
hide_streamlit_branding()
apply_professional_theme()  # Apply Plotly chart theme

# Main app header
st.title("📞 AI-Caller Dashboard")
st.markdown("---")

# Welcome message
st.markdown("""
### Welcome to AI-Caller

Manage your AI-powered calling campaigns, leads, and analytics from one place.

**Quick Navigation:**
- 📊 **Dashboard** - View stats and performance metrics
- 👥 **Leads** - Manage your leads and contacts
- 📞 **Calls** - View call history and analytics
- 📈 **Campaigns** - Monitor campaign performance
- ⚙️ **Settings** - Configure your preferences

Use the sidebar to navigate between pages.
""")

# Status indicator
st.sidebar.markdown("### System Status")
st.sidebar.success("✅ System Online")

# API connection test
try:
    from utils.api_client import get_api_client
    from utils.config import Config
    
    api_client = get_api_client()
    st.sidebar.info(f"🌐 API: {Config.N8N_WEBHOOK_BASE_URL}")
    st.sidebar.caption("Connected to n8n workflows")
except Exception as e:
    st.sidebar.error(f"⚠️ API Error: {str(e)}")

