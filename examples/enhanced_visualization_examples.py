"""
Enhanced Visualization Examples
Comprehensive examples demonstrating all features of the enhanced VisualEnhancementEngine.

This file provides practical examples of:
- Interactive chart creation with advanced features
- Animation and transition support
- Sparkline integration for st.metric
- Error handling and fallback mechanisms
- Performance optimization
- Responsive design
- Accessibility features
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.ui.visual_enhancement_engine import (
    VisualEnhancementEngine,
    ChartType,
    ChartConfig,
    BraveThemeConfig,
    AnimationType,
    ResponsiveBreakpoint
)


def create_sample_data():
    """Create comprehensive sample datasets for examples"""
    
    # Time series data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    time_series = pd.DataFrame({
        'date': dates,
        'revenue': np.cumsum(np.random.randn(100) * 1000) + 50000,
        'costs': np.cumsum(np.random.randn(100) * 800) + 30000,
        'users': np.cumsum(np.random.randint(-50, 100, 100)) + 10000,
        'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'product': np.random.choice(['Product A', 'Product B', 'Product C'], 100)
    })
    
    # Hierarchical data for sunburst/treemap
    hierarchical_data = pd.DataFrame([
        {'ids': 'Total', 'parents': '', 'values': 1000000},
        {'ids': 'Sales', 'parents': 'Total', 'values': 600000},
        {'ids': 'Marketing', 'parents': 'Total', 'values': 250000},
        {'ids': 'Operations', 'parents': 'Total', 'values': 150000},
        {'ids': 'Online Sales', 'parents': 'Sales', 'values': 400000},
        {'ids': 'Retail Sales', 'parents': 'Sales', 'values': 200000},
        {'ids': 'Digital Marketing', 'parents': 'Marketing', 'values': 150000},
        {'ids': 'Traditional Marketing', 'parents': 'Marketing', 'values': 100000},
        {'ids': 'IT Operations', 'parents': 'Operations', 'values': 80000},
        {'ids': 'Facilities', 'parents': 'Operations', 'values': 70000}
    ])
    
    # Flow data for Sankey diagrams
    flow_data = pd.DataFrame([
        {'source': 'Budget', 'target': 'Development', 'value': 300000},
        {'source': 'Budget', 'target': 'Marketing', 'value': 200000},
        {'source': 'Budget', 'target': 'Operations', 'value': 150000},
        {'source': 'Development', 'target': 'Frontend', 'value': 120000},
        {'source': 'Development', 'target': 'Backend', 'value': 100000},
        {'source': 'Development', 'target': 'DevOps', 'value': 80000},
        {'source': 'Marketing', 'target': 'Digital Ads', 'value': 120000},
        {'source': 'Marketing', 'target': 'Content', 'value': 80000},
        {'source': 'Operations', 'target': 'Infrastructure', 'value': 90000},
        {'source': 'Operations', 'target': 'Support', 'value': 60000}
    ])
    
    return time_series, hierarchical_data, flow_data


def example_1_basic_interactive_charts():
    """Example 1: Basic interactive charts with enhanced features"""
    st.header("Example 1: Enhanced Interactive Charts")
    
    # Initialize engine with custom theme
    theme = BraveThemeConfig(
        animation_duration=750,
        high_contrast=False,
        reduced_motion=False
    )
    engine = VisualEnhancementEngine(theme=theme)
    
    # Get sample data
    time_series, _, _ = create_sample_data()
    
    # Create different chart types
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Enhanced Line Chart")
        
        config = ChartConfig(
            chart_type=ChartType.LINE,
            title="Revenue Trend Over Time",
            animation_type=AnimationType.SMOOTH,
            height=400,
            hover_enabled=True,
            zoom_enabled=True,
            responsive=True,
            accessibility=True
        )
        
        fig = engine.create_line_chart(
            data=time_series,
            x='date',
            y='revenue',
            color='region',
            config=config
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Enhanced Bar Chart")
        
        # Aggregate data for bar chart
        bar_data = time_series.groupby('region')['revenue'].sum().reset_index()
        
        config = ChartConfig(
            chart_type=ChartType.BAR,
            title="Revenue by Region",
            animation_type=AnimationType.BOUNCE,
            height=400,
            hover_enabled=True,
            responsive=True
        )
        
        fig = engine.create_bar_chart(
            data=bar_data,
            x='region',
            y='revenue',
            config=config
        )
        
        st.plotly_chart(fig, use_container_width=True)


def example_2_advanced_animations():
    """Example 2: Advanced animation types and transitions"""
    st.header("Example 2: Advanced Animation Types")
    
    engine = VisualEnhancementEngine()
    time_series, _, _ = create_sample_data()
    
    # Animation type selector
    animation_type = st.selectbox(
        "Select Animation Type",
        [AnimationType.SMOOTH, AnimationType.FADE_IN, AnimationType.SLIDE_IN,
         AnimationType.ZOOM_IN, AnimationType.BOUNCE, AnimationType.ELASTIC]
    )
    
    config = ChartConfig(
        chart_type=ChartType.AREA,
        title=f"Area Chart with {animation_type.value.title()} Animation",
        animation_type=animation_type,
        height=500,
        animations=True
    )
    
    fig = engine.create_area_chart(
        data=time_series,
        x='date',
        y='revenue',
        color='product',
        config=config
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show animation details
    st.info(f"Current animation: {animation_type.value} with {engine.theme.animation_duration}ms duration")


def example_3_enhanced_sparklines():
    """Example 3: Enhanced sparklines for st.metric integration"""
    st.header("Example 3: Enhanced Sparklines for Metrics")
    
    engine = VisualEnhancementEngine()
    
    # Generate sample metric data
    metrics_data = [
        {
            'label': 'Monthly Revenue',
            'value': '$127,450',
            'delta': '+12.3%',
            'sparkline_data': [100000, 105000, 108000, 112000, 115000, 120000, 118000, 127450],
            'trend_type': 'auto'
        },
        {
            'label': 'Active Users',
            'value': '45,230',
            'delta': '+8.7%',
            'sparkline_data': [40000, 41000, 42500, 43200, 44100, 44800, 45100, 45230],
            'trend_type': 'positive'
        },
        {
            'label': 'Conversion Rate',
            'value': '3.42%',
            'delta': '-0.3%',
            'sparkline_data': [3.8, 3.7, 3.6, 3.5, 3.4, 3.45, 3.43, 3.42],
            'trend_type': 'negative'
        },
        {
            'label': 'Customer Satisfaction',
            'value': '4.7/5.0',
            'delta': '+0.1',
            'sparkline_data': [4.5, 4.6, 4.6, 4.7, 4.6, 4.7, 4.7, 4.7],
            'trend_type': 'neutral'
        }
    ]
    
    # Display enhanced metrics
    cols = st.columns(len(metrics_data))
    
    for i, metric in enumerate(metrics_data):
        with cols[i]:
            # Create enhanced metric display
            enhanced_metric = engine.create_enhanced_metric_display(
                label=metric['label'],
                value=metric['value'],
                delta=metric['delta'],
                sparkline_data=metric['sparkline_data'],
                trend_analysis=True
            )
            
            # Display metric
            st.metric(
                label=enhanced_metric['label'],
                value=enhanced_metric['value'],
                delta=enhanced_metric['delta']
            )
            
            # Display sparkline
            if enhanced_metric['sparkline']:
                st.plotly_chart(enhanced_metric['sparkline'], use_container_width=True)
            
            # Display trend analysis
            if enhanced_metric['trend_info']:
                trend_info = enhanced_metric['trend_info']
                st.caption(f"Trend: {trend_info['trend']} | Volatility: {trend_info['volatility']:.2f}")


def example_4_error_handling_fallbacks():
    """Example 4: Error handling and fallback mechanisms"""
    st.header("Example 4: Error Handling & Fallback Mechanisms")
    
    engine = VisualEnhancementEngine()
    
    st.subheader("Fallback Demonstration")
    
    # Create intentionally problematic data
    problematic_data = pd.DataFrame({
        'x': [1, 2, None, 4, 5],  # Contains None values
        'y': ['a', 'b', 'c', 'd', 'e'],  # Non-numeric for numeric chart
        'category': ['A', 'B', 'C', 'D', 'E']
    })
    
    config = ChartConfig(
        chart_type=ChartType.SCATTER,
        title="Chart with Fallback Handling",
        fallback_enabled=True,
        height=400
    )
    
    try:
        # This will likely fail due to data issues, triggering fallback
        fig = engine.create_chart_with_fallback(
            chart_type=ChartType.SCATTER,
            data=problematic_data,
            config=config,
            fallback_type=ChartType.BAR,
            x='category',
            y='x'  # Using the numeric column
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.success("Chart created successfully (possibly using fallback)")
        
    except Exception as e:
        st.error(f"Chart creation failed: {str(e)}")
    
    # Show performance metrics
    metrics = engine.get_performance_metrics()
    if metrics.get('status') != 'no_data':
        st.subheader("Performance Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Charts Rendered", metrics['total_charts_rendered'])
        with col2:
            st.metric("Error Count", metrics['error_count'])
        with col3:
            st.metric("Error Rate", f"{metrics['error_rate']:.1%}")


def example_5_batch_processing():
    """Example 5: Batch chart creation and processing"""
    st.header("Example 5: Batch Chart Processing")
    
    engine = VisualEnhancementEngine()
    time_series, hierarchical_data, flow_data = create_sample_data()
    
    # Define multiple chart specifications
    chart_specs = [
        {
            'chart_type': ChartType.LINE,
            'data': time_series,
            'config': ChartConfig(
                chart_type=ChartType.LINE,
                title="Revenue Trend",
                height=300
            ),
            'kwargs': {'x': 'date', 'y': 'revenue'}
        },
        {
            'chart_type': ChartType.PIE,
            'data': time_series.groupby('region')['revenue'].sum().reset_index(),
            'config': ChartConfig(
                chart_type=ChartType.PIE,
                title="Revenue by Region",
                height=300
            ),
            'kwargs': {'values': 'revenue', 'names': 'region'}
        },
        {
            'chart_type': ChartType.SUNBURST,
            'data': hierarchical_data,
            'config': ChartConfig(
                chart_type=ChartType.SUNBURST,
                title="Organizational Breakdown",
                height=300
            ),
            'kwargs': {'ids': 'ids', 'parents': 'parents', 'values': 'values'}
        }
    ]
    
    # Create charts in batch
    if st.button("Generate Batch Charts"):
        with st.spinner("Creating charts..."):
            figures = engine.batch_create_charts(chart_specs)
        
        # Display charts
        cols = st.columns(len(figures))
        for i, fig in enumerate(figures):
            with cols[i]:
                st.plotly_chart(fig, use_container_width=True)
        
        st.success(f"Successfully created {len(figures)} charts in batch!")


def example_6_responsive_accessibility():
    """Example 6: Responsive design and accessibility features"""
    st.header("Example 6: Responsive Design & Accessibility")
    
    # Accessibility options
    col1, col2 = st.columns(2)
    with col1:
        high_contrast = st.checkbox("High Contrast Mode")
    with col2:
        reduced_motion = st.checkbox("Reduced Motion")
    
    # Create engine with accessibility settings
    theme = BraveThemeConfig(
        high_contrast=high_contrast,
        reduced_motion=reduced_motion
    )
    engine = VisualEnhancementEngine(theme=theme)
    
    time_series, _, _ = create_sample_data()
    
    config = ChartConfig(
        chart_type=ChartType.LINE,
        title="Accessible Chart Example",
        responsive=True,
        accessibility=True,
        height=400
    )
    
    fig = engine.create_line_chart(
        data=time_series,
        x='date',
        y='revenue',
        config=config
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show responsive configuration for different breakpoints
    st.subheader("Responsive Configuration")
    breakpoints = [480, 768, 1024, 1440]
    
    for bp in breakpoints:
        responsive_config = config.get_responsive_config(bp)
        st.write(f"**{bp}px viewport:** Height: {responsive_config['height']}px, "
                f"Toolbar: {responsive_config['show_toolbar']}, "
                f"Title Size: {responsive_config['title_font_size']}px")


def example_7_performance_optimization():
    """Example 7: Performance optimization for large datasets"""
    st.header("Example 7: Performance Optimization")
    
    engine = VisualEnhancementEngine()
    
    # Generate large dataset
    dataset_size = st.slider("Dataset Size", 1000, 50000, 10000, step=1000)
    
    large_data = pd.DataFrame({
        'x': np.random.randn(dataset_size),
        'y': np.random.randn(dataset_size),
        'category': np.random.choice(['A', 'B', 'C', 'D'], dataset_size),
        'size': np.random.randint(5, 50, dataset_size)
    })
    
    st.write(f"Original dataset size: {len(large_data):,} points")
    
    # Optimize data for performance
    optimized_data = engine.optimize_for_performance(large_data, ChartType.SCATTER)
    st.write(f"Optimized dataset size: {len(optimized_data):,} points")
    
    # Create chart with performance monitoring
    config = ChartConfig(
        chart_type=ChartType.SCATTER,
        title="Performance Optimized Scatter Plot",
        height=500,
        max_data_points=5000,
        enable_webgl=dataset_size > 10000
    )
    
    import time
    start_time = time.time()
    
    fig = engine.create_scatter_chart(
        data=optimized_data,
        x='x',
        y='y',
        size='size',
        color='category',
        config=config
    )
    
    render_time = time.time() - start_time
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show performance metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Render Time", f"{render_time:.3f}s")
    with col2:
        st.metric("WebGL Enabled", "Yes" if config.enable_webgl else "No")
    with col3:
        st.metric("Data Reduction", f"{(1 - len(optimized_data)/len(large_data)):.1%}")


def main():
    """Main function to run all examples"""
    st.set_page_config(
        page_title="Enhanced Visualization Examples",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🚀 Enhanced Visual Enhancement Engine Examples")
    st.markdown("Comprehensive demonstration of all enhanced visualization features")
    
    # Sidebar for example selection
    st.sidebar.title("Examples")
    example_choice = st.sidebar.selectbox(
        "Choose an example:",
        [
            "1. Basic Interactive Charts",
            "2. Advanced Animations",
            "3. Enhanced Sparklines",
            "4. Error Handling & Fallbacks",
            "5. Batch Processing",
            "6. Responsive & Accessibility",
            "7. Performance Optimization"
        ]
    )
    
    # Run selected example
    if example_choice.startswith("1"):
        example_1_basic_interactive_charts()
    elif example_choice.startswith("2"):
        example_2_advanced_animations()
    elif example_choice.startswith("3"):
        example_3_enhanced_sparklines()
    elif example_choice.startswith("4"):
        example_4_error_handling_fallbacks()
    elif example_choice.startswith("5"):
        example_5_batch_processing()
    elif example_choice.startswith("6"):
        example_6_responsive_accessibility()
    elif example_choice.startswith("7"):
        example_7_performance_optimization()
    
    # Footer
    st.markdown("---")
    st.markdown("**Enhanced Visual Enhancement Engine** - Task 6.2 Implementation")
    st.markdown("Features: Interactive Charts • Advanced Animations • Sparkline Integration • Error Handling • Performance Optimization")


if __name__ == "__main__":
    main()