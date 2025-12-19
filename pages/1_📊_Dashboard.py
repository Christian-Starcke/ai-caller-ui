"""
Dashboard Page - Overview of stats and performance metrics
"""
import streamlit as st
from utils.api_client import get_api_client
from utils.helpers import format_percentage, safe_get
from utils.error_handler import handle_api_error
from components.ui.stat_card import stat_card
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard")
st.markdown("---")

# Initialize API client
api_client = get_api_client()

# Time frame selector
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("Performance Overview")
with col2:
    time_frame = st.selectbox(
        "Time Frame",
        ["today", "last7days", "last30days"],
        index=1,
        key="dashboard_timeframe"
    )

# Fetch stats
try:
    # Show loading state
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        from components.ui.loading import loading_skeleton_card
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="skeleton skeleton-card" style="height: 120px;"></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="skeleton skeleton-card" style="height: 120px;"></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="skeleton skeleton-card" style="height: 120px;"></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="skeleton skeleton-card" style="height: 120px;"></div>', unsafe_allow_html=True)
    
    stats_data = api_client.get_stats(time_frame=time_frame)
    loading_placeholder.empty()
    
    if stats_data:
        # Extract stats
        totals = safe_get(stats_data, "totals", default={})
        daily_stats = safe_get(stats_data, "dailyStats", default=[])
        disposition_breakdown = safe_get(stats_data, "dispositionBreakdown", default={})
        campaign_breakdown = safe_get(stats_data, "campaignBreakdown", default={})
        
        # Stats Cards with professional styling
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_leads = safe_get(totals, "total_leads", default=0)
            stat_card(
                "Total Leads",
                f"{total_leads:,}",
                icon="👥",
                color="primary"
            )
        
        with col2:
            active_leads = safe_get(totals, "active_leads", default=0)
            stat_card(
                "Active Leads",
                f"{active_leads:,}",
                icon="📞",
                color="success"
            )
        
        with col3:
            total_calls = safe_get(totals, "total_calls", default=0)
            stat_card(
                "Total Calls",
                f"{total_calls:,}",
                icon="📊",
                color="primary"
            )
        
        with col4:
            answer_rate = safe_get(totals, "answer_rate", default=0)
            answer_rate_pct = format_percentage(answer_rate)
            stat_card(
                "Answer Rate",
                answer_rate_pct,
                icon="✅",
                color="success"
            )
        
        st.markdown("---")
        
        # Charts Row
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Campaign Performance")
            if campaign_breakdown:
                campaigns = list(campaign_breakdown.keys())
                values = list(campaign_breakdown.values())
                
                fig = px.pie(
                    values=values,
                    names=campaigns,
                    title="Leads by Campaign"
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No campaign data available")
        
        with col2:
            st.subheader("Call Dispositions")
            if disposition_breakdown:
                dispositions = list(disposition_breakdown.keys())
                counts = list(disposition_breakdown.values())
                
                fig = px.bar(
                    x=dispositions,
                    y=counts,
                    title="Calls by Disposition",
                    labels={"x": "Disposition", "y": "Count"}
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No disposition data available")
        
        # Daily Stats Chart
        if daily_stats:
            st.subheader("Daily Activity")
            dates = [day.get("date", "") for day in daily_stats]
            calls = [day.get("calls", 0) for day in daily_stats]
            
            fig = px.line(
                x=dates,
                y=calls,
                title="Calls Over Time",
                labels={"x": "Date", "y": "Number of Calls"}
            )
            fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("No stats data available")
        
except Exception as e:
    handle_api_error(e, context="Loading dashboard statistics")

