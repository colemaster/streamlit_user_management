import streamlit as st
import time
from src.ui.enhanced_metrics import EnhancedMetrics, MetricColorScheme


def render_metric_card(
    label: str,
    value: str,
    delta: str = None,
    delta_color: str = "neutral",
    delay: float = 0,
    sparkline_data: list = None,
):
    """
    Renders a Brave Design metric card with enhanced st.metric features.
    
    Now uses Streamlit nightly 2026 enhanced st.metric with:
    - Markdown support in labels and values
    - Sparkline chart integration
    - Advanced color schemes
    """
    # Map old color system to new MetricColorScheme
    color_mapping = {
        "success": MetricColorScheme.SUCCESS,
        "error": MetricColorScheme.ERROR,
        "warning": MetricColorScheme.WARNING,
        "neutral": MetricColorScheme.NEUTRAL,
    }
    
    metric_color = color_mapping.get(delta_color, MetricColorScheme.NEUTRAL)
    
    # Add animation delay using custom CSS if needed
    if delay > 0:
        st.markdown(
            f"""
            <style>
            .metric-container {{
                animation-delay: {delay}s;
                animation: fadeInUp 0.6s ease-out both;
            }}
            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(20px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    # Use enhanced metric with Markdown and sparkline support
    EnhancedMetrics.enhanced_metric(
        label=f"**{label}**",  # Markdown formatting
        value=f"**{value}**",  # Markdown formatting
        delta=delta,
        delta_color=metric_color,
        sparkline_data=sparkline_data,
        sparkline_color="#FF4500",  # Brave Design orange
        markdown_label=True,
        markdown_value=True
    )


def render_action_group():
    """Renders 3 modern action buttons."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("🚀 DEPLOY", type="primary", use_container_width=True)
    with col2:
        st.button("⚡ OPTIMIZE", use_container_width=True)
    with col3:
        st.button("🔍 AUDIT", use_container_width=True)


def render_status_badge(status: str, label: str):
    """
    Renders a neon status badge.
    """
    status_lower = status.lower()

    color_map = {
        "active": "#00FF9D",
        "inactive": "#666",
        "warning": "#FFD700",
        "error": "#FF0055",
    }
    color = color_map.get(status_lower, "#666")

    st.markdown(
        f"""
    <div style="
        display: inline-flex;
        align-items: center;
        padding: 4px 16px;
        border-radius: 4px;
        background: rgba(0,0,0,0.5);
        border: 1px solid {color};
        color: {color};
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        letter-spacing: 0.1em;
        box-shadow: 0 0 10px {color}40;
    ">
        <span style="width: 8px; height: 8px; background: {color}; border-radius: 50%; margin-right: 8px; box-shadow: 0 0 8px {color};"></span>
        {label.upper()}
    </div>
    """,
        unsafe_allow_html=True,
    )


def animated_header(title: str, subtitle: str = None):
    """
    Renders a 3D animated metallic header.
    """
    subtitle_html = (
        f'<div class="metallic-subtitle" style="margin-top: -10px; font-size: 1.2rem; animation: slideIn 1.2s ease-out;">{subtitle}</div>'
        if subtitle
        else ""
    )

    st.html(
        f"""
    <div style="margin-bottom: 3rem; animation: fadeIn 1s ease-out; text-align: left;">
        <h1 class="metallic-title" style="font-size: 5.5rem; line-height: 1; margin: 0;">{title}</h1>
        {subtitle_html}
        <div style="height: 2px; width: 100%; background: linear-gradient(90deg, var(--accent-primary), transparent); margin-top: 1.5rem; box-shadow: 0 0 10px var(--accent-primary);"></div>
    </div>
    """
    )
