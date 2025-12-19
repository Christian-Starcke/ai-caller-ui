"""
Campaigns Management Page - View and manage campaigns
"""
import streamlit as st
from utils.api_client import get_api_client
from utils.helpers import safe_get, format_percentage
from components.ui.stat_card import stat_card
import plotly.express as px

st.set_page_config(page_title="Campaigns", page_icon="📈", layout="wide")

st.title("📈 Campaign Management")
st.markdown("---")

# Initialize API client
api_client = get_api_client()

# Fetch campaigns
try:
    with st.spinner("Loading campaigns..."):
        campaigns_data = api_client.get_campaigns(include_stats=True)
    
    campaigns = safe_get(campaigns_data, "campaigns", default=[])
    
    if campaigns:
        # Campaigns Overview
        st.subheader("Campaigns Overview")
        
        # Display campaigns in cards
        for campaign in campaigns:
            with st.expander(f"📋 {campaign.get('campaign_name', 'Unknown Campaign')}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Description:** {campaign.get('description', 'N/A')}")
                    st.markdown(f"**Sequence Template:** `{campaign.get('sequence_template', 'N/A')}`")
                    st.markdown(f"**Max Calls:** {campaign.get('max_calls', 'N/A')}")
                    st.markdown(f"**Duration:** {campaign.get('duration_weeks', 'N/A')} weeks")
                
                with col2:
                    stats = safe_get(campaign, "stats", default={})
                    total_leads = safe_get(stats, "total_leads", default=0)
                    active_leads = safe_get(stats, "active_leads", default=0)
                    completed_leads = safe_get(stats, "completed_leads", default=0)
                    
                    st.markdown("**Statistics:**")
                    st.metric("Total Leads", f"{total_leads:,}")
                    st.metric("Active Leads", f"{active_leads:,}")
                    st.metric("Completed Leads", f"{completed_leads:,}")
                
                with col3:
                    if total_leads > 0:
                        completion_rate = (completed_leads / total_leads) * 100 if total_leads > 0 else 0
                        active_rate = (active_leads / total_leads) * 100 if total_leads > 0 else 0
                        
                        st.markdown("**Performance:**")
                        st.metric("Completion Rate", format_percentage(completion_rate))
                        st.metric("Active Rate", format_percentage(active_rate))
                    else:
                        st.info("No leads assigned to this campaign yet")
        
        st.markdown("---")
        
        # Campaign Performance Charts
        st.subheader("Campaign Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Leads distribution
            campaign_names = [camp.get("campaign_name", "Unknown") for camp in campaigns]
            campaign_totals = [safe_get(camp, "stats", "total_leads", default=0) for camp in campaigns]
            
            if sum(campaign_totals) > 0:
                fig = px.pie(
                    values=campaign_totals,
                    names=campaign_names,
                    title="Leads Distribution by Campaign"
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No leads data available for distribution")
        
        with col2:
            # Campaign comparison
            campaign_active = [safe_get(camp, "stats", "active_leads", default=0) for camp in campaigns]
            campaign_completed = [safe_get(camp, "stats", "completed_leads", default=0) for camp in campaigns]
            
            if sum(campaign_active) > 0 or sum(campaign_completed) > 0:
                fig = px.bar(
                    x=campaign_names,
                    y=[campaign_active, campaign_completed],
                    title="Active vs Completed Leads by Campaign",
                    labels={"x": "Campaign", "y": "Number of Leads", "value": "Count"},
                    barmode='group'
                )
                fig.update_layout(
                    legend=dict(
                        title="Status",
                        labels=["Active", "Completed"]
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No leads data available for comparison")
        
        # Campaign Stats Summary
        st.markdown("---")
        st.subheader("Campaign Statistics Summary")
        
        # Calculate totals
        total_all_leads = sum([safe_get(camp, "stats", "total_leads", default=0) for camp in campaigns])
        total_active = sum([safe_get(camp, "stats", "active_leads", default=0) for camp in campaigns])
        total_completed = sum([safe_get(camp, "stats", "completed_leads", default=0) for camp in campaigns])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            stat_card(
                "Total Campaigns",
                str(len(campaigns)),
                icon="📋",
                color="primary"
            )
        
        with col2:
            stat_card(
                "Total Leads",
                f"{total_all_leads:,}",
                icon="👥",
                color="primary"
            )
        
        with col3:
            stat_card(
                "Active Leads",
                f"{total_active:,}",
                icon="📞",
                color="success"
            )
        
        with col4:
            stat_card(
                "Completed Leads",
                f"{total_completed:,}",
                icon="✅",
                color="success"
            )
        
        # Campaign Details Table
        st.markdown("---")
        st.subheader("Campaign Details")
        
        table_data = []
        for campaign in campaigns:
            stats = safe_get(campaign, "stats", default={})
            table_data.append({
                "Campaign Name": campaign.get("campaign_name", "N/A"),
                "Sequence": campaign.get("sequence_template", "N/A"),
                "Max Calls": campaign.get("max_calls", "N/A"),
                "Duration": f"{campaign.get('duration_weeks', 'N/A')} weeks",
                "Total Leads": safe_get(stats, "total_leads", default=0),
                "Active": safe_get(stats, "active_leads", default=0),
                "Completed": safe_get(stats, "completed_leads", default=0),
                "Status": "Active" if campaign.get("is_active", True) else "Inactive"
            })
        
        st.dataframe(table_data, use_container_width=True, hide_index=True)
        
    else:
        st.warning("No campaigns found")
        st.info("Please check your API configuration and ensure campaigns are set up in the database.")
        
except Exception as e:
    st.error(f"Error loading campaigns: {str(e)}")
    st.info("Please check your API configuration and ensure n8n workflows are active.")

