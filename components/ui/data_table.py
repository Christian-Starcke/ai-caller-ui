"""
Enhanced data table component using streamlit-aggrid.
"""
import streamlit as st
import pandas as pd
from streamlit_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from typing import Dict, List, Optional, Any


def enhanced_table(
    data: List[Dict[str, Any]],
    key: str,
    columns: Optional[List[str]] = None,
    selectable: bool = False,
    editable: bool = False,
    page_size: int = 50,
    height: int = 400
) -> Optional[List[Dict[str, Any]]]:
    """
    Display an enhanced data table with sorting, filtering, and selection.
    
    Args:
        data: List of dictionaries representing rows
        key: Unique key for the table
        columns: List of column names to display (if None, uses all keys)
        selectable: Enable row selection
        editable: Enable cell editing
        page_size: Number of rows per page
        height: Table height in pixels
        
    Returns:
        Selected rows if selectable, else None
    """
    if not data:
        st.info("No data available")
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Filter columns if specified
    if columns:
        available_columns = [col for col in columns if col in df.columns]
        df = df[available_columns]
    
    # Build grid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        resizable=True,
        sortable=True,
        filterable=True,
        editable=editable
    )
    
    # Configure selection
    if selectable:
        gb.configure_selection(
            selection_mode="multiple",
            use_checkbox=True,
            pre_selected_rows=[]
        )
    
    # Configure pagination
    gb.configure_pagination(
        enabled=True,
        paginationAutoPageSize=False,
        paginationPageSize=page_size
    )
    
    # Configure grid
    grid_options = gb.build()
    
    # Display table
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED if selectable else GridUpdateMode.NO_UPDATE,
        height=height,
        theme="streamlit",
        key=key,
        allow_unsafe_jscode=True
    )
    
    # Return selected rows if selectable
    if selectable and grid_response.get("selected_rows"):
        return grid_response["selected_rows"]
    
    return None

