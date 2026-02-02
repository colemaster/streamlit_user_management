"""
Enhanced Visual Showcase - Comprehensive Demonstration
Showcases all enhanced visualization components with advanced interactive features,
animations, sparkline integration, and comprehensive error handling.
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.ui.visual_enhancement_engine import (
    VisualEnhancementEngine,
    ChartType,
    ChartConfig,
    BraveThemeConfig,
    AnimationType,
    ResponsiveBreakpoint,
    generate_hierarchical_data,
    generate_flow_data,
    generate_3d_data
)
from src.ui.components import animated_header
from src.ui.styles import get_css
import time


def render_visual_showcase():
    """Render the enhanced visual showcase page with all new features"""
    
    # Apply Brave Design CSS
    st.markdown(get_css(), unsafe_allow_html=True)
    
    # Header
    animated_header("ENHANCED VISUAL ENGINE", "Advanced Interactive Charts with Brave Design")
    
    # Initialize Visual Enhancement Engine with custom theme
    theme_config = BraveThemeConfig(
        animation_duration=600,
        high_contrast=st.sidebar.checkbox("High Contrast Mode", False),
        reduced_motion=st.sidebar.checkbox("Reduced Motion", False)
    )
    visual_engine = VisualEnhancementEngine(theme=theme_config)
    
    # Performance metrics display
    if st.sidebar.button("Show Performance Metrics"):
        metrics = visual_engine.get_performance_metrics()
        if metrics.get('status') != 'no_data':
            st.sidebar.json(metrics)
    
    # Enhanced showcase tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Interactive Charts", 
        "🌊 Advanced Flows", 
        "📈 Smart Analytics",
        "🎯 3D Immersive",
        "⚡ Enhanced Metrics",
        "🎨 Animation Studio",
        "🔧 Performance Lab"
    ])
    
    with tab1:
        st.markdown("### Interactive Chart Creation with Advanced Features")
        
        # Chart type selector
        col1, col2, col3 = st.columns(3)
        with col1:
            chart_type = st.selectbox("Chart Type", [
                ChartType.LINE, ChartType.BAR, ChartType.SCATTER, 
                ChartType.PIE, ChartType.AREA, ChartType.BOX, 
                ChartType.HISTOGRAM, ChartType.SUNBURST, ChartType.TREEMAP
            ])
        with col2:
            animation_type = st.selectbox("Animation", [
                AnimationType.SMOOTH, AnimationType.FADE_IN, AnimationType.SLIDE_IN,
                AnimationType.ZOOM_IN, AnimationType.BOUNCE, AnimationType.ELASTIC
            ])
        with col3:
            enable_fallback = st.checkbox("Enable Fallback", True)
        
        # Generate sample data based on chart type
        if chart_type in [ChartType.SUNBURST, ChartType.TREEMAP]:
            sample_data = generate_hierarchical_data(3, 4)
            required_cols = ["ids", "parents", "values"]
        else:
            # Generate time series data
            dates = pd.date_range('2024-01-01', periods=100, freq='D')
            sample_data = pd.DataFrame({
                'date': dates,
                'value': np.cumsum(np.random.randn(100)) + 100,
                'category': np.random.choice(['A', 'B', 'C'], 100),
                'size': np.random.randint(10, 100, 100)
            })
            required_cols = ['date', 'value']
        
        # Create enhanced configuration
        config = ChartConfig(
            chart_type=chart_type,
            title=f"Enhanced {chart_type.value.title()} Chart",
            animation_type=animation_type,
            height=500,
            animations=True,
            responsive=True,
            accessibility=True,
            fallback_enabled=enable_fallback,
            hover_enabled=True,
            zoom_enabled=True,
            pan_enabled=True
        )
        
        # Create chart with error handling
        try:
            start_time = time.time()
            
            if chart_type in [ChartType.SUNBURST, ChartType.TREEMAP]:
                if chart_type == ChartType.SUNBURST:
                    fig = visual_engine.create_sunburst_chart(
                        sample_data, "ids", "parents", "values", config
                    )
                else:
                    fig = visual_engine.create_treemap_chart(
                        sample_data, "ids", "parents", "values", config
                    )
            else:
                # Use the enhanced interactive chart creation
                kwargs = {}
                if chart_type == ChartType.LINE:
                    kwargs = {'x': 'date', 'y': 'value', 'color': 'category'}
                elif chart_type == ChartType.BAR:
                    kwargs = {'x': 'category', 'y': 'value'}
                elif chart_type == ChartType.SCATTER:
                    kwargs = {'x': 'date', 'y': 'value', 'size': 'size', 'color': 'category'}
                elif chart_type == ChartType.PIE:
                    pie_data = sample_data.groupby('category')['value'].sum().reset_index()
                    kwargs = {'values': 'value', 'names': 'category'}
                    sample_data = pie_data
                elif chart_type == ChartType.AREA:
                    kwargs = {'x': 'date', 'y': 'value', 'color': 'category'}
                elif chart_type == ChartType.BOX:
                    kwargs = {'x': 'category', 'y': 'value'}
                elif chart_type == ChartType.HISTOGRAM:
                    kwargs = {'x': 'value'}
                
                fig = visual_engine.create_interactive_chart(
                    chart_type, sample_data, config, **kwargs
                )
            
            render_time = time.time() - start_time
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Render Time", f"{render_time:.3f}s")
            with col2:
                st.metric("Data Points", len(sample_data))
            with col3:
                st.metric("Chart Type", chart_type.value.title())
                
        except Exception as e:
            st.error(f"Chart creation error: {str(e)}")
            if enable_fallback:
                st.info("Attempting fallback chart...")
                fallback_fig = visual_engine.create_chart_with_fallback(
                    chart_type, sample_data, config
                )
                st.plotly_chart(fallback_fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Flow and Process Visualization")
        
        st.markdown('<div class="brave-card">', unsafe_allow_html=True)
        st.markdown("**Sankey Diagram - Budget Flow Analysis**")
        
        # Generate flow data
        nodes = [
            "Total Budget", "Development", "Operations", "Marketing",
            "EC2", "RDS", "S3", "Lambda", "CloudFront", "Route53"
        ]
        df_flow = generate_flow_data(nodes, num_flows=20)
        
        config_sankey = ChartConfig(
            chart_type=ChartType.SANKEY,
            title="Budget Flow from Departments to AWS Services",
            height=500,
            animations=True
        )
        
        fig_sankey = visual_engine.create_sankey_diagram(
            data=df_flow,
            source="source",
            target="target",
            value="value",
            config=config_sankey
        )
        
        st.plotly_chart(fig_sankey, use_container_width=True)
        
        # Controls
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Regenerate Flow", key="regen_sankey"):
                st.rerun()
        with col2:
            min_flow = st.slider("Minimum Flow Value", 1, 20, 5, key="min_flow")
        with col3:
            st.metric("Total Flows", len(df_flow))
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Distribution and Statistical Analysis")
        
        st.markdown('<div class="brave-card">', unsafe_allow_html=True)
        st.markdown("**Violin Plot - Cost Distribution by Service**")
        
        # Generate distribution data
        services = ["EC2", "RDS", "S3", "Lambda", "CloudWatch"]
        data = []
        
        for service in services:
            if service == "EC2":
                values = np.random.normal(150, 40, 100)
            elif service == "RDS":
                values = np.random.exponential(80, 100)
            elif service == "S3":
                values = np.random.gamma(2, 30, 100)
            elif service == "Lambda":
                values = np.random.lognormal(2, 1, 100)
            else:
                values = np.random.uniform(10, 50, 100)
            
            for value in values:
                data.append({"Service": service, "Cost": max(0, value)})
        
        df_violin = pd.DataFrame(data)
        
        config_violin = ChartConfig(
            chart_type=ChartType.VIOLIN,
            title="Cost Distribution Analysis by AWS Service",
            height=400,
            animations=True
        )
        
        fig_violin = visual_engine.create_violin_plot(
            data=df_violin,
            x="Service",
            y="Cost",
            config=config_violin
        )
        
        st.plotly_chart(fig_violin, use_container_width=True)
        
        # Statistical summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean Cost", f"${df_violin['Cost'].mean():.2f}")
        with col2:
            st.metric("Median Cost", f"${df_violin['Cost'].median():.2f}")
        with col3:
            st.metric("Std Dev", f"${df_violin['Cost'].std():.2f}")
        with col4:
            st.metric("Max Cost", f"${df_violin['Cost'].max():.2f}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 3D Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="brave-card">', unsafe_allow_html=True)
            st.markdown("**3D Scatter Plot - Resource Performance**")
            
            # Generate 3D data
            df_3d = generate_3d_data(n_points=150)
            
            config_3d_scatter = ChartConfig(
                chart_type=ChartType.SCATTER_3D,
                title="CPU vs Memory vs Cost Analysis",
                height=500,
                animations=True
            )
            
            fig_3d_scatter = visual_engine.create_3d_scatter(
                data=df_3d,
                x="x",
                y="y",
                z="z",
                size="size",
                color="color",
                config=config_3d_scatter
            )
            
            # Update axis labels
            fig_3d_scatter.update_layout(
                scene=dict(
                    xaxis_title="CPU Usage (%)",
                    yaxis_title="Memory Usage (GB)",
                    zaxis_title="Cost ($)"
                )
            )
            
            st.plotly_chart(fig_3d_scatter, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="brave-card">', unsafe_allow_html=True)
            st.markdown("**3D Surface Plot - Performance Landscape**")
            
            # Generate 3D surface data
            x = np.linspace(-3, 3, 40)
            y = np.linspace(-3, 3, 40)
            X, Y = np.meshgrid(x, y)
            Z = 3 * (1 - X)**2 * np.exp(-(X**2) - (Y + 1)**2) \
                - 10 * (X/5 - X**3 - Y**5) * np.exp(-X**2 - Y**2) \
                - 1/3 * np.exp(-(X + 1)**2 - Y**2)
            
            config_3d_surface = ChartConfig(
                chart_type=ChartType.SURFACE_3D,
                title="Cost Optimization Landscape",
                height=500,
                animations=True
            )
            
            fig_3d_surface = visual_engine.create_3d_surface(
                z_data=Z,
                x_labels=x,
                y_labels=y,
                config=config_3d_surface
            )
            
            st.plotly_chart(fig_3d_surface, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 3D Controls
        st.markdown('<div class="brave-card">', unsafe_allow_html=True)
        st.markdown("**3D Visualization Controls**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            camera_angle = st.selectbox("Camera Angle", ["Default", "Top View", "Side View", "Isometric"])
        with col2:
            point_size = st.slider("Point Size", 1, 20, 8)
        with col3:
            opacity = st.slider("Opacity", 0.1, 1.0, 0.8)
        with col4:
            if st.button("🎲 Randomize Data", key="randomize_3d"):
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### Enhanced Metrics with Sparklines")
        
        st.markdown('<div class="brave-card">', unsafe_allow_html=True)
        st.markdown("**Real-time Metrics Dashboard**")
        
        # Create enhanced metrics with sparklines
        metrics_data = [
            {
                "label": "Total Monthly Cost",
                "value": "$47,832",
                "delta": "+8.3%",
                "sparkline": [42000, 43500, 44200, 45800, 46100, 47200, 46800, 47832]
            },
            {
                "label": "Active Instances",
                "value": "1,247",
                "delta": "+12",
                "sparkline": [1200, 1215, 1230, 1225, 1240, 1235, 1250, 1247]
            },
            {
                "label": "Cost per Instance",
                "value": "$38.37",
                "delta": "-2.1%",
                "sparkline": [40.2, 39.8, 39.1, 38.9, 38.5, 38.8, 38.4, 38.37]
            },
            {
                "label": "Efficiency Score",
                "value": "94.2%",
                "delta": "+1.8%",
                "sparkline": [91.5, 92.1, 92.8, 93.2, 93.6, 94.0, 93.8, 94.2]
            }
        ]
        
        cols = st.columns(len(metrics_data))
        
        for i, metric in enumerate(metrics_data):
            with cols[i]:
                # Create sparkline
                sparkline_fig = visual_engine.create_sparkline_metrics(
                    data=metric["sparkline"],
                    color=visual_engine.theme.primary_orange
                )
                
                # Display metric
                st.metric(
                    label=metric["label"],
                    value=metric["value"],
                    delta=metric["delta"]
                )
                
                # Display sparkline
                st.plotly_chart(sparkline_fig, use_container_width=True, key=f"sparkline_{i}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Sparkline controls
        st.markdown('<div class="brave-card">', unsafe_allow_html=True)
        st.markdown("**Sparkline Configuration**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            sparkline_color = st.color_picker("Sparkline Color", "#FF4500")
        with col2:
            time_range = st.selectbox("Time Range", ["7 days", "30 days", "90 days"])
        with col3:
            if st.button("🔄 Refresh Metrics", key="refresh_metrics"):
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer with technical details
    st.markdown("---")
    st.markdown('<div class="brave-card">', unsafe_allow_html=True)
    st.markdown("**Technical Implementation Details**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **Chart Types Implemented:**
        - Sunburst Charts
        - Sankey Diagrams  
        - Treemap Charts
        - Violin Plots
        - 3D Scatter Plots
        - 3D Surface Plots
        - Enhanced Sparklines
        """)
    
    with col2:
        st.markdown("""
        **Features:**
        - Brave Design Theme Integration
        - Interactive Hover Effects
        - Smooth Animations
        - Responsive Design
        - Accessibility Support
        - Custom Color Palettes
        """)
    
    with col3:
        st.markdown("""
        **Technology Stack:**
        - Plotly 6.5.2+
        - Streamlit Nightly 2026
        - NumPy & Pandas
        - Custom Theme Engine
        - Property-based Testing
        - Modern CSS3 Effects
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    render_visual_showcase()