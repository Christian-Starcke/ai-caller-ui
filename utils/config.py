"""
Configuration management for the Streamlit UI application.
Handles environment variables and default configuration values.
"""
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # n8n API Configuration
    N8N_WEBHOOK_BASE_URL = os.getenv(
        "N8N_WEBHOOK_BASE_URL",
        "https://primary-production-10917.up.railway.app/webhook"
    )
    
    # Streamlit Configuration
    STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")
    
    # Application Settings
    CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", "5"))
    ITEMS_PER_PAGE = int(os.getenv("ITEMS_PER_PAGE", "50"))
    
    # API Timeout Settings
    API_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "30"))
    API_RETRY_ATTEMPTS = int(os.getenv("API_RETRY_ATTEMPTS", "3"))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        errors = []
        
        if not cls.N8N_WEBHOOK_BASE_URL:
            errors.append("N8N_WEBHOOK_BASE_URL is required")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    @classmethod
    def get_api_url(cls, endpoint: str) -> str:
        """
        Get full API URL for an endpoint.
        
        Args:
            endpoint: API endpoint path (e.g., 'api/get-campaigns')
            
        Returns:
            Full URL string
        """
        # Remove leading slash if present
        endpoint = endpoint.lstrip('/')
        # Ensure base URL doesn't end with slash
        base_url = cls.N8N_WEBHOOK_BASE_URL.rstrip('/')
        return f"{base_url}/{endpoint}"


# Initialize and validate configuration
try:
    Config.validate()
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

