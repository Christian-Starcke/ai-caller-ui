"""
Professional stat card component with icon, value, and trend indicator.
"""
import streamlit as st
from typing import Optional


def stat_card(
    title: str,
    value: str,
    change: Optional[str] = None,
    icon: Optional[str] = None,
    color: str = "primary"
) -> None:
    """
    Display a professional stat card.
    
    Args:
        title: Card title
        value: Main value to display
        change: Change indicator (e.g., "+12%", "-5%")
        icon: Emoji or icon to display
        color: Color theme (primary, success, warning, error)
    """
    # Determine color classes
    color_classes = {
        "primary": "stat-card-primary",
        "success": "stat-card-success",
        "warning": "stat-card-warning",
        "error": "stat-card-error"
    }
    card_class = color_classes.get(color, "stat-card-primary")
    
    # Parse change direction
    change_class = "stat-change-positive"
    change_icon = "↑"
    if change and change.startswith("-"):
        change_class = "stat-change-negative"
        change_icon = "↓"
    elif change and change.startswith("+"):
        change_class = "stat-change-positive"
        change_icon = "↑"
    
    # Build HTML
    icon_html = f'<span class="stat-icon">{icon}</span>' if icon else ""
    change_html = f'<span class="{change_class}">{change_icon} {change}</span>' if change else ""
    
    st.markdown(f"""
    <div class="stat-card {card_class}">
        <div class="stat-header">
            {icon_html}
            <span class="stat-title">{title}</span>
        </div>
        <div class="stat-value">{value}</div>
        {change_html}
    </div>
    """, unsafe_allow_html=True)


# Add CSS for stat cards
st.markdown("""
<style>
.stat-card {
    background: var(--surface);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    transition: all 0.2s;
}

.stat-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

.stat-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
}

.stat-icon {
    font-size: 1.5rem;
}

.stat-title {
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.stat-change-positive {
    color: var(--success);
    font-size: 0.875rem;
    font-weight: 600;
}

.stat-change-negative {
    color: var(--error);
    font-size: 0.875rem;
    font-weight: 600;
}

.stat-card-primary {
    border-left: 4px solid var(--primary);
}

.stat-card-success {
    border-left: 4px solid var(--success);
}

.stat-card-warning {
    border-left: 4px solid var(--warning);
}

.stat-card-error {
    border-left: 4px solid var(--error);
}
</style>
""", unsafe_allow_html=True)

