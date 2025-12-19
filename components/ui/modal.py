"""
Modal/dialog component for confirmations and forms.
"""
import streamlit as st
from typing import Optional, Callable


def show_modal(
    title: str,
    content: str,
    confirm_label: str = "Confirm",
    cancel_label: str = "Cancel",
    on_confirm: Optional[Callable] = None,
    on_cancel: Optional[Callable] = None,
    key: str = "modal"
) -> bool:
    """
    Show a modal dialog.
    
    Args:
        title: Modal title
        content: Modal content (HTML supported)
        confirm_label: Label for confirm button
        cancel_label: Label for cancel button
        on_confirm: Callback function when confirmed
        on_cancel: Callback function when cancelled
        key: Unique key for the modal
        
    Returns:
        True if confirmed, False if cancelled
    """
    modal_key = f"{key}_modal"
    
    if modal_key not in st.session_state:
        st.session_state[modal_key] = False
    
    # Show modal button (triggers modal)
    if st.button(title, key=f"{key}_trigger"):
        st.session_state[modal_key] = True
    
    # Render modal if active
    if st.session_state[modal_key]:
        st.markdown("""
        <div class="modal-overlay" id="modal-overlay">
            <div class="modal">
                <div class="modal-header">
                    <div class="modal-title">{}</div>
                    <button class="modal-close" onclick="document.getElementById('modal-overlay').style.display='none'">×</button>
                </div>
                <div class="modal-body">
                    {}
                </div>
                <div class="modal-footer">
                </div>
            </div>
        </div>
        """.format(title, content), unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(cancel_label, key=f"{key}_cancel", use_container_width=True):
                st.session_state[modal_key] = False
                if on_cancel:
                    on_cancel()
                st.rerun()
        
        with col2:
            if st.button(confirm_label, key=f"{key}_confirm", type="primary", use_container_width=True):
                st.session_state[modal_key] = False
                if on_confirm:
                    on_confirm()
                return True
    
    return False


def confirmation_dialog(
    message: str,
    confirm_label: str = "Yes, proceed",
    cancel_label: str = "Cancel",
    key: str = "confirm"
) -> bool:
    """
    Simple confirmation dialog.
    
    Args:
        message: Confirmation message
        confirm_label: Confirm button label
        cancel_label: Cancel button label
        key: Unique key
        
    Returns:
        True if confirmed, False otherwise
    """
    confirm_key = f"{key}_confirmed"
    
    if confirm_key not in st.session_state:
        st.session_state[confirm_key] = False
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.warning(message)
    with col2:
        if st.button(confirm_label, type="primary", key=f"{key}_btn", use_container_width=True):
            st.session_state[confirm_key] = True
            st.rerun()
    
    if st.session_state[confirm_key]:
        st.session_state[confirm_key] = False
        return True
    
    return False

