"""
Toast notification component for success/error messages.
Note: Streamlit doesn't support persistent toasts, so this uses session state.
"""
import streamlit as st
from typing import Optional


def show_toast(
    message: str,
    type: str = "success",
    title: Optional[str] = None,
    duration: int = 3
) -> None:
    """
    Show a toast notification.
    
    Args:
        message: Toast message
        type: Type of toast (success, error, warning, info)
        title: Optional title
        duration: Duration in seconds (not used, kept for API compatibility)
    """
    # Store toast in session state
    if "toasts" not in st.session_state:
        st.session_state.toasts = []
    
    toast = {
        "message": message,
        "type": type,
        "title": title or type.capitalize()
    }
    
    st.session_state.toasts.append(toast)


def render_toasts() -> None:
    """Render all toasts from session state."""
    if "toasts" not in st.session_state or not st.session_state.toasts:
        return
    
    # Get icon based on type
    icons = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️"
    }
    
    # Render toasts
    for toast in st.session_state.toasts:
        icon = icons.get(toast["type"], "ℹ️")
        toast_class = f"toast-{toast['type']}"
        
        st.markdown(f"""
        <div class="toast {toast_class}">
            <div class="toast-icon">{icon}</div>
            <div class="toast-content">
                <div class="toast-title">{toast['title']}</div>
                <div class="toast-message">{toast['message']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Clear toasts after rendering
    st.session_state.toasts = []


# Add CSS for toast container
st.markdown("""
<style>
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

