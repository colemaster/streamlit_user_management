"""
Enhanced Chart Cards using Visual Enhancement Engine
Implements new chart types with Brave Design theme integration.
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.ui.cards.engine import register_card
from src.nexus.protocol import NexusCardState
from src.ui.visual_enhancement_engine import (
    VisualEnhancementEngine, 
    ChartType, 
    ChartConfig,
    generate_hierarchical_data,
    generate_flow_data,
    generate_3d_data
)


# Initialize the Visual Enhancement Engine
visual_engine = VisualEnhancementEngine()


@register_card("sunburst-chart")
@st.fragment
def render_sunburst_chart(card: NexusCardState):
    """
    Sunburst Chart for hierarchical cost breakdown.
    
    Data Expectation: {
        'data_source': str (optional - 'mock' or custom),
        'levels': int (optional - depth of hierarchy),
        'items_per_level': int (optional)
    }
    """
    st.markdown(f'<div class="brave-card">', unsafe_allow_html=True)
    st.markdown(f"**{card.title}**")
    
    # Generate or use provided data
    data_source = card.data.get("data_source", "mock")
    if data_source == "mock":
        levels = card.data.get("levels", 3)
        items_per_level = card.data.get("items_per_level", 4)
        df = generate_hierarchical_data(levels, items_per_level)
    else:
        # In a real implementation, this would fetch from actual data source
        df = generate_hierarchical_data(3, 4)
    
    # Create chart configuration
    config = ChartConfig(
        chart_type=ChartType.SUNBURST,
        title=card.title,
        height=400,
        animations=True
    )
    
    # Create the sunburst chart
    fig = visual_engine.create_sunburst_chart(
        data=df,
        ids="ids",
        parents="parents", 
        values="values",
        config=config
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Drill Down", key=f"drill_{card.id}"):
            st.toast("Drilling down to next level...")
    with col2:
        if st.button("Export Data", key=f"export_{card.id}"):
            st.toast("Exporting chart data...")
    
    st.markdown("</div>", unsafe_allow_html=True)


@register_card("sankey-diagram")
@st.fragment
def render_sankey_diagram(card: NexusCardState):
    """
    Sankey Diagram for flow visualization (e.g., cost flows between services).
    
    Data Expectation: {
        'nodes': list (optional - list of node names),
        'num_flows': int (optional - number of flows to generate)
    }
    """
    st.markdown(f'<div class="brave-card">', unsafe_allow_html=True)
    st.markdown(f"**{card.title}**")
    
    # Generate or use provided data
    nodes = card.data.get("nodes", [
        "Budget", "Planning", "Development", "Testing", "Production",
        "EC2", "RDS", "S3", "Lambda", "CloudWatch"
    ])
    num_flows = card.data.get("num_flows", 15)
    
    df = generate_flow_data(nodes, num_flows)
    
    # Create chart configuration
    config = ChartConfig(
        chart_type=ChartType.SANKEY,
        title=card.title,
        height=500,
        animations=True
    )
    
    # Create the Sankey diagram
    fig = visual_engine.create_sankey_diagram(
        data=df,
        source="source",
        target="target",
        value="value",
        config=config
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Filter Flows", key=f"filter_{card.id}"):
            st.toast("Applying flow filters...")
    with col2:
        threshold = st.slider("Min Flow Value", 1, 50, 10, key=f"threshold_{card.id}")
    
    st.markdown("</div>", unsafe_allow_html=True)


@register_card("treemap-chart")
@st.fragment
def render_treemap_chart(card: NexusCardState):
    """
    Treemap Chart for hierarchical data with area-based visualization.
    
    Data Expectation: {
        'data_source': str (optional),
        'levels': int (optional),
        'items_per_level': int (optional)
    }
    """
    st.markdown(f'<div class="brave-card">', unsafe_allow_html=True)
    st.markdown(f"**{card.title}**")
    
    # Generate or use provided data
    data_source = card.data.get("data_source", "mock")
    if data_source == "mock":
        levels = card.data.get("levels", 3)
        items_per_level = card.data.get("items_per_level", 3)
        df = generate_hierarchical_data(levels, items_per_level)
    else:
        df = generate_hierarchical_data(3, 3)
    
    # Create chart configuration
    config = ChartConfig(
        chart_type=ChartType.TREEMAP,
        title=card.title,
        height=400,
        animations=True
    )
    
    # Create the treemap chart
    fig = visual_engine.create_treemap_chart(
        data=df,
        ids="ids",
        parents="parents",
        values="values",
        config=config
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zoom In", key=f"zoom_{card.id}"):
            st.toast("Zooming into selected area...")
    with col2:
        if st.button("Reset View", key=f"reset_{card.id}"):
            st.toast("Resetting treemap view...")
    
    st.markdown("</div>", unsafe_allow_html=True)


@register_card("violin-plot")
@st.fragment
def render_violin_plot(card: NexusCardState):
    """
    Violin Plot for distribution analysis.
    
    Data Expectation: {
        'categories': list (optional - category names),
        'n_points': int (optional - number of data points per category)
    }
    """
    st.markdown(f'<div class="brave-card">', unsafe_allow_html=True)
    st.markdown(f"**{card.title}**")
    
    # Generate sample data for violin plot
    categories = card.data.get("categories", ["EC2", "RDS", "S3", "Lambda"])
    n_points = card.data.get("n_points", 100)
    
    # Create sample distribution data
    data = []
    for category in categories:
        # Generate different distributions for each category
        if category == "EC2":
            values = np.random.normal(100, 25, n_points)
        elif category == "RDS":
            values = np.random.exponential(50, n_points)
        elif category == "S3":
            values = np.random.gamma(2, 20, n_points)
        else:
            values = np.random.lognormal(3, 1, n_points)
        
        for value in values:
            data.append({"Service": category, "Cost": max(0, value)})
    
    df = pd.DataFrame(data)
    
    # Create chart configuration
    config = ChartConfig(
        chart_type=ChartType.VIOLIN,
        title=card.title,
        height=400,
        animations=True
    )
    
    # Create the violin plot
    fig = visual_engine.create_violin_plot(
        data=df,
        x="Service",
        y="Cost",
        config=config
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add controls
    col1, col2 = st.columns(2)
    with col1:
        show_box = st.checkbox("Show Box Plot", value=True, key=f"box_{card.id}")
    with col2:
        if st.button("Statistical Summary", key=f"stats_{card.id}"):
            st.toast("Generating statistical summary...")
    
    st.markdown("</div>", unsafe_allow_html=True)


@register_card("3d-scatter")
@st.fragment
def render_3d_scatter(card: NexusCardState):
    """
    3D Scatter Plot for multidimensional data visualization.
    
    Data Expectation: {
        'n_points': int (optional - number of data points),
        'x_label': str (optional),
        'y_label': str (optional),
        'z_label': str (optional)
    }
    """
    st.markdown(f'<div class="brave-card">', unsafe_allow_html=True)
    st.markdown(f"**{card.title}**")
    
    # Generate 3D data
    n_points = card.data.get("n_points", 100)
    df = generate_3d_data(n_points)
    
    # Add labels
    x_label = card.data.get("x_label", "CPU Usage")
    y_label = card.data.get("y_label", "Memory Usage")
    z_label = card.data.get("z_label", "Cost")
    
    # Create chart configuration
    config = ChartConfig(
        chart_type=ChartType.SCATTER_3D,
        title=card.title,
        height=500,
        animations=True
    )
    
    # Create the 3D scatter plot
    fig = visual_engine.create_3d_scatter(
        data=df,
        x="x",
        y="y", 
        z="z",
        size="size",
        color="color",
        config=config
    )
    
    # Update axis labels
    fig.update_layout(
        scene=dict(
            xaxis_title=x_label,
            yaxis_title=y_label,
            zaxis_title=z_label
        )
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Rotate View", key=f"rotate_{card.id}"):
            st.toast("Rotating 3D view...")
    with col2:
        if st.button("Filter Points", key=f"filter_3d_{card.id}"):
            st.toast("Applying 3D filters...")
    with col3:
        opacity = st.slider("Opacity", 0.1, 1.0, 0.8, key=f"opacity_{card.id}")
    
    st.markdown("</div>", unsafe_allow_html=True)


@register_card("3d-surface")
@st.fragment
def render_3d_surface(card: NexusCardState):
    """
    3D Surface Plot for continuous data visualization.
    
    Data Expectation: {
        'grid_size': int (optional - size of the data grid),
        'function_type': str (optional - type of surface function)
    }
    """
    st.markdown(f'<div class="brave-card">', unsafe_allow_html=True)
    st.markdown(f"**{card.title}**")
    
    # Generate 3D surface data
    grid_size = card.data.get("grid_size", 50)
    function_type = card.data.get("function_type", "peaks")
    
    x = np.linspace(-3, 3, grid_size)
    y = np.linspace(-3, 3, grid_size)
    X, Y = np.meshgrid(x, y)
    
    if function_type == "peaks":
        Z = 3 * (1 - X)**2 * np.exp(-(X**2) - (Y + 1)**2) \
            - 10 * (X/5 - X**3 - Y**5) * np.exp(-X**2 - Y**2) \
            - 1/3 * np.exp(-(X + 1)**2 - Y**2)
    elif function_type == "sinc":
        R = np.sqrt(X**2 + Y**2)
        Z = np.sinc(R)
    else:
        Z = np.sin(np.sqrt(X**2 + Y**2))
    
    # Create chart configuration
    config = ChartConfig(
        chart_type=ChartType.SURFACE_3D,
        title=card.title,
        height=500,
        animations=True
    )
    
    # Create the 3D surface plot
    fig = visual_engine.create_3d_surface(
        z_data=Z,
        x_labels=x,
        y_labels=y,
        config=config
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add controls
    col1, col2 = st.columns(2)
    with col1:
        surface_type = st.selectbox(
            "Surface Type", 
            ["peaks", "sinc", "wave"], 
            key=f"surface_{card.id}"
        )
    with col2:
        if st.button("Regenerate", key=f"regen_{card.id}"):
            st.toast("Regenerating surface...")
    
    st.markdown("</div>", unsafe_allow_html=True)


@register_card("enhanced-metrics-with-sparklines")
@st.fragment
def render_enhanced_metrics_sparklines(card: NexusCardState):
    """
    Enhanced metrics card with integrated sparklines using Visual Enhancement Engine.
    
    Data Expectation: {
        'metrics': list of dict with 'label', 'value', 'delta', 'sparkline_data'
    }
    """
    st.markdown(f'<div class="brave-card">', unsafe_allow_html=True)
    st.markdown(f"**{card.title}**")
    
    # Get metrics data
    metrics = card.data.get("metrics", [
        {
            "label": "Total Cost",
            "value": "$45,230",
            "delta": "+12.5%",
            "sparkline_data": [100, 120, 110, 130, 125, 140, 135, 150, 145, 160]
        },
        {
            "label": "Active Resources",
            "value": "1,247",
            "delta": "+3.2%",
            "sparkline_data": [1200, 1210, 1205, 1220, 1215, 1230, 1225, 1240, 1235, 1247]
        },
        {
            "label": "Efficiency Score",
            "value": "87.3%",
            "delta": "-2.1%",
            "sparkline_data": [90, 89, 88, 87, 88, 86, 87, 88, 87, 87.3]
        }
    ])
    
    # Create columns for metrics
    cols = st.columns(len(metrics))
    
    for i, metric in enumerate(metrics):
        with cols[i]:
            # Create sparkline chart
            sparkline_fig = visual_engine.create_sparkline_metrics(
                data=metric["sparkline_data"],
                color=visual_engine.theme.primary_orange
            )
            
            # Display metric with sparkline
            st.metric(
                label=metric["label"],
                value=metric["value"],
                delta=metric["delta"]
            )
            
            # Display sparkline below metric
            st.plotly_chart(sparkline_fig, use_container_width=True, key=f"spark_{card.id}_{i}")
    
    st.markdown("</div>", unsafe_allow_html=True)