import streamlit as st


def render_metric_card(
    label: str, value: str, delta: str = None, delta_color: str = "neutral"
):
    """
    Renders a custom metric card with glassmorphism effect.

    Args:
        label: The title of the metric
        value: The main value to display
        delta: Optional change value (e.g. "+5%")
        delta_color: One of "success", "error", "neutral"
    """
    delta_html = ""
    if delta:
        color_class = {
            "success": "delta-up",
            "error": "delta-down",
            "neutral": "delta-neutral",
        }.get(delta_color, "delta-neutral")

        arrow = (
            "↑" if delta_color == "success" else "↓" if delta_color == "error" else ""
        )
        delta_html = f'<span class="metric-delta {color_class}">{arrow} {delta}</span>'

    st.markdown(
        f"""
    <div class="glass-card animate-enter">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_status_badge(status: str, label: str):
    """
    Renders a status badge.
    """
    colors = {
        "active": "#00D16C",
        "inactive": "#A0A5AA",
        "warning": "#FFB020",
        "error": "#FF3333",
    }
    color = colors.get(status.lower(), "#A0A5AA")

    st.markdown(
        f"""
    <div style="display: inline-flex; align-items: center; background: {color}20; padding: 4px 12px; border-radius: 20px; border: 1px solid {color}40;">
        <span style="width: 8px; height: 8px; border-radius: 50%; background: {color}; margin-right: 8px; box-shadow: 0 0 8px {color};"></span>
        <span style="color: {color}; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.05em;">{label.upper()}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )


def animated_header(title: str, subtitle: str = None):
    """
    Renders an animated header section.
    """
    subtitle_html = (
        f'<p style="color: var(--text-secondary); margin-top: 4px; font-size: 1.1rem;">{subtitle}</p>'
        if subtitle
        else ""
    )

    st.markdown(
        f"""
    <div style="margin-bottom: 2rem; animation: fadeIn 0.8s ease-out;">
        <h1 style="font-size: 3rem; margin-bottom: 0; background: linear-gradient(90deg, #fff, #aaa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1>
        {subtitle_html}
        <div style="height: 4px; width: 60px; background: var(--accent-primary); margin-top: 1rem; border-radius: 2px;"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )
