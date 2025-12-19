"""
Error handling utilities for graceful error management.
"""
import streamlit as st
from typing import Callable, Any
import traceback


def handle_api_error(error: Exception, context: str = "") -> None:
    """
    Display user-friendly error messages for API errors.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    """
    error_msg = str(error)
    
    # Determine error type and show appropriate message
    if "404" in error_msg or "not found" in error_msg.lower():
        st.warning(f"⚠️ Resource not found")
        if context:
            st.info(f"**Context:** {context}")
        st.info("""
        **Possible causes:**
        - The API endpoint may not be activated in n8n
        - The resource may have been deleted
        - Check your API configuration
        """)
    elif "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
        st.error("⏱️ Request timeout")
        st.info("""
        The API request took too long to respond. This could be due to:
        - Network connectivity issues
        - API server overload
        - Large data processing
        
        Please try again in a moment.
        """)
    elif "401" in error_msg or "403" in error_msg or "unauthorized" in error_msg.lower():
        st.error("🔒 Authentication Error")
        st.info("""
        **Access denied.** Please check:
        - Your API credentials are correct
        - You have permission to access this resource
        - Your API key hasn't expired
        """)
    elif "500" in error_msg or "server error" in error_msg.lower():
        st.error("🔴 Server Error")
        st.info("""
        The API server encountered an error. This is likely a temporary issue.
        
        **What to do:**
        1. Wait a few moments and try again
        2. Check the n8n workflow logs
        3. Contact support if the issue persists
        """)
    else:
        # Generic error
        st.error(f"❌ Error: {error_msg}")
        if context:
            st.info(f"**Context:** {context}")
    
    # Show technical details in expander (for debugging)
    with st.expander("🔍 Technical Details (for debugging)"):
        st.code(traceback.format_exc())


def safe_execute(func: Callable, *args, error_context: str = "", **kwargs) -> Any:
    """
    Safely execute a function and handle errors gracefully.
    
    Args:
        func: Function to execute
        *args: Positional arguments
        error_context: Context for error messages
        **kwargs: Keyword arguments
        
    Returns:
        Function result or None if error occurred
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        handle_api_error(e, error_context)
        return None


@st.cache_data(ttl=300)  # Cache for 5 minutes
def cached_api_call(func: Callable, *args, **kwargs) -> Any:
    """
    Execute an API call with caching.
    
    Args:
        func: API function to call
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        API response or None if error
    """
    return safe_execute(func, *args, **kwargs)

