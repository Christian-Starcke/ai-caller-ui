"""
Leads Management Page - Create, view, update, and manage leads
"""
import streamlit as st
import pandas as pd
from utils.api_client import get_api_client
from utils.helpers import (
    format_phone_number,
    format_date,
    validate_phone_number,
    validate_email,
    get_status_badge_color,
    safe_get
)
from utils.error_handler import handle_api_error
from components.ui.data_table import enhanced_table
from components.ui.empty_state import empty_state
from components.ui.badge import status_badge
from components.ui.loading import loading_skeleton_table

st.set_page_config(page_title="Leads", page_icon="👥", layout="wide")

st.title("👥 Lead Management")
st.markdown("---")

# Initialize API client
api_client = get_api_client()

# Initialize session state
if "leads_page" not in st.session_state:
    st.session_state.leads_page = 1
if "leads_filters" not in st.session_state:
    st.session_state.leads_filters = {}
if "show_create_form" not in st.session_state:
    st.session_state.show_create_form = False

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    
    # Status filter
    status_filter = st.selectbox(
        "Status",
        ["All", "New", "Calling", "Completed", "DNC"],
        key="filter_status"
    )
    
    # Campaign filter - fetch campaigns first
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
    search_query = st.text_input("Search (name, email, phone, company)", key="filter_search")
    
    # Items per page
    items_per_page = st.selectbox(
        "Items per page",
        [25, 50, 100],
        index=1,
        key="items_per_page"
    )
    
    # Apply filters button
    if st.button("Apply Filters", type="primary"):
        st.session_state.leads_filters = {
            "status": status_filter if status_filter != "All" else None,
            "campaign_name": campaign_filter if campaign_filter != "All" else None,
            "search": search_query if search_query else None
        }
        st.session_state.leads_page = 1
        st.rerun()

# Main content area
tab1, tab2, tab3 = st.tabs(["📋 View Leads", "➕ Create Lead", "📤 Upload CSV"])

# Tab 1: View Leads
with tab1:
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.subheader("All Leads")
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    with col3:
        if st.button("📥 Export", use_container_width=True):
            st.info("Export functionality coming soon")
    
    # Fetch leads
    try:
        # Show loading skeleton while fetching
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            loading_skeleton_table(rows=5, cols=6)
        
        filters = st.session_state.leads_filters
        leads_data = api_client.get_leads(
            page=st.session_state.leads_page,
            limit=items_per_page,
            status=filters.get("status"),
            campaign_name=filters.get("campaign_name")
        )
        
        loading_placeholder.empty()
        
        leads = safe_get(leads_data, "leads", default=[])
        total_leads = safe_get(leads_data, "total", default=len(leads))
        total_pages = safe_get(leads_data, "total_pages", default=1)
        
        if leads:
            # Apply search filter if provided
            if filters.get("search"):
                search_term = filters["search"].lower()
                leads = [
                    lead for lead in leads
                    if (search_term in lead.get("first_name", "").lower() or
                        search_term in lead.get("last_name", "").lower() or
                        search_term in lead.get("email", "").lower() or
                        search_term in lead.get("mobile_phone", "").lower() or
                        search_term in lead.get("company", "").lower())
                ]
            
            # Prepare data for table
            table_data = []
            for lead in leads:
                table_data.append({
                    "Lead ID": lead.get("lead_id", "")[:8] + "..." if lead.get("lead_id") else "",
                    "Name": f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip(),
                    "Email": lead.get("email", ""),
                    "Phone": format_phone_number(lead.get("mobile_phone", "")),
                    "Company": lead.get("company", ""),
                    "Campaign": lead.get("campaign_name", "N/A"),
                    "Status": lead.get("status", "N/A"),  # Will be displayed with badge
                    "Calls": lead.get("call_count", 0),
                    "Next Call": format_date(lead.get("next_call_date")),
                    "Created": format_date(lead.get("upload_date"))
                })
            
            # Display table
            selected_rows = enhanced_table(
                table_data,
                key="leads_table",
                selectable=True,
                page_size=items_per_page,
                height=600
            )
            
            # Pagination
            if total_pages > 1:
                col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
                with col1:
                    if st.button("◀ Previous", disabled=st.session_state.leads_page == 1):
                        st.session_state.leads_page -= 1
                        st.rerun()
                with col3:
                    st.caption(f"Page {st.session_state.leads_page} of {total_pages} ({total_leads} total leads)")
                with col5:
                    if st.button("Next ▶", disabled=st.session_state.leads_page >= total_pages):
                        st.session_state.leads_page += 1
                        st.rerun()
            
            # Selected rows actions
            if selected_rows:
                st.markdown("---")
                st.subheader(f"Selected: {len(selected_rows)} lead(s)")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📝 Bulk Update Status", use_container_width=True):
                        st.info("Bulk update coming soon")
                with col2:
                    if st.button("🔄 Change Campaign", use_container_width=True):
                        st.info("Bulk campaign change coming soon")
                with col3:
                    if st.button("📥 Export Selected", use_container_width=True):
                        st.info("Export selected coming soon")
        else:
            empty_state(
                icon="👥",
                title="No leads found",
                description="Create your first lead to get started, or adjust your filters to see more results.",
                action_label="Create Lead",
                action_callback=lambda: st.switch_page("pages/2_👥_Leads.py")
            )
            
    except Exception as e:
        handle_api_error(e, context="Loading leads data")

# Tab 2: Create Lead
with tab2:
    st.subheader("Create New Lead")
    
    with st.form("create_lead_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name *", placeholder="John")
            last_name = st.text_input("Last Name *", placeholder="Doe")
            email = st.text_input("Email *", placeholder="john.doe@example.com")
            mobile_phone = st.text_input("Mobile Phone *", placeholder="+15551234567")
        
        with col2:
            company = st.text_input("Company", placeholder="Acme Corp")
            
            # Campaign selector
            try:
                campaigns_data = api_client.get_campaigns(include_stats=False)
                campaigns = safe_get(campaigns_data, "campaigns", default=[])
                campaign_options = {camp.get("campaign_name", ""): camp.get("campaign_id", "") 
                                  for camp in campaigns if camp.get("campaign_name")}
                campaign_names = list(campaign_options.keys())
                default_campaign = "Standard 7-Week" if "Standard 7-Week" in campaign_names else (campaign_names[0] if campaign_names else None)
                
                selected_campaign = st.selectbox(
                    "Campaign",
                    campaign_names,
                    index=0 if default_campaign and campaign_names else None
                )
                campaign_id = campaign_options.get(selected_campaign)
            except:
                campaign_id = None
                selected_campaign = st.text_input("Campaign", value="Standard 7-Week")
            
            notes = st.text_area("Notes", height=100)
        
        submitted = st.form_submit_button("Create Lead", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            errors = []
            if not first_name:
                errors.append("First name is required")
            if not last_name:
                errors.append("Last name is required")
            if not email:
                errors.append("Email is required")
            elif not validate_email(email):
                errors.append("Invalid email format")
            if not mobile_phone:
                errors.append("Mobile phone is required")
            elif not validate_phone_number(mobile_phone):
                errors.append("Invalid phone number format")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Create lead
                try:
                    lead_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "mobile_phone": mobile_phone,
                        "company": company if company else None,
                        "notes": notes if notes else None
                    }
                    
                    # Add campaign
                    if campaign_id:
                        lead_data["campaign_id"] = campaign_id
                    elif selected_campaign:
                        lead_data["campaign_name"] = selected_campaign
                    
                    with st.spinner("Creating lead..."):
                        result = api_client.create_lead(lead_data)
                    
                    if result:
                        st.success(f"✅ Lead created successfully!")
                        st.balloons()
                        # Optionally switch to View Leads tab
                        st.info("Switch to 'View Leads' tab to see your new lead.")
                except Exception as e:
                    st.error(f"Error creating lead: {str(e)}")

# Tab 3: CSV Upload
with tab3:
    st.subheader("Bulk Upload Leads via CSV")
    st.info("📋 Upload a CSV file with lead data. Required columns: first_name, last_name, email, mobile_phone")
    
    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=["csv"],
        help="CSV file should contain columns: first_name, last_name, email, mobile_phone, company (optional)"
    )
    
    if uploaded_file:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            
            # Show preview
            st.subheader("CSV Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Campaign selector for bulk assignment
            try:
                campaigns_data = api_client.get_campaigns(include_stats=False)
                campaigns = safe_get(campaigns_data, "campaigns", default=[])
                campaign_options = {camp.get("campaign_name", ""): camp.get("campaign_id", "") 
                                  for camp in campaigns if camp.get("campaign_name")}
                campaign_names = list(campaign_options.keys())
                default_campaign = "Standard 7-Week" if "Standard 7-Week" in campaign_names else (campaign_names[0] if campaign_names else None)
                
                selected_campaign = st.selectbox(
                    "Assign all leads to campaign",
                    campaign_names,
                    index=0 if default_campaign and campaign_names else None
                )
                campaign_id = campaign_options.get(selected_campaign)
            except:
                campaign_id = None
                selected_campaign = st.text_input("Campaign", value="Standard 7-Week")
            
            # Upload button
            if st.button("📤 Upload CSV", type="primary", use_container_width=True):
                try:
                    # Convert DataFrame to CSV string
                    csv_string = df.to_csv(index=False)
                    
                    # Prepare options
                    options = {}
                    if campaign_id:
                        options["campaign_id"] = campaign_id
                    elif selected_campaign:
                        options["campaign_name"] = selected_campaign
                    
                    with st.spinner("Uploading leads..."):
                        result = api_client.upload_csv(csv_string, options)
                    
                    if result:
                        st.success(f"✅ Successfully uploaded {len(df)} leads!")
                        st.balloons()
                        st.json(result)
                except Exception as e:
                    st.error(f"Error uploading CSV: {str(e)}")
        
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
            st.info("Please ensure your CSV file is properly formatted.")

