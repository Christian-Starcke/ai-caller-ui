"""
n8n API Client for interacting with webhook endpoints.
Handles HTTP requests, error handling, and response caching.
"""
import requests
import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from utils.config import Config


class APIClient:
    """Client for interacting with n8n webhook APIs."""
    
    def __init__(self):
        self.base_url = Config.N8N_WEBHOOK_BASE_URL
        self.timeout = Config.API_TIMEOUT_SECONDS
        self.retry_attempts = Config.API_RETRY_ATTEMPTS
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to n8n API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: Request body (for POST/PUT)
            headers: Custom headers
            
        Returns:
            Response data as dictionary
            
        Raises:
            requests.RequestException: If request fails
        """
        url = Config.get_api_url(endpoint)
        
        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if headers:
            default_headers.update(headers)
        
        for attempt in range(self.retry_attempts):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    headers=default_headers,
                    timeout=self.timeout
                )
                
                # Raise exception for bad status codes
                response.raise_for_status()
                
                # Try to parse JSON, return empty dict if not JSON
                try:
                    return response.json()
                except ValueError:
                    return {"status": "success", "message": response.text}
                    
            except requests.exceptions.Timeout:
                if attempt == self.retry_attempts - 1:
                    raise Exception(f"Request timeout after {self.retry_attempts} attempts")
                continue
                
            except requests.exceptions.RequestException as e:
                if attempt == self.retry_attempts - 1:
                    raise Exception(f"API request failed: {str(e)}")
                continue
        
        raise Exception("Request failed after all retry attempts")
    
    # Campaign APIs
    def get_campaigns(self, include_stats: bool = True) -> Dict[str, Any]:
        """Get all campaigns with optional stats."""
        params = {"include_stats": "true"} if include_stats else {}
        return self._make_request("GET", "api/get-campaigns", params=params)
    
    # Lead APIs
    def get_leads(
        self,
        page: int = 1,
        limit: int = 50,
        status: Optional[str] = None,
        campaign_id: Optional[str] = None,
        campaign_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get leads with pagination and filters."""
        params = {
            "page": page,
            "limit": limit
        }
        if status:
            params["status"] = status
        if campaign_id:
            params["campaign_id"] = campaign_id
        if campaign_name:
            params["campaign_name"] = campaign_name
        
        return self._make_request("GET", "api/leads", params=params)
    
    def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead."""
        return self._make_request("POST", "api/create-lead", json_data=lead_data)
    
    def update_lead(self, lead_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing lead."""
        payload = {"lead_id": lead_id, **update_data}
        return self._make_request("POST", "api/leads", json_data=payload)
    
    def delete_lead(self, lead_id: str) -> Dict[str, Any]:
        """Delete a lead."""
        return self._make_request("POST", "api/delete-lead", json_data={"lead_id": lead_id})
    
    # Stats API
    def get_stats(
        self,
        time_frame: str = "last7days",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get statistics.
        
        Args:
            time_frame: One of 'today', 'last7days', 'last30days', 'custom'
            start_date: Start date for custom time frame (YYYY-MM-DD)
            end_date: End date for custom time frame (YYYY-MM-DD)
        """
        params = {"timeFrame": time_frame}
        if time_frame == "custom" and start_date and end_date:
            params["start_date"] = start_date
            params["end_date"] = end_date
        
        return self._make_request("GET", "api/stats-v2", params=params)
    
    # CSV Upload API
    def upload_csv(self, csv_data: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Upload CSV file.
        
        Args:
            csv_data: CSV file content as string
            options: Upload options (campaign_id, campaign_name, etc.)
        """
        payload = {"csv_data": csv_data}
        if options:
            payload["options"] = options
        
        return self._make_request("POST", "api/csv-upload", json_data=payload)
    
    # Calls API (if activated)
    def get_calls(
        self,
        page: int = 1,
        limit: int = 50,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get call history with pagination and filters."""
        params = {"page": page, "limit": limit}
        if filters:
            params.update(filters)
        
        return self._make_request("GET", "api/calls", params=params)
    
    # Recap API (if activated)
    def get_recap(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Get daily recap data."""
        params = {}
        if date:
            params["date"] = date
        
        return self._make_request("GET", "api/recap", params=params)
    
    # Trigger Call API (if activated)
    def trigger_call(self, lead_id: str) -> Dict[str, Any]:
        """Manually trigger a call for a lead."""
        return self._make_request("POST", "api/trigger-call", json_data={"lead_id": lead_id})


# Create singleton instance
@st.cache_resource
def get_api_client() -> APIClient:
    """Get cached API client instance."""
    return APIClient()

