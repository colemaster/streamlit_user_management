"""
Enhanced Metrics Components for Streamlit Nightly 2026.

Implements enhanced st.metric with Markdown support, sparklines, and advanced
color schemes using the latest Streamlit nightly features.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, List, Union, Dict, Any
from enum import Enum
import numpy as np


class MetricColorScheme(Enum):
    """Color schemes for enhanced metrics."""
    SUCCESS = "normal"  # Green for positive metrics
    WARNING = "inverse"  # Orange/yellow for warning metrics
    ERROR = "off"       # Red for error/negative metrics
    NEUTRAL = "normal"  # Default neutral colors


class SparklineType(Enum):
    """Types of sparkline charts."""
    LINE = "line"
    BAR = "bar"
    AREA = "area"


class EnhancedMetrics:
    """
    Enhanced metrics component using Streamlit nightly 2026 features.
    
    Provides advanced st.metric functionality with:
    - Markdown support in labels and values
    - Sparkline chart integration
    - Advanced color schemes and delta arrows
    - Custom styling and animations
    """
    
    @staticmethod
    def create_sparkline_data(
        values: List[float],
        chart_type: SparklineType = SparklineType.LINE,
        color: str = "#FF4500"
    ) -> go.Figure:
        """
        Create sparkline chart data for st.metric integration.
        
        Args:
            values: List of numeric values for the sparkline
            chart_type: Type of sparkline chart
            color: Color for the sparkline
            
        Returns:
            Plotly figure optimized for sparkline display
        """
        fig = go.Figure()
        
        if chart_type == SparklineType.LINE:
            fig.add_trace(go.Scatter(
                y=values,
                mode='lines',
                line=dict(color=color, width=2),
                fill='tonexty' if len(values) > 1 else None,
                fillcolor=f"rgba{tuple(list(px.colors.hex_to_rgb(color)) + [0.2])}",
                showlegend=False,
                hovertemplate='<b>%{y}</b><extra></extra>'
            ))
        elif chart_type == SparklineType.BAR:
            fig.add_trace(go.Bar(
                y=values,
                marker_color=color,
                showlegend=False,
                hovertemplate='<b>%{y}</b><extra></extra>'
            ))
        elif chart_type == SparklineType.AREA:
            fig.add_trace(go.Scatter(
                y=values,
                mode='lines',
                line=dict(color=color, width=1),
                fill='tozeroy',
                fillcolor=f"rgba{tuple(list(px.colors.hex_to_rgb(color)) + [0.3])}",
                showlegend=False,
                hovertemplate='<b>%{y}</b><extra></extra>'
            ))
        
        # Optimize for sparkline display
        fig.update_layout(
            height=60,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                showticklabels=False,
                zeroline=False,
                visible=False
            ),
            yaxis=dict(
                showgrid=False,
                showticklabels=False,
                zeroline=False,
                visible=False
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        return fig
    
    @staticmethod
    def enhanced_metric(
        label: Union[str, None] = None,
        value: Union[str, int, float, None] = None,
        delta: Union[str, int, float, None] = None,
        delta_color: MetricColorScheme = MetricColorScheme.NEUTRAL,
        help: Optional[str] = None,
        label_visibility: str = "visible",
        sparkline_data: Optional[List[float]] = None,
        sparkline_type: SparklineType = SparklineType.LINE,
        sparkline_color: str = "#FF4500",
        markdown_label: bool = True,
        markdown_value: bool = True,
        custom_styling: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Create an enhanced metric using Streamlit nightly 2026 features.
        
        Args:
            label: Metric label (supports Markdown if markdown_label=True)
            value: Metric value (supports Markdown if markdown_value=True)
            delta: Delta value for comparison
            delta_color: Color scheme for delta display
            help: Help text for the metric
            label_visibility: Visibility of the label
            sparkline_data: Data for sparkline chart
            sparkline_type: Type of sparkline chart
            sparkline_color: Color for sparkline
            markdown_label: Enable Markdown in label
            markdown_value: Enable Markdown in value
            custom_styling: Custom CSS styling options
        """
        # Prepare chart data for sparkline
        chart_data = None
        if sparkline_data:
            chart_data = EnhancedMetrics.create_sparkline_data(
                sparkline_data, sparkline_type, sparkline_color
            )
        
        # Format label with Markdown support
        formatted_label = label
        if markdown_label and label:
            # Convert simple formatting to Markdown
            if not label.startswith('**') and not label.startswith('*'):
                formatted_label = f"**{label}**"
        
        # Format value with Markdown support
        formatted_value = value
        if markdown_value and isinstance(value, str):
            # Add emphasis for large numbers or special formatting
            if any(char in str(value) for char in ['$', '%', 'k', 'M', 'B']):
                formatted_value = f"**{value}**"
        
        # Use enhanced st.metric with new features
        try:
            # Streamlit nightly 2026 enhanced st.metric
            st.metric(
                label=formatted_label,
                value=formatted_value,
                delta=delta,
                delta_color=delta_color.value,
                help=help,
                label_visibility=label_visibility,
                chart_data=chart_data  # New sparkline parameter
            )
        except TypeError:
            # Fallback for older Streamlit versions
            st.metric(
                label=formatted_label,
                value=formatted_value,
                delta=delta,
                delta_color=delta_color.value if hasattr(delta_color, 'value') else "normal",
                help=help,
                label_visibility=label_visibility
            )
            
            # Show sparkline separately if not supported
            if sparkline_data:
                st.plotly_chart(chart_data, use_container_width=True, config={'displayModeBar': False})
    
    @staticmethod
    def metric_grid(
        metrics: List[Dict[str, Any]],
        columns: int = 3,
        spacing: str = "medium"
    ) -> None:
        """
        Create a grid of enhanced metrics.
        
        Args:
            metrics: List of metric configurations
            columns: Number of columns in the grid
            spacing: Spacing between metrics ("small", "medium", "large")
        """
        # Create columns
        cols = st.columns(columns)
        
        for i, metric_config in enumerate(metrics):
            col_index = i % columns
            
            with cols[col_index]:
                EnhancedMetrics.enhanced_metric(**metric_config)
                
                # Add spacing
                if spacing == "small":
                    st.markdown("<br>", unsafe_allow_html=True)
                elif spacing == "medium":
                    st.markdown("<br><br>", unsafe_allow_html=True)
                elif spacing == "large":
                    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    @staticmethod
    def financial_metric(
        label: str,
        amount: float,
        currency: str = "USD",
        delta: Optional[float] = None,
        delta_percentage: bool = True,
        sparkline_data: Optional[List[float]] = None,
        trend_color: str = "#FF4500"
    ) -> None:
        """
        Create a financial metric with proper formatting.
        
        Args:
            label: Metric label
            amount: Financial amount
            currency: Currency code
            delta: Change amount
            delta_percentage: Show delta as percentage
            sparkline_data: Historical data for sparkline
            trend_color: Color for trend visualization
        """
        # Format currency
        if currency == "USD":
            formatted_value = f"${amount:,.0f}"
        else:
            formatted_value = f"{amount:,.0f} {currency}"
        
        # Format delta
        formatted_delta = None
        delta_color = MetricColorScheme.NEUTRAL
        
        if delta is not None:
            if delta_percentage:
                formatted_delta = f"{delta:+.1f}%"
            else:
                formatted_delta = f"${delta:+,.0f}"
            
            # Determine color based on delta
            if delta > 0:
                delta_color = MetricColorScheme.SUCCESS
            elif delta < 0:
                delta_color = MetricColorScheme.ERROR
        
        EnhancedMetrics.enhanced_metric(
            label=label,
            value=formatted_value,
            delta=formatted_delta,
            delta_color=delta_color,
            sparkline_data=sparkline_data,
            sparkline_color=trend_color,
            markdown_label=True,
            markdown_value=True
        )
    
    @staticmethod
    def performance_metric(
        label: str,
        value: Union[int, float],
        unit: str = "",
        target: Optional[float] = None,
        sparkline_data: Optional[List[float]] = None,
        format_type: str = "number"  # "number", "percentage", "duration"
    ) -> None:
        """
        Create a performance metric with target comparison.
        
        Args:
            label: Metric label
            value: Performance value
            unit: Unit of measurement
            target: Target value for comparison
            sparkline_data: Historical performance data
            format_type: How to format the value
        """
        # Format value based on type
        if format_type == "percentage":
            formatted_value = f"{value:.1f}%"
        elif format_type == "duration":
            if value < 1:
                formatted_value = f"{value*1000:.0f}ms"
            elif value < 60:
                formatted_value = f"{value:.1f}s"
            else:
                formatted_value = f"{value/60:.1f}m"
        else:
            formatted_value = f"{value:,.0f}{unit}"
        
        # Calculate delta against target
        formatted_delta = None
        delta_color = MetricColorScheme.NEUTRAL
        
        if target is not None:
            delta_pct = ((value - target) / target) * 100
            formatted_delta = f"{delta_pct:+.1f}% vs target"
            
            # Color based on whether we're above or below target
            # For performance metrics, being above target is usually good
            if delta_pct > 0:
                delta_color = MetricColorScheme.SUCCESS
            elif delta_pct < -10:  # More than 10% below target
                delta_color = MetricColorScheme.ERROR
            elif delta_pct < 0:
                delta_color = MetricColorScheme.WARNING
        
        EnhancedMetrics.enhanced_metric(
            label=label,
            value=formatted_value,
            delta=formatted_delta,
            delta_color=delta_color,
            sparkline_data=sparkline_data,
            sparkline_color="#00FF9D" if delta_color == MetricColorScheme.SUCCESS else "#FF4500",
            markdown_label=True,
            markdown_value=True
        )


# Convenience functions for common metric patterns
def show_financial_dashboard():
    """Show a sample financial metrics dashboard."""
    st.markdown("### 💰 Financial Metrics Dashboard")
    
    # Sample data
    spend_data = [42000, 43500, 41000, 45000, 47000, 45000, 48000]
    forecast_data = [48000, 49000, 50000, 51000, 52000, 53000, 54000]
    savings_data = [2000, 2500, 3000, 2800, 3200, 3500, 4000]
    
    metrics = [
        {
            "label": "💸 **Total Spend**",
            "amount": 45000,
            "delta": 12.5,
            "sparkline_data": spend_data,
            "trend_color": "#FF0055"
        },
        {
            "label": "📈 **Forecast**",
            "amount": 52000,
            "delta": 8.2,
            "sparkline_data": forecast_data,
            "trend_color": "#FF8C00"
        },
        {
            "label": "💰 **Savings**",
            "amount": 3500,
            "delta": 15.8,
            "sparkline_data": savings_data,
            "trend_color": "#00FF9D"
        }
    ]
    
    cols = st.columns(3)
    for i, metric in enumerate(metrics):
        with cols[i]:
            EnhancedMetrics.financial_metric(**metric)


def show_performance_dashboard():
    """Show a sample performance metrics dashboard."""
    st.markdown("### ⚡ Performance Metrics Dashboard")
    
    # Sample performance data
    response_times = [0.12, 0.15, 0.11, 0.13, 0.14, 0.12, 0.10]
    throughput_data = [1200, 1350, 1180, 1420, 1380, 1450, 1500]
    error_rates = [0.5, 0.3, 0.8, 0.2, 0.1, 0.4, 0.2]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        EnhancedMetrics.performance_metric(
            label="🚀 **Response Time**",
            value=0.12,
            target=0.15,
            sparkline_data=response_times,
            format_type="duration"
        )
    
    with col2:
        EnhancedMetrics.performance_metric(
            label="📊 **Throughput**",
            value=1500,
            unit=" req/s",
            target=1200,
            sparkline_data=throughput_data,
            format_type="number"
        )
    
    with col3:
        EnhancedMetrics.performance_metric(
            label="⚠️ **Error Rate**",
            value=0.2,
            target=0.5,
            sparkline_data=error_rates,
            format_type="percentage"
        )