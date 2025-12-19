# UI Components Guide

## Overview
This document describes all the professional UI components available in the Streamlit UI application.

## Components

### 1. Stat Card (`components/ui/stat_card.py`)
Professional stat card with icon, value, and trend indicator.

**Usage:**
```python
from components.ui.stat_card import stat_card

stat_card(
    title="Total Leads",
    value="1,234",
    change="+12%",
    icon="👥",
    color="primary"  # primary, success, warning, error
)
```

### 2. Enhanced Data Table (`components/ui/data_table.py`)
Professional data table with sorting, filtering, and pagination using streamlit-aggrid.

**Usage:**
```python
from components.ui.data_table import enhanced_table

selected_rows = enhanced_table(
    data=list_of_dicts,
    key="my_table",
    selectable=True,
    page_size=50,
    height=600
)
```

### 3. Empty State (`components/ui/empty_state.py`)
Display when there's no data to show.

**Usage:**
```python
from components.ui.empty_state import empty_state

empty_state(
    icon="👥",
    title="No leads found",
    description="Create your first lead to get started.",
    action_label="Create Lead",
    action_callback=lambda: st.switch_page("pages/2_👥_Leads.py")
)
```

### 4. Loading Skeleton (`components/ui/loading.py`)
Skeleton screens for better loading UX.

**Usage:**
```python
from components.ui.loading import loading_skeleton_table, loading_skeleton_card

# For tables
loading_skeleton_table(rows=5, cols=4)

# For cards
loading_skeleton_card(count=3)
```

### 5. Toast Notifications (`components/ui/toast.py`)
Success/error notifications (uses session state).

**Usage:**
```python
from components.ui.toast import show_toast, render_toasts

# Show toast
show_toast("Lead created successfully!", type="success")

# Render toasts (call at top of page)
render_toasts()
```

### 6. Modal/Dialog (`components/ui/modal.py`)
Modal dialogs for confirmations.

**Usage:**
```python
from components.ui.modal import confirmation_dialog

if confirmation_dialog(
    message="Are you sure you want to delete this lead?",
    confirm_label="Yes, delete",
    cancel_label="Cancel"
):
    # Delete action
    pass
```

### 7. Badge (`components/ui/badge.py`)
Status badges with automatic color coding.

**Usage:**
```python
from components.ui.badge import badge, status_badge

# Custom badge
badge("Active", color="success")

# Status badge (auto-color)
status_badge("Completed")  # Green
status_badge("New")        # Blue
status_badge("DNC")        # Red
```

### 8. Header (`components/layout/header.py`)
Application header component.

**Usage:**
```python
from components.layout.header import render_header

render_header(title="AI-Caller", show_actions=True)
```

## Styling

All components use the professional theme defined in `assets/style.css`. The theme includes:

- **Color Scheme**: Professional blue primary, with success/warning/error colors
- **Typography**: Clean, modern fonts
- **Shadows**: Subtle elevation effects
- **Animations**: Smooth transitions and hover effects
- **Responsive**: Mobile-friendly design

## Best Practices

1. **Use loading skeletons** instead of spinners for better UX
2. **Show empty states** when there's no data
3. **Use badges** for status indicators
4. **Implement toasts** for user feedback
5. **Use modals** for destructive actions

## Examples

See the existing pages for examples:
- `pages/1_📊_Dashboard.py` - Stat cards and charts
- `pages/2_👥_Leads.py` - Tables, forms, empty states
- `pages/3_📞_Calls.py` - Data tables and analytics
- `pages/4_📈_Campaigns.py` - Campaign cards and charts

