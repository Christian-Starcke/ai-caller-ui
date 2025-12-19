"""
Empty state component for when there's no data to display.
"""
import streamlit as st


def empty_state(
    icon: str = "📭",
    title: str = "No data available",
    description: str = "There's nothing here yet.",
    action_label: str = None,
    action_callback=None
) -> None:
    """
    Display an empty state with icon, message, and optional action.
    
    Args:
        icon: Emoji or icon to display
        title: Main title text
        description: Description text
        action_label: Label for action button (optional)
        action_callback: Function to call when button is clicked (optional)
    """
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{title}</div>
        <div class="empty-state-description">{description}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if action_label and action_callback:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(action_label, type="primary", use_container_width=True):
            action_callback()

