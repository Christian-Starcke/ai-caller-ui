"""
Header component for the application.
"""
import streamlit as st


def render_header(title: str = "AI-Caller", show_actions: bool = True) -> None:
    """
    Render application header.
    
    Args:
        title: Application title
        show_actions: Whether to show action buttons
    """
    if show_actions:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"<h1 style='margin: 0;'>{title}</h1>", unsafe_allow_html=True)
        with col2:
            col2a, col2b = st.columns(2)
            with col2a:
                if st.button("🔄 Refresh", use_container_width=True):
                    st.rerun()
            with col2b:
                if st.button("⚙️ Settings", use_container_width=True):
                    st.switch_page("pages/5_⚙️_Settings.py")
    else:
        st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)

