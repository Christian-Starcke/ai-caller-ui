"""
Chart configuration and theme utilities for Plotly.
"""
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px


# Professional color palette
COLOR_PALETTE = [
    "#2563eb",  # Primary blue
    "#10b981",  # Success green
    "#f59e0b",  # Warning amber
    "#ef4444",  # Error red
    "#8b5cf6",  # Purple
    "#06b6d4",  # Cyan
    "#f97316",  # Orange
    "#84cc16",  # Lime
]


def apply_professional_theme():
    """Apply professional theme to all Plotly charts."""
    # Create custom template
    pio.templates["ai_caller"] = go.layout.Template(
        layout=go.Layout(
            font=dict(
                family="Inter, system-ui, -apple-system, sans-serif",
                size=12,
                color="#1e293b"
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            colorway=COLOR_PALETTE,
            xaxis=dict(
                showgrid=True,
                gridcolor="#e2e8f0",
                gridwidth=1,
                zeroline=False,
                linecolor="#e2e8f0",
                linewidth=1
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#e2e8f0",
                gridwidth=1,
                zeroline=False,
                linecolor="#e2e8f0",
                linewidth=1
            ),
            legend=dict(
                bgcolor="white",
                bordercolor="#e2e8f0",
                borderwidth=1,
                font=dict(size=11)
            ),
            hovermode="closest",
            hoverlabel=dict(
                bgcolor="white",
                bordercolor="#2563eb",
                font_size=12,
                font_family="Inter, system-ui, sans-serif"
            )
        )
    )
    
    # Set as default
    pio.templates.default = "ai_caller"


def create_bar_chart(
    x_data,
    y_data,
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    color: str = None
) -> go.Figure:
    """Create a professional bar chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=x_data,
        y=y_data,
        marker_color=color or COLOR_PALETTE[0],
        marker_line_color=color or COLOR_PALETTE[0],
        marker_line_width=0,
        text=y_data,
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Value: %{y}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color="#1e293b"),
            x=0.5,
            xanchor="center"
        ),
        xaxis_title=x_label,
        yaxis_title=y_label,
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    
    return fig


def create_line_chart(
    x_data,
    y_data,
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    color: str = None
) -> go.Figure:
    """Create a professional line chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode="lines+markers",
        line=dict(color=color or COLOR_PALETTE[0], width=3),
        marker=dict(size=8, color=color or COLOR_PALETTE[0]),
        hovertemplate="<b>%{x}</b><br>Value: %{y}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color="#1e293b"),
            x=0.5,
            xanchor="center"
        ),
        xaxis_title=x_label,
        yaxis_title=y_label,
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    
    return fig


def create_pie_chart(
    labels,
    values,
    title: str = "",
    colors: list = None
) -> go.Figure:
    """Create a professional pie chart."""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4 if len(labels) <= 4 else 0,
        marker=dict(colors=colors or COLOR_PALETTE[:len(labels)]),
        textinfo="label+percent",
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>Value: %{value}<br>Percent: %{percent}<extra></extra>"
    )])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color="#1e293b"),
            x=0.5,
            xanchor="center"
        ),
        showlegend=True,
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


# Initialize theme on import
apply_professional_theme()

