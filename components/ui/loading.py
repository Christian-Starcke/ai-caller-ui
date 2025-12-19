"""
Loading skeleton components for better UX during data fetching.
"""
import streamlit as st


def loading_skeleton_card(count: int = 3) -> None:
    """
    Display skeleton loading cards.
    
    Args:
        count: Number of skeleton cards to display
    """
    for _ in range(count):
        st.markdown("""
        <div class="skeleton skeleton-card" style="height: 150px; margin-bottom: 1rem;"></div>
        """, unsafe_allow_html=True)


def loading_skeleton_table(rows: int = 5, cols: int = 4) -> None:
    """
    Display skeleton loading table.
    
    Args:
        rows: Number of rows
        cols: Number of columns
    """
    st.markdown("""
    <div style="background: var(--surface); padding: 1rem; border-radius: 8px;">
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div style="display: flex; gap: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
    for _ in range(cols):
        st.markdown('<div class="skeleton skeleton-text" style="flex: 1; height: 1.25rem;"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Rows
    for _ in range(rows):
        st.markdown('<div style="display: flex; gap: 1rem; margin-bottom: 0.75rem;">', unsafe_allow_html=True)
        for _ in range(cols):
            st.markdown('<div class="skeleton skeleton-text" style="flex: 1; height: 1rem;"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def loading_skeleton_text(lines: int = 3) -> None:
    """
    Display skeleton loading text lines.
    
    Args:
        lines: Number of text lines
    """
    for i in range(lines):
        width = "100%" if i == lines - 1 else f"{80 - i * 10}%"
        st.markdown(f"""
        <div class="skeleton skeleton-text" style="width: {width}; margin-bottom: 0.5rem;"></div>
        """, unsafe_allow_html=True)

