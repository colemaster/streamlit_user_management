import streamlit as st
import pandas as pd
import numpy as np
from src.ui.cards.engine import register_card
from src.nexus.protocol import NexusCardState
from src.ui.components import render_metric_card

# --------------------------------------------------------------------------
#                                 CORE CARDS
# --------------------------------------------------------------------------


@register_card("metric-card")
@st.fragment
def render_metric(card: NexusCardState):
    """
    Enhanced Metric Card with sparkline support.
    
    Data Expectation: {
        'value': str, 
        'delta': str, 
        'color': str,
        'sparkline_data': list (optional),
        'sparkline_type': str (optional)
    }
    """
    from src.ui.enhanced_metrics import EnhancedMetrics, MetricColorScheme
    
    val = card.data.get("value", "N/A")
    delta = card.data.get("delta", None)
    color = card.data.get("color", "neutral")
    sparkline_data = card.data.get("sparkline_data", None)
    
    # Map color to MetricColorScheme
    color_mapping = {
        "success": MetricColorScheme.SUCCESS,
        "error": MetricColorScheme.ERROR,
        "warning": MetricColorScheme.WARNING,
        "neutral": MetricColorScheme.NEUTRAL,
    }
    
    metric_color = color_mapping.get(color, MetricColorScheme.NEUTRAL)
    
    # Use enhanced metric with sparkline support
    EnhancedMetrics.enhanced_metric(
        label=f"**{card.title}**",
        value=f"**{val}**",
        delta=delta,
        delta_color=metric_color,
        sparkline_data=sparkline_data,
        sparkline_color="#FF4500",  # Brave Design orange
        markdown_label=True,
        markdown_value=True
    )


@register_card("cost-chart")
@st.fragment
def render_cost_chart(card: NexusCardState):
    """
    Interactive Cost Chart.
    Data Expectation: {'filter_service': str, 'days': int}
    """
    st.markdown(f'<div class="brave-card">', unsafe_allow_html=True)
    st.markdown(f"**{card.title}**")

    service_filter = card.data.get("filter_service", "All")
    days = card.data.get("days", 30)

    # Mock Data Generation based on filter
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days)
    base = 100 if service_filter == "All" else 50
    values = np.random.normal(base, 10, size=days).cumsum()
    values = np.maximum(values, 0)

    df = pd.DataFrame({"Date": dates, "Cost": values})

    st.area_chart(df, x="Date", y="Cost", color="#FF4500", use_container_width=True)

    # Dynamic Controls inside the card
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Refresh", key=f"refresh_{card.id}"):
            st.toast("Refreshing Data...")
    with col2:
        st.caption(f"Filter: {service_filter}")

    st.markdown("</div>", unsafe_allow_html=True)


@register_card("anomaly-feed")
@st.fragment
def render_anomalies(card: NexusCardState):
    """
    Live Anomaly Feed.
    """
    st.markdown(f'<div class="brave-card">', unsafe_allow_html=True)
    st.markdown(
        f"**{card.title}** <span style='color:var(--error); float:right;'>LIVE</span>",
        unsafe_allow_html=True,
    )

    anomalies = [
        {
            "service": "EC2",
            "cost": "$450",
            "reason": "Instance Spike",
            "time": "2m ago",
        },
        {"service": "RDS", "cost": "$120", "reason": "IOPS Burst", "time": "15m ago"},
    ]

    for a in anomalies:
        st.markdown(
            f"""
            <div style="border-left: 2px solid #FF0055; padding-left: 10px; margin-bottom: 8px; background: rgba(255,0,85,0.05);">
                <div style="font-weight: 600; font-size: 0.9rem;">{a["service"]} - {a["cost"]}</div>
                <div style="font-size: 0.8rem; color: #888;">{a["reason"]} • {a["time"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("Investigate All", key=f"inv_{card.id}", use_container_width=True):
        st.toast("Opening Investigation Agent...")

    st.markdown("</div>", unsafe_allow_html=True)
