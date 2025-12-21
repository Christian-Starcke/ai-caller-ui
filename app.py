"""
AI-Caller - Simple Streamlit UI
"""
import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
import base64
import io

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

# Helper function to make API calls
def api_call(endpoint, method="GET", params=None, json_data=None, files=None):
    """Make API call to n8n webhook"""
    try:
        url = f"{N8N_WEBHOOK_URL}/{endpoint.lstrip('/')}"
        if method == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method == "POST":
            if files:
                response = requests.post(url, data=json_data, files=files, timeout=60)
            else:
                response = requests.post(url, json=json_data, timeout=30)
        else:
            return None, "Unsupported method"
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return None, str(e)

# Main title
st.title("📞 AI-Caller Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Leads", "Calls", "Campaigns", "Settings"]
)

# Dashboard Page
if page == "Dashboard":
    st.header("📊 Dashboard")
    
    # API Status
    st.subheader("System Status")
    try:
        # Test API connection with stats endpoint
        data, error = api_call("api/stats-v2", params={"timeFrame": "last7days"})
        if error:
            st.error(f"❌ API Error: {error}")
        else:
            st.success("✅ API Connected")
    except Exception as e:
        st.error(f"❌ Connection Error: {str(e)}")
    
    st.markdown("---")
    
    # Time frame selector
    time_frame = st.selectbox(
        "Time Frame",
        ["today", "last7days", "last30days", "last90days", "thismonth", "lastmonth", "alltime"],
        index=1,
        key="dashboard_timeframe"
    )
    
    # Fetch stats
    with st.spinner("Loading statistics..."):
        stats_data, error = api_call("api/stats-v2", params={"timeFrame": time_frame})
    
    if error:
        st.error(f"Error loading stats: {error}")
    elif stats_data:
        
        # Stats Section
        st.subheader("Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        # Extract stats from actual API response structure
        total_calls = stats_data.get("totalCalls", 0)
        connections = stats_data.get("connections", 0)
        conversations = stats_data.get("conversations", 0)
        total_cost = stats_data.get("totalCost", 0)
        
        # Calculate answer rate as connections/totalCalls (as percentage)
        answer_rate = (connections / total_calls * 100) if total_calls > 0 else 0
        
        with col1:
            st.metric("Total Calls", f"{total_calls:,}")
        with col2:
            st.metric("Connections", f"{connections:,}")
        with col3:
            st.metric("Conversations", f"{conversations:,}")
        with col4:
            st.metric("Answer Rate", f"{answer_rate:.1f}%")
        
        st.markdown("---")
        
        # Campaign Breakdown
        if stats_data.get("campaignBreakdown"):
            st.subheader("Campaign Performance")
            campaign_data = stats_data["campaignBreakdown"]
            if campaign_data:
                df_campaigns = pd.DataFrame(campaign_data)
                st.dataframe(df_campaigns, use_container_width=True)
        
        # Recent Calls
        if stats_data.get("recentCalls"):
            st.subheader("Recent Calls")
            recent_calls = stats_data["recentCalls"]
            if recent_calls:
                df_recent = pd.DataFrame(recent_calls)
                st.dataframe(df_recent, use_container_width=True)
        
        # Daily Recap Section
        st.markdown("---")
        st.subheader("📅 Daily Recap")
        recap_date = st.date_input("Select Date", value=datetime.now().date(), key="recap_date")
        
        if st.button("Get Recap", key="get_recap"):
            with st.spinner("Loading recap..."):
                recap_data, error = api_call("api/recap", params={"date": recap_date.isoformat()})
            
            if error:
                st.error(f"Error loading recap: {error}")
            elif recap_data:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Calls", recap_data.get("totalCalls", 0))
                with col2:
                    st.metric("Connections", recap_data.get("connections", 0))
                with col3:
                    st.metric("Conversations", recap_data.get("conversations", 0))
                with col4:
                    st.metric("Total Cost", f"${recap_data.get('totalCost', 0):.2f}")
                
                if recap_data.get("dispositionBreakdown"):
                    st.markdown("**Disposition Breakdown:**")
                    st.text(recap_data["dispositionBreakdown"])
    else:
        st.warning("No stats data available")

# Leads Page
elif page == "Leads":
    st.header("👥 Leads Management")
    
    # Tabs for different lead operations
    tab1, tab2, tab3 = st.tabs(["View Leads", "Create Lead", "Upload CSV"])
    
    # Tab 1: View Leads
    with tab1:
        # Initialize page number in session state if not exists
        if "leads_page" not in st.session_state:
            st.session_state.leads_page = 1
        
        # Search and filter
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            search_term = st.text_input("🔍 Search leads", placeholder="Enter name, phone, or email...", key="search_leads")
        with col2:
            status_filter = st.selectbox("Status", ["All", "New", "Calling", "Completed", "DNC", "Pending"], key="status_filter")
        with col3:
            # Use session state value but different key for widget
            page_input = st.number_input("Page", min_value=1, value=st.session_state.leads_page, step=1, key="leads_page_input")
            # Sync session state if user manually changed the input
            if page_input != st.session_state.leads_page:
                st.session_state.leads_page = page_input
                st.rerun()
        
        st.markdown("---")
        
        # Fetch leads
        params = {
            "page": st.session_state.leads_page,
            "limit": 50
        }
        if search_term:
            params["search"] = search_term
        if status_filter != "All":
            params["status"] = status_filter
        
        with st.spinner("Loading leads..."):
            leads_data, error = api_call("api/leads", params=params)
        
        if error:
            st.error(f"Error loading leads: {error}")
        elif leads_data and leads_data.get("leads"):
            leads = leads_data["leads"]
            pagination = leads_data.get("pagination", {})
            
            st.subheader(f"Leads List ({pagination.get('total', 0)} total)")
            
            if leads:
                # Prepare data for display
                display_data = []
                for lead in leads:
                    display_data.append({
                        "Lead ID": lead.get("lead_id", ""),
                        "Name": f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip(),
                        "Email": lead.get("email", ""),
                        "Phone": lead.get("mobile_phone", ""),
                        "Company": lead.get("company", ""),
                        "Status": lead.get("status", ""),
                        "Calls": lead.get("call_count", 0),
                        "Campaign": lead.get("campaign", {}).get("campaign_name", "") if lead.get("campaign") else ""
                    })
                
                df = pd.DataFrame(display_data)
                st.dataframe(df, use_container_width=True)
                
                # Pagination info
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if pagination.get("hasMore"):
                        if st.button("Next Page", key="next_page"):
                            st.session_state.leads_page = st.session_state.leads_page + 1
                            st.rerun()
                with col2:
                    st.caption(f"Page {pagination.get('page', 1)} of {pagination.get('totalPages', 1)}")
                with col3:
                    if st.session_state.leads_page > 1:
                        if st.button("Previous Page", key="prev_page"):
                            st.session_state.leads_page = st.session_state.leads_page - 1
                            st.rerun()
                
                # Action buttons for selected lead
                st.markdown("---")
                st.subheader("Actions")
                selected_lead_id = st.text_input("Enter Lead ID to perform actions", placeholder="Lead ID", key="selected_lead")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📞 Trigger Call", use_container_width=True, key="trigger_call"):
                        if selected_lead_id:
                            with st.spinner("Triggering call..."):
                                result, error = api_call("api/trigger-call", method="POST", json_data={"lead_id": selected_lead_id})
                            if error:
                                st.error(f"Error: {error}")
                            elif result:
                                st.success(f"Call initiated! Call ID: {result.get('call_id', 'N/A')}")
                        else:
                            st.warning("Please enter a Lead ID")
                
                with col2:
                    new_status = st.selectbox("Update Status", ["New", "Calling", "Completed", "DNC"], key="update_status")
                    if st.button("💾 Update Lead", use_container_width=True, key="update_lead"):
                        if selected_lead_id:
                            with st.spinner("Updating lead..."):
                                result, error = api_call("api/leads", method="POST", json_data={"lead_id": selected_lead_id, "status": new_status})
                            if error:
                                st.error(f"Error: {error}")
                            elif result:
                                st.success("Lead updated successfully!")
                                st.rerun()
                        else:
                            st.warning("Please enter a Lead ID")
                
                with col3:
                    if st.button("🗑️ Delete Lead", use_container_width=True, key="delete_lead"):
                        if selected_lead_id:
                            with st.spinner("Deleting lead..."):
                                result, error = api_call("api/delete-lead", method="POST", json_data={"lead_id": selected_lead_id})
                            if error:
                                st.error(f"Error: {error}")
                            elif result:
                                st.success("Lead deleted successfully!")
                                st.rerun()
                        else:
                            st.warning("Please enter a Lead ID")
            else:
                st.info("No leads found")
        else:
            st.info("📋 No leads data available. Connect to your n8n workflow to load data.")
    
    # Tab 2: Create Lead
    with tab2:
        st.subheader("Create New Lead")
        
        with st.form("create_lead_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name *", key="create_first_name")
                last_name = st.text_input("Last Name *", key="create_last_name")
                email = st.text_input("Email *", key="create_email")
                mobile_phone = st.text_input("Mobile Phone * (e.g., +1234567890)", key="create_phone")
                company = st.text_input("Company *", key="create_company")
            
            with col2:
                title = st.text_input("Title", key="create_title")
                website = st.text_input("Website", key="create_website")
                state = st.text_input("State", key="create_state")
                notes = st.text_area("Notes", key="create_notes")
                campaign_name = st.text_input("Campaign Name (optional)", key="create_campaign")
            
            submitted = st.form_submit_button("Create Lead", use_container_width=True)
            
            if submitted:
                if not all([first_name, last_name, email, mobile_phone, company]):
                    st.error("Please fill in all required fields (marked with *)")
                else:
                    lead_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "mobile_phone": mobile_phone,
                        "company": company,
                        "title": title if title else None,
                        "website": website if website else None,
                        "state": state if state else None,
                        "notes": notes if notes else None
                    }
                    if campaign_name:
                        lead_data["campaign_name"] = campaign_name
                    
                    with st.spinner("Creating lead..."):
                        result, error = api_call("api/create-lead", method="POST", json_data=lead_data)
                    
                    if error:
                        st.error(f"Error creating lead: {error}")
                    elif result:
                        st.success(f"Lead created successfully! Lead ID: {result.get('lead', {}).get('lead_id', 'N/A')}")
                        st.rerun()
    
    # Tab 3: Upload CSV
    with tab3:
        st.subheader("Upload CSV File")
        st.info("Upload a CSV file with leads. The CSV should have headers that match your column mapping.")
        
        uploaded_file = st.file_uploader("Choose CSV file", type="csv", key="csv_upload")
        
        if uploaded_file:
            # Read CSV to show preview
            try:
                df_preview = pd.read_csv(uploaded_file, nrows=5)
                st.subheader("CSV Preview (first 5 rows)")
                st.dataframe(df_preview)
                
                st.markdown("---")
                st.subheader("Column Mapping")
                st.caption("Map your CSV columns to database fields")
                
                # Get available columns
                uploaded_file.seek(0)
                df_full = pd.read_csv(uploaded_file)
                csv_columns = df_full.columns.tolist()
                
                # Mapping form
                with st.form("csv_mapping_form"):
                    mapping = {}
                    col1, col2 = st.columns(2)
                    
                    db_fields = ["first_name", "last_name", "email", "mobile_phone", "company", "title", "website", "state", "notes"]
                    
                    for i, field in enumerate(db_fields):
                        col = col1 if i % 2 == 0 else col2
                        with col:
                            mapping[field] = st.selectbox(
                                field.replace("_", " ").title(),
                                ["None"] + csv_columns,
                                key=f"mapping_{field}"
                            )
                    
                    campaign_name = st.text_input("Campaign Name (optional)", key="csv_campaign")
                    skip_duplicates = st.checkbox("Skip Duplicates", value=True, key="skip_duplicates")
                    
                    submitted = st.form_submit_button("Upload CSV", use_container_width=True)
                    
                    if submitted:
                        # Build mapping (remove "None" values)
                        clean_mapping = {k: v for k, v in mapping.items() if v != "None"}
                        
                        if not clean_mapping:
                            st.error("Please map at least one column")
                        else:
                            # Read CSV content
                            uploaded_file.seek(0)
                            csv_content = uploaded_file.read().decode('utf-8')
                            
                            # Prepare request
                            request_data = {
                                "csv": csv_content,
                                "mapping": clean_mapping,
                                "options": {
                                    "skipDuplicates": skip_duplicates
                                }
                            }
                            
                            if campaign_name:
                                request_data["options"]["campaign_name"] = campaign_name
                            
                            with st.spinner("Uploading CSV..."):
                                result, error = api_call("api/csv-upload-flexible", method="POST", json_data=request_data)
                            
                            if error:
                                st.error(f"Error uploading CSV: {error}")
                            elif result:
                                st.success(f"CSV uploaded successfully!")
                                st.json(result)
            except Exception as e:
                st.error(f"Error reading CSV: {str(e)}")

# Calls Page
elif page == "Calls":
    st.header("📞 Call History")
    
    # Initialize page number in session state if not exists
    if "calls_page" not in st.session_state:
        st.session_state.calls_page = 1
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        date_from = st.date_input("From Date", value=datetime.now() - timedelta(days=7), key="calls_from")
    with col2:
        date_to = st.date_input("To Date", value=datetime.now(), key="calls_to")
    with col3:
        call_status = st.selectbox("Disposition", ["All", "Answered", "No Answer", "Busy", "Interested", "Not Interested"], key="call_disposition")
    with col4:
        # Use session state value but different key for widget
        page_input = st.number_input("Page", min_value=1, value=st.session_state.calls_page, step=1, key="calls_page_input")
        # Sync session state if user manually changed the input
        if page_input != st.session_state.calls_page:
            st.session_state.calls_page = page_input
            st.rerun()
    
    st.markdown("---")
    
    # Fetch calls
    params = {
        "dateFrom": date_from.isoformat(),
        "dateTo": date_to.isoformat(),
        "page": st.session_state.calls_page,
        "limit": 50
    }
    if call_status != "All":
        params["disposition"] = call_status
    
    with st.spinner("Loading calls..."):
        calls_data, error = api_call("api/calls", params=params)
    
    if error:
        st.error(f"Error loading calls: {error}")
    elif calls_data and calls_data.get("calls"):
        calls = calls_data["calls"]
        pagination = calls_data.get("pagination", {})
        
        st.subheader(f"Recent Calls ({pagination.get('total', 0)} total)")
        
        if calls:
            # Prepare data for display
            display_data = []
            for call in calls:
                call_date = call.get("call_date", "")
                if call_date:
                    try:
                        # Parse ISO date
                        dt = datetime.fromisoformat(call_date.replace('Z', '+00:00'))
                        call_date = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                
                display_data.append({
                    "Call ID": call.get("call_id", ""),
                    "Lead ID": call.get("lead_id", ""),
                    "Date": call_date,
                    "Duration": f"{call.get('duration', 0)}s",
                    "Disposition": call.get("disposition", ""),
                    "Answered": "✅" if call.get("answered") else "❌",
                    "Cost": f"${call.get('cost', 0):.2f}"
                })
            
            df = pd.DataFrame(display_data)
            st.dataframe(df, use_container_width=True)
            
            # Pagination
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if pagination.get("hasMore"):
                    if st.button("Next Page", key="calls_next"):
                        st.session_state.calls_page = st.session_state.calls_page + 1
                        st.rerun()
            with col2:
                st.caption(f"Page {pagination.get('page', 1)} of {pagination.get('totalPages', 1)}")
            with col3:
                if st.session_state.calls_page > 1:
                    if st.button("Previous Page", key="calls_prev"):
                        st.session_state.calls_page = st.session_state.calls_page - 1
                        st.rerun()
        else:
            st.info("No calls found for the selected filters")
    else:
        st.info("📋 No call history available. Connect to your n8n workflow to load data.")

# Campaigns Page
elif page == "Campaigns":
    st.header("📈 Campaigns")
    
    include_stats = st.checkbox("Include Statistics", value=True, key="campaigns_stats")
    
    if st.button("Refresh Campaigns", key="refresh_campaigns"):
        st.rerun()
    
    st.markdown("---")
    
    # Fetch campaigns
    params = {}
    if include_stats:
        params["include_stats"] = "true"
    
    with st.spinner("Loading campaigns..."):
        campaigns_data, error = api_call("api/get-campaigns", params=params)
    
    if error:
        st.error(f"Error loading campaigns: {error}")
    elif campaigns_data and campaigns_data.get("campaigns"):
        campaigns = campaigns_data["campaigns"]
        
        st.subheader(f"Active Campaigns ({len(campaigns)} total)")
        
        for campaign in campaigns:
            with st.expander(f"📋 {campaign.get('campaign_name', 'Unnamed Campaign')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Campaign ID:** {campaign.get('campaign_id', 'N/A')}")
                    st.write(f"**Sequence Template:** {campaign.get('sequence_template', 'N/A')}")
                    st.write(f"**Max Calls:** {campaign.get('max_calls', 'N/A')}")
                    st.write(f"**Duration (Weeks):** {campaign.get('duration_weeks', 'N/A')}")
                    st.write(f"**Active:** {'✅' if campaign.get('is_active') else '❌'}")
                
                with col2:
                    if campaign.get("stats"):
                        stats = campaign["stats"]
                        st.write("**Statistics:**")
                        st.write(f"- Total Leads: {stats.get('total_leads', 0)}")
                        st.write(f"- Active Leads: {stats.get('active_leads', 0)}")
                        st.write(f"- Completed Leads: {stats.get('completed_leads', 0)}")
    else:
        st.info("📋 No campaigns available.")

# Settings Page
elif page == "Settings":
    st.header("⚙️ Settings")
    
    st.subheader("API Configuration")
    api_url = st.text_input(
        "N8N Webhook URL",
        value=N8N_WEBHOOK_URL,
        help="Enter your n8n webhook base URL"
    )
    
    st.info(f"Current API Base URL: `{N8N_WEBHOOK_URL}`")
    st.caption("To change this, update the N8N_WEBHOOK_BASE_URL environment variable or .env file")
    
    st.markdown("---")
    
    st.subheader("Available API Endpoints")
    st.code("""
    GET  /api/stats-v2              - Get dashboard statistics
    GET  /api/leads                 - Get leads list (with filters)
    POST /api/leads                 - Update a lead
    GET  /api/calls                 - Get call history (with filters)
    POST /api/trigger-call         - Trigger a call for a lead
    POST /api/delete-lead           - Delete a lead
    POST /api/create-lead           - Create a new lead
    POST /api/csv-upload-flexible   - Upload CSV file with leads
    GET  /api/get-campaigns         - Get campaigns list
    GET  /api/recap                 - Get daily recap for a date
    """)
    
    st.markdown("---")
    
    st.subheader("About")
    st.info("""
    **AI-Caller v2.0**
    
    A simple Streamlit interface for managing AI-powered calling campaigns.
    
    **Features:**
    - Dashboard overview with real-time stats and daily recap
    - Leads management with search, filters, create, update, and delete
    - Call history with date range filtering
    - Campaign management and statistics
    - CSV upload for bulk lead import
    - Trigger calls and update leads
    
    All endpoints are connected to your n8n workflows.
    """)

# Footer
st.markdown("---")
st.caption("AI-Caller Dashboard | Powered by Streamlit & n8n")
