"""
Metrics Showcase Component - Demonstrates Enhanced st.metric Features.

This component showcases the enhanced st.metric capabilities with Markdown support,
sparklines, and advanced color schemes for testing and demonstration purposes.
"""

import streamlit as st
import numpy as np
from src.ui.enhanced_metrics import (
    EnhancedMetrics,
    MetricColorScheme,
    SparklineType,
    show_financial_dashboard,
    show_performance_dashboard
)


def render_metrics_showcase():
    """Render the metrics showcase component."""
    st.markdown("## 📊 Enhanced Metrics Showcase")
    st.markdown("Test the new Streamlit nightly st.metric features with Markdown support and sparklines.")
    
    # Basic Enhanced Metrics
    st.markdown("### Basic Enhanced Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        EnhancedMetrics.enhanced_metric(
            label="**Revenue**",
            value="**$125,430**",
            delta="+12.5%",
            delta_color=MetricColorScheme.SUCCESS,
            help="Total revenue for this month"
        )
    
    with col2:
        EnhancedMetrics.enhanced_metric(
            label="*Active Users*",
            value="*8,432*",
            delta="-2.1%",
            delta_color=MetricColorScheme.ERROR,
            help="Monthly active users"
        )
    
    with col3:
        EnhancedMetrics.enhanced_metric(
            label="**Conversion Rate**",
            value="**3.2%**",
            delta="+0.8%",
            delta_color=MetricColorScheme.SUCCESS,
            help="User conversion rate"
        )
    
    st.divider()
    
    # Sparkline Metrics
    st.markdown("### Metrics with Sparklines")
    
    # Generate sample data
    revenue_trend = [100000, 105000, 98000, 115000, 120000, 118000, 125430]
    users_trend = [8800, 8650, 8900, 8750, 8600, 8500, 8432]
    conversion_trend = [2.8, 2.9, 3.1, 3.0, 3.2, 3.1, 3.2]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        EnhancedMetrics.enhanced_metric(
            label="📈 **Revenue Trend**",
            value="**$125,430**",
            delta="+12.5%",
            delta_color=MetricColorScheme.SUCCESS,
            sparkline_data=revenue_trend,
            sparkline_type=SparklineType.AREA,
            sparkline_color="#00FF9D"
        )
    
    with col2:
        EnhancedMetrics.enhanced_metric(
            label="👥 **User Trend**",
            value="**8,432**",
            delta="-2.1%",
            delta_color=MetricColorScheme.ERROR,
            sparkline_data=users_trend,
            sparkline_type=SparklineType.LINE,
            sparkline_color="#FF0055"
        )
    
    with col3:
        EnhancedMetrics.enhanced_metric(
            label="🎯 **Conversion Trend**",
            value="**3.2%**",
            delta="+0.8%",
            delta_color=MetricColorScheme.SUCCESS,
            sparkline_data=conversion_trend,
            sparkline_type=SparklineType.BAR,
            sparkline_color="#FF8C00"
        )
    
    st.divider()
    
    # Different Sparkline Types
    st.markdown("### Different Sparkline Types")
    
    sample_data = [10, 15, 12, 18, 22, 19, 25, 23, 28, 30]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Line Sparkline**")
        EnhancedMetrics.enhanced_metric(
            label="Line Chart",
            value="30",
            delta="+200%",
            delta_color=MetricColorScheme.SUCCESS,
            sparkline_data=sample_data,
            sparkline_type=SparklineType.LINE,
            sparkline_color="#FF4500"
        )
    
    with col2:
        st.markdown("**Bar Sparkline**")
        EnhancedMetrics.enhanced_metric(
            label="Bar Chart",
            value="30",
            delta="+200%",
            delta_color=MetricColorScheme.SUCCESS,
            sparkline_data=sample_data,
            sparkline_type=SparklineType.BAR,
            sparkline_color="#FF4500"
        )
    
    with col3:
        st.markdown("**Area Sparkline**")
        EnhancedMetrics.enhanced_metric(
            label="Area Chart",
            value="30",
            delta="+200%",
            delta_color=MetricColorScheme.SUCCESS,
            sparkline_data=sample_data,
            sparkline_type=SparklineType.AREA,
            sparkline_color="#FF4500"
        )
    
    st.divider()
    
    # Color Schemes
    st.markdown("### Color Schemes")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        EnhancedMetrics.enhanced_metric(
            label="**Success**",
            value="**✅ Good**",
            delta="+15%",
            delta_color=MetricColorScheme.SUCCESS
        )
    
    with col2:
        EnhancedMetrics.enhanced_metric(
            label="**Warning**",
            value="**⚠️ Caution**",
            delta="+5%",
            delta_color=MetricColorScheme.WARNING
        )
    
    with col3:
        EnhancedMetrics.enhanced_metric(
            label="**Error**",
            value="**❌ Critical**",
            delta="-10%",
            delta_color=MetricColorScheme.ERROR
        )
    
    with col4:
        EnhancedMetrics.enhanced_metric(
            label="**Neutral**",
            value="**ℹ️ Info**",
            delta="0%",
            delta_color=MetricColorScheme.NEUTRAL
        )
    
    st.divider()
    
    # Financial Metrics Dashboard
    show_financial_dashboard()
    
    st.divider()
    
    # Performance Metrics Dashboard
    show_performance_dashboard()
    
    st.divider()
    
    # Interactive Metrics Grid
    st.markdown("### Interactive Metrics Grid")
    
    if st.button("🔄 Generate New Data", use_container_width=True):
        st.session_state["metrics_data_refresh"] = True
        st.rerun()
    
    # Generate or use cached data
    if "metrics_data_refresh" not in st.session_state:
        st.session_state["metrics_data_refresh"] = True
    
    if st.session_state["metrics_data_refresh"]:
        # Generate random metrics data
        metrics_data = []
        
        for i in range(6):
            base_value = np.random.randint(1000, 10000)
            trend_data = [base_value + np.random.randint(-500, 500) for _ in range(7)]
            delta_value = np.random.uniform(-20, 20)
            
            # Determine color based on delta
            if delta_value > 10:
                color = MetricColorScheme.SUCCESS
            elif delta_value < -10:
                color = MetricColorScheme.ERROR
            elif abs(delta_value) > 5:
                color = MetricColorScheme.WARNING
            else:
                color = MetricColorScheme.NEUTRAL
            
            metrics_data.append({
                "label": f"**Metric {i+1}**",
                "value": f"**{base_value:,}**",
                "delta": f"{delta_value:+.1f}%",
                "delta_color": color,
                "sparkline_data": trend_data,
                "sparkline_color": "#FF4500"
            })
        
        st.session_state["cached_metrics"] = metrics_data
        st.session_state["metrics_data_refresh"] = False
    
    # Display metrics grid
    EnhancedMetrics.metric_grid(
        metrics=st.session_state.get("cached_metrics", []),
        columns=3,
        spacing="medium"
    )
    
    st.divider()
    
    # Markdown Formatting Examples
    st.markdown("### Markdown Formatting Examples")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Rich Text Labels:**")
        EnhancedMetrics.enhanced_metric(
            label="🚀 **Launch** *Success*",
            value="**100%** ✅",
            delta="+50%",
            delta_color=MetricColorScheme.SUCCESS
        )
        
        EnhancedMetrics.enhanced_metric(
            label="💰 *Revenue* **Growth**",
            value="***$1.2M***",
            delta="+25%",
            delta_color=MetricColorScheme.SUCCESS
        )
    
    with col2:
        st.markdown("**Emoji Integration:**")
        EnhancedMetrics.enhanced_metric(
            label="🎯 **Target** Achievement",
            value="**95%** 🎉",
            delta="+5%",
            delta_color=MetricColorScheme.SUCCESS
        )
        
        EnhancedMetrics.enhanced_metric(
            label="⚡ **Performance** Score",
            value="**A+** ⭐",
            delta="Excellent",
            delta_color=MetricColorScheme.SUCCESS
        )


def add_enhanced_metrics_to_dashboard():
    """Add enhanced metrics examples to existing dashboard components."""
    
    st.markdown("### Enhanced Dashboard Metrics")
    
    # Sample FinOps metrics with sparklines
    cost_trend = [42000, 43500, 41000, 45000, 47000, 45000, 48000]
    efficiency_trend = [85, 87, 83, 89, 91, 88, 92]
    savings_trend = [2000, 2500, 3000, 2800, 3200, 3500, 4000]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        EnhancedMetrics.financial_metric(
            label="💸 **Monthly Spend**",
            amount=48000,
            delta=12.5,
            sparkline_data=cost_trend,
            trend_color="#FF0055"
        )
    
    with col2:
        EnhancedMetrics.performance_metric(
            label="⚡ **Efficiency**",
            value=92,
            unit="%",
            target=85,
            sparkline_data=efficiency_trend,
            format_type="percentage"
        )
    
    with col3:
        EnhancedMetrics.financial_metric(
            label="💰 **Cost Savings**",
            amount=4000,
            delta=25.8,
            sparkline_data=savings_trend,
            trend_color="#00FF9D"
        )