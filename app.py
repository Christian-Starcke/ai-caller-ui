"""
AI-Caller - Simple Streamlit UI
"""
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI-Caller",
    page_icon="📞",
    layout="wide"
)

# Get API URL from environment
N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_BASE_URL",
    "https://primary-production-10917.up.railway.app/webhook"
)

# Main title
st.title("📞 AI-Caller Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Leads", "Calls", "Settings"]
)

# Dashboard Page
if page == "Dashboard":
    st.header("📊 Dashboard")
    
    # API Status
    st.subheader("System Status")
    try:
        # Simple health check
        response = requests.get(f"{N8N_WEBHOOK_URL}/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.warning("⚠️ API Response: " + str(response.status_code))
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
    
    st.markdown("---")
    
    # Stats Section
    st.subheader("Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Leads", "0")
    with col2:
        st.metric("Active Calls", "0")
    with col3:
        st.metric("Success Rate", "0%")
    with col4:
        st.metric("Total Campaigns", "0")
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.info("Data refreshed!")
    
    with col2:
        if st.button("📊 View Reports", use_container_width=True):
            st.info("Reports coming soon!")
    
    with col3:
        if st.button("➕ New Campaign", use_container_width=True):
            st.info("New campaign feature coming soon!")

# Leads Page
elif page == "Leads":
    st.header("👥 Leads Management")
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search leads", placeholder="Enter name, phone, or email...")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Active", "Completed", "Pending"])
    
    st.markdown("---")
    
    # Leads table placeholder
    st.subheader("Leads List")
    st.info("📋 Leads data will appear here. Connect to your n8n workflow to load data.")
    
    # Example data
    if st.checkbox("Show example data"):
        import pandas as pd
        example_data = pd.DataFrame({
            "Name": ["John Doe", "Jane Smith", "Bob Johnson"],
            "Phone": ["+1234567890", "+1234567891", "+1234567892"],
            "Status": ["Active", "Pending", "Completed"],
            "Campaign": ["Campaign A", "Campaign B", "Campaign A"]
        })
        st.dataframe(example_data, use_container_width=True)

# Calls Page
elif page == "Calls":
    st.header("📞 Call History")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        date_from = st.date_input("From Date")
    with col2:
        date_to = st.date_input("To Date")
    with col3:
        call_status = st.selectbox("Call Status", ["All", "Answered", "No Answer", "Busy"])
    
    st.markdown("---")
    
    # Calls list placeholder
    st.subheader("Recent Calls")
    st.info("📋 Call history will appear here. Connect to your n8n workflow to load data.")
    
    # Example data
    if st.checkbox("Show example calls"):
        import pandas as pd
        example_calls = pd.DataFrame({
            "Date": ["2024-01-15", "2024-01-14", "2024-01-13"],
            "Phone": ["+1234567890", "+1234567891", "+1234567892"],
            "Duration": ["2:30", "1:45", "0:00"],
            "Status": ["Answered", "No Answer", "Busy"],
            "Disposition": ["Interested", "Not Interested", "No Answer"]
        })
        st.dataframe(example_calls, use_container_width=True)

# Settings Page
elif page == "Settings":
    st.header("⚙️ Settings")
    
    st.subheader("API Configuration")
    api_url = st.text_input(
        "N8N Webhook URL",
        value=N8N_WEBHOOK_URL,
        help="Enter your n8n webhook base URL"
    )
    
    if st.button("💾 Save Settings"):
        st.success("Settings saved! (Note: This is a demo - settings are not persisted)")
    
    st.markdown("---")
    
    st.subheader("About")
    st.info("""
    **AI-Caller v2.0**
    
    A simple Streamlit interface for managing AI-powered calling campaigns.
    
    **Features:**
    - Dashboard overview
    - Leads management
    - Call history
    - Settings configuration
    
    Connect to your n8n workflows to enable full functionality.
    """)

# Footer
st.markdown("---")
st.caption("AI-Caller Dashboard | Powered by Streamlit & n8n")
