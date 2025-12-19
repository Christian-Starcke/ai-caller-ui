"""
Badge component for status indicators.
"""
import streamlit as st
from typing import Optional


def badge(
    text: str,
    color: str = "primary",
    size: str = "normal"
) -> None:
    """
    Display a badge component.
    
    Args:
        text: Badge text
        color: Badge color (primary, success, warning, error, secondary)
        size: Badge size (small, normal, large)
    """
    size_class = f"badge-{size}" if size != "normal" else ""
    
    st.markdown(f"""
    <span class="badge badge-{color} {size_class}">{text}</span>
    """, unsafe_allow_html=True)


def status_badge(status: str) -> None:
    """
    Display a status badge with automatic color based on status.
    
    Args:
        status: Status value (New, Calling, Completed, DNC, etc.)
    """
    status_colors = {
        "new": "primary",
        "calling": "warning",
        "completed": "success",
        "dnc": "error",
        "answered": "success",
        "voicemail": "warning",
        "no_answer": "secondary",
        "busy": "warning",
        "failed": "error",
        "active": "success",
        "inactive": "secondary"
    }
    
    status_lower = status.lower()
    color = status_colors.get(status_lower, "secondary")
    
    badge(status, color)

