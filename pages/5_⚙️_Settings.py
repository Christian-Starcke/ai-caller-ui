"""
Settings Page - Configuration and preferences
"""
import streamlit as st
from utils.config import Config
from utils.api_client import get_api_client

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ Settings")
st.markdown("---")

# Initialize API client
api_client = get_api_client()

# API Configuration Section
st.subheader("🔌 API Configuration")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"**n8n Webhook Base URL:**")
    st.code(Config.N8N_WEBHOOK_BASE_URL, language=None)

with col2:
    st.markdown("**Connection Status**")
    # Test API connection
    if st.button("Test Connection", type="primary", use_container_width=True):
        try:
            # Try to fetch campaigns as a connection test
            with st.spinner("Testing connection..."):
                result = api_client.get_campaigns(include_stats=False)
            
            if result:
                st.success("✅ Connected successfully!")
                st.balloons()
            else:
                st.warning("⚠️ Connection successful but no data returned")
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")

st.markdown("---")

# Application Settings Section
st.subheader("⚙️ Application Settings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Current Configuration:**")
    st.json({
        "Cache TTL (minutes)": Config.CACHE_TTL_MINUTES,
        "Items per page": Config.ITEMS_PER_PAGE,
        "API Timeout (seconds)": Config.API_TIMEOUT_SECONDS,
        "API Retry Attempts": Config.API_RETRY_ATTEMPTS,
        "Server Port": Config.STREAMLIT_SERVER_PORT,
        "Server Address": Config.STREAMLIT_SERVER_ADDRESS
    })

with col2:
    st.info("""
    **Note:** Configuration is managed via environment variables.
    
    To change settings:
    1. Update your `.env` file (local development)
    2. Update Railway environment variables (production)
    3. Restart the application
    """)

st.markdown("---")

# System Information Section
st.subheader("ℹ️ System Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Application Info:**")
    st.markdown("- **Application:** AI-Caller Streamlit UI")
    st.markdown("- **Version:** 1.0.0")
    st.markdown("- **Framework:** Streamlit")
    
with col2:
    st.markdown("**API Endpoints:**")
    st.markdown("- `GET /api/get-campaigns`")
    st.markdown("- `GET /api/leads`")
    st.markdown("- `POST /api/create-lead`")
    st.markdown("- `POST /api/leads` (update)")
    st.markdown("- `GET /api/stats-v2`")
    st.markdown("- `POST /api/csv-upload`")

st.markdown("---")

# About Section
st.subheader("📖 About")

st.markdown("""
**AI-Caller** is a modern platform for managing AI-powered calling campaigns.

**Features:**
- 📊 Real-time dashboard and analytics
- 👥 Comprehensive lead management
- 📞 Call history and tracking
- 📈 Campaign performance monitoring
- 📤 Bulk CSV uploads

**Built with:**
- Streamlit for the web interface
- n8n for workflow automation
- Retell AI for voice AI calls
- Supabase for data storage
""")

