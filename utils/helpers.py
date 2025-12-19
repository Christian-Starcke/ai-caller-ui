"""
Utility functions for formatting, validation, and data manipulation.
"""
import re
from datetime import datetime
from typing import Optional, Dict, Any


def format_phone_number(phone: str) -> str:
    """
    Format phone number for display.
    
    Args:
        phone: Phone number in any format
        
    Returns:
        Formatted phone number (e.g., (555) 123-4567)
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[0:3]}) {digits[3:6]}-{digits[6:10]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:11]}"
    else:
        return phone  # Return as-is if format is unexpected


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not phone:
        return False
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Check if it's 10 or 11 digits (with country code)
    return len(digits) in [10, 11] and digits.isdigit()


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_date(date_str: Optional[str], format_str: str = "%Y-%m-%d") -> str:
    """
    Format date string for display.
    
    Args:
        date_str: Date string or datetime object
        format_str: Output format string
        
    Returns:
        Formatted date string
    """
    if not date_str:
        return ""
    
    try:
        if isinstance(date_str, str):
            # Try parsing common date formats
            for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime(format_str)
                except ValueError:
                    continue
            return date_str
        elif isinstance(date_str, datetime):
            return date_str.strftime(format_str)
        else:
            return str(date_str)
    except Exception:
        return str(date_str)


def format_datetime(datetime_str: Optional[str]) -> str:
    """
    Format datetime string for display.
    
    Args:
        datetime_str: Datetime string
        
    Returns:
        Formatted datetime string (e.g., "Dec 19, 2025 3:45 PM")
    """
    return format_date(datetime_str, "%b %d, %Y %I:%M %p")


def get_status_badge_color(status: str) -> str:
    """
    Get color for status badge.
    
    Args:
        status: Lead or call status
        
    Returns:
        Color name for badge
    """
    status_colors = {
        "new": "blue",
        "calling": "orange",
        "completed": "green",
        "dnc": "red",
        "answered": "green",
        "voicemail": "yellow",
        "no_answer": "gray",
        "busy": "orange",
        "failed": "red"
    }
    
    return status_colors.get(status.lower(), "gray")


def format_currency(amount: Optional[float]) -> str:
    """
    Format number as currency.
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string (e.g., "$1,234.56")
    """
    if amount is None:
        return "$0.00"
    
    return f"${amount:,.2f}"


def format_percentage(value: Optional[float], decimals: int = 1) -> str:
    """
    Format number as percentage.
    
    Args:
        value: Value to format (0-100 or 0-1)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string (e.g., "68.5%")
    """
    if value is None:
        return "0%"
    
    # If value is between 0 and 1, multiply by 100
    if 0 <= value <= 1:
        value = value * 100
    
    return f"{value:.{decimals}f}%"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def safe_get(data: Dict[str, Any], *keys, default: Any = None) -> Any:
    """
    Safely get nested dictionary value.
    
    Args:
        data: Dictionary to search
        *keys: Keys to traverse
        default: Default value if key not found
        
    Returns:
        Value or default
    """
    result = data
    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            return default
    return result

