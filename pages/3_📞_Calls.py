"""
Calls History Page - View and analyze call history
"""
import streamlit as st
from utils.api_client import get_api_client
from utils.helpers import (
    format_phone_number,
    format_datetime,
    get_status_badge_color,
    safe_get
)
from components.ui.data_table import enhanced_table
from components.ui.empty_state import empty_state
from components.ui.loading import loading_skeleton_table
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Calls", page_icon="📞", layout="wide")

st.title("📞 Call History")
st.markdown("---")

# Initialize API client
api_client = get_api_client()

# Initialize session state
if "calls_page" not in st.session_state:
    st.session_state.calls_page = 1
if "calls_filters" not in st.session_state:
    st.session_state.calls_filters = {}

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    
    # Date range (simplified - can be enhanced)
    date_filter = st.selectbox(
        "Time Period",
        ["All", "Today", "Last 7 Days", "Last 30 Days"],
        key="filter_date"
    )
    
    # Disposition filter
    disposition_filter = st.selectbox(
        "Disposition",
        ["All", "Answered", "Voicemail", "No Answer", "Busy", "Failed"],
        key="filter_disposition"
    )
    
    # Campaign filter
    try:
        campaigns_data = api_client.get_campaigns(include_stats=False)
        campaigns = safe_get(campaigns_data, "campaigns", default=[])
        campaign_names = ["All"] + [camp.get("campaign_name", "") for camp in campaigns if camp.get("campaign_name")]
    except:
        campaign_names = ["All"]
    
    campaign_filter = st.selectbox(
        "Campaign",
        campaign_names,
        key="filter_campaign"
    )
    
    # Search
    search_query = st.text_input("Search (name, phone)", key="filter_search")
    
    # Items per page
    items_per_page = st.selectbox(
        "Items per page",
        [25, 50, 100],
        index=1,
        key="items_per_page"
    )
    
    # Apply filters
    if st.button("Apply Filters", type="primary"):
        st.session_state.calls_filters = {
            "date": date_filter if date_filter != "All" else None,
            "disposition": disposition_filter if disposition_filter != "All" else None,
            "campaign_name": campaign_filter if campaign_filter != "All" else None,
            "search": search_query if search_query else None
        }
        st.session_state.calls_page = 1
        st.rerun()

# Main content
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("All Calls")
with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

# Check if Get Calls API is available
try:
    # Try to fetch calls
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        loading_skeleton_table(rows=5, cols=6)
    
    filters = st.session_state.calls_filters
    calls_data = api_client.get_calls(
        page=st.session_state.calls_page,
        limit=items_per_page,
        filters=filters
    )
    
    loading_placeholder.empty()
    
    calls = safe_get(calls_data, "calls", default=[])
    total_calls = safe_get(calls_data, "total", default=len(calls))
    total_pages = safe_get(calls_data, "total_pages", default=1)
    
    if calls:
        # Apply search filter if provided
        if filters.get("search"):
            search_term = filters["search"].lower()
            calls = [
                call for call in calls
                if (search_term in safe_get(call, "lead", "first_name", default="").lower() or
                    search_term in safe_get(call, "lead", "last_name", default="").lower() or
                    search_term in safe_get(call, "to_number", default="").lower())
            ]
        
        # Prepare data for table
        table_data = []
        for call in calls:
            lead = safe_get(call, "lead", default={})
            lead_name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
            
            table_data.append({
                "Call ID": call.get("call_id", "")[:8] + "..." if call.get("call_id") else "",
                "Lead": lead_name or "N/A",
                "Phone": format_phone_number(call.get("to_number", "")),
                "Campaign": safe_get(call, "lead", "campaign_name", default="N/A"),
                "Date": format_datetime(call.get("call_date")),
                "Duration": f"{call.get('duration_seconds', 0)}s" if call.get("duration_seconds") else "N/A",
                "Disposition": call.get("disposition", "N/A"),
                "Status": call.get("status", "N/A")
            })
        
        # Display table
        enhanced_table(
            table_data,
            key="calls_table",
            selectable=False,
            page_size=items_per_page,
            height=600
        )
        
        # Pagination
        if total_pages > 1:
            col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
            with col1:
                if st.button("◀ Previous", disabled=st.session_state.calls_page == 1):
                    st.session_state.calls_page -= 1
                    st.rerun()
            with col3:
                st.caption(f"Page {st.session_state.calls_page} of {total_pages} ({total_calls} total calls)")
            with col5:
                if st.button("Next ▶", disabled=st.session_state.calls_page >= total_pages):
                    st.session_state.calls_page += 1
                    st.rerun()
        
        # Analytics section
        st.markdown("---")
        st.subheader("📊 Analytics")
        
        # Calculate stats
        dispositions = {}
        for call in calls:
            disp = call.get("disposition", "Unknown")
            dispositions[disp] = dispositions.get(disp, 0) + 1
        
        if dispositions:
            col1, col2 = st.columns(2)
            
            with col1:
                # Disposition breakdown chart
                fig = px.pie(
                    values=list(dispositions.values()),
                    names=list(dispositions.keys()),
                    title="Calls by Disposition"
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Disposition bar chart
                fig = px.bar(
                    x=list(dispositions.keys()),
                    y=list(dispositions.values()),
                    title="Call Dispositions",
                    labels={"x": "Disposition", "y": "Count"}
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    else:
        empty_state(
            icon="📞",
            title="No calls found",
            description="Calls will appear here once your campaigns start making calls. Make sure 'API - Get Calls' workflow is activated in n8n.",
            action_label="View Dashboard",
            action_callback=lambda: st.switch_page("pages/1_📊_Dashboard.py")
        )

except Exception as e:
    error_msg = str(e)
    if "404" in error_msg or "not found" in error_msg.lower():
        st.warning("⚠️ Calls API endpoint not available")
        st.info("""
        The 'API - Get Calls' workflow may not be activated in n8n.
        
        **To enable this feature:**
        1. Go to your n8n instance
        2. Find the 'API - Get Calls' workflow (ID: `R6Sfo6fgihCRXouy`)
        3. Activate the workflow
        4. Refresh this page
        """)
    else:
        st.error(f"Error loading calls: {error_msg}")
        st.info("Please check your API configuration and ensure n8n workflows are active.")

