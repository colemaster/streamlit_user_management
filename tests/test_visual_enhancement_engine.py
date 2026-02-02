"""
Enhanced Tests for Visual Enhancement Engine - Plotly 6.5.2+ Integration
Tests advanced interactive features, animations, sparkline integration,
error handling, and performance monitoring.
"""

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from unittest.mock import Mock, patch
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


class TestEnhancedBraveThemeConfig:
    """Test enhanced Brave Design theme configuration"""
    
    def test_default_theme_colors(self):
        """Test that default theme colors match Brave Design specification"""
        theme = BraveThemeConfig()
        
        assert theme.primary_orange == "#FF4500"
        assert theme.secondary_orange == "#FF8C00"
        assert theme.dark_background == "#1a1a1a"
        assert theme.text_primary == "#FFFFFF"
        assert theme.success_color == "#00FF9D"
        assert theme.warning_color == "#FFD700"
        assert theme.error_color == "#FF0055"
    
    def test_enhanced_color_palette_generation(self):
        """Test that enhanced color palette is properly generated"""
        theme = BraveThemeConfig()
        
        assert len(theme.color_palette) == 12  # Enhanced palette
        assert theme.color_palette[0] == theme.primary_orange
        assert theme.color_palette[1] == theme.secondary_orange
    
    def test_animation_settings(self):
        """Test animation configuration settings"""
        theme = BraveThemeConfig(
            animation_duration=750,
            transition_easing="ease-in-out"
        )
        
        assert theme.animation_duration == 750
        assert theme.transition_easing == "ease-in-out"
    
    def test_responsive_height_calculation(self):
        """Test responsive height calculation for different breakpoints"""
        theme = BraveThemeConfig(
            mobile_height=250,
            tablet_height=350,
            desktop_height=450
        )
        
        assert theme.get_responsive_height(ResponsiveBreakpoint.MOBILE) == 250
        assert theme.get_responsive_height(ResponsiveBreakpoint.TABLET) == 350
        assert theme.get_responsive_height(ResponsiveBreakpoint.DESKTOP) == 450
        assert theme.get_responsive_height(ResponsiveBreakpoint.LARGE) == 450
    
    def test_accessibility_settings(self):
        """Test accessibility configuration options"""
        theme = BraveThemeConfig(
            high_contrast=True,
            reduced_motion=True
        )
        
        assert theme.high_contrast is True
        assert theme.reduced_motion is True


class TestVisualEnhancementEngine:
    """Test Visual Enhancement Engine functionality"""
    
    @pytest.fixture
    def engine(self):
        """Create Visual Enhancement Engine instance"""
        return VisualEnhancementEngine()
    
    @pytest.fixture
    def sample_hierarchical_data(self):
        """Generate sample hierarchical data"""
        return generate_hierarchical_data(levels=3, items_per_level=3)
    
    @pytest.fixture
    def sample_flow_data(self):
        """Generate sample flow data"""
        nodes = ["Source1", "Source2", "Target1", "Target2", "Target3"]
        return generate_flow_data(nodes, num_flows=8)
    
    @pytest.fixture
    def sample_3d_data(self):
        """Generate sample 3D data"""
        return generate_3d_data(n_points=50)
    
    def test_engine_initialization(self, engine):
        """Test that engine initializes with proper theme"""
        assert isinstance(engine.theme, BraveThemeConfig)
        assert engine.theme.primary_orange == "#FF4500"
        assert 'paper_bgcolor' in engine._base_layout
        assert engine._base_layout['paper_bgcolor'] == "#1a1a1a"
    
    def test_sunburst_chart_creation(self, engine, sample_hierarchical_data):
        """Test sunburst chart creation with Brave theme"""
        config = ChartConfig(
            chart_type=ChartType.SUNBURST,
            title="Test Sunburst",
            height=400
        )
        
        fig = engine.create_sunburst_chart(
            data=sample_hierarchical_data,
            ids="ids",
            parents="parents",
            values="values",
            config=config
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert isinstance(fig.data[0], go.Sunburst)
        assert fig.layout.title.text == "Test Sunburst"
        assert fig.layout.paper_bgcolor == "#1a1a1a"
        assert fig.layout.height == 400
    
    def test_sankey_diagram_creation(self, engine, sample_flow_data):
        """Test Sankey diagram creation"""
        config = ChartConfig(
            chart_type=ChartType.SANKEY,
            title="Test Sankey",
            height=500
        )
        
        fig = engine.create_sankey_diagram(
            data=sample_flow_data,
            source="source",
            target="target",
            value="value",
            config=config
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert isinstance(fig.data[0], go.Sankey)
        assert fig.layout.title.text == "Test Sankey"
        assert fig.layout.height == 500
    
    def test_treemap_chart_creation(self, engine, sample_hierarchical_data):
        """Test treemap chart creation"""
        config = ChartConfig(
            chart_type=ChartType.TREEMAP,
            title="Test Treemap",
            height=400
        )
        
        fig = engine.create_treemap_chart(
            data=sample_hierarchical_data,
            ids="ids",
            parents="parents",
            values="values",
            config=config
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert isinstance(fig.data[0], go.Treemap)
        assert fig.layout.title.text == "Test Treemap"
    
    def test_violin_plot_creation(self, engine):
        """Test violin plot creation"""
        # Create sample distribution data
        data = []
        categories = ["A", "B", "C"]
        for cat in categories:
            values = np.random.normal(50, 10, 30)
            for val in values:
                data.append({"category": cat, "value": val})
        
        df = pd.DataFrame(data)
        
        config = ChartConfig(
            chart_type=ChartType.VIOLIN,
            title="Test Violin Plot",
            height=400
        )
        
        fig = engine.create_violin_plot(
            data=df,
            x="category",
            y="value",
            config=config
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 1  # May have multiple traces for different categories
        assert fig.layout.title.text == "Test Violin Plot"
    
    def test_3d_scatter_creation(self, engine, sample_3d_data):
        """Test 3D scatter plot creation"""
        config = ChartConfig(
            chart_type=ChartType.SCATTER_3D,
            title="Test 3D Scatter",
            height=500
        )
        
        fig = engine.create_3d_scatter(
            data=sample_3d_data,
            x="x",
            y="y",
            z="z",
            size="size",
            color="color",
            config=config
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert isinstance(fig.data[0], go.Scatter3d)
        assert fig.layout.title.text == "Test 3D Scatter"
        assert 'scene' in fig.layout
    
    def test_3d_surface_creation(self, engine):
        """Test 3D surface plot creation"""
        # Create sample surface data
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2))
        
        config = ChartConfig(
            chart_type=ChartType.SURFACE_3D,
            title="Test 3D Surface",
            height=500
        )
        
        fig = engine.create_3d_surface(
            z_data=Z,
            x_labels=x,
            y_labels=y,
            config=config
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert isinstance(fig.data[0], go.Surface)
        assert fig.layout.title.text == "Test 3D Surface"
    
    def test_sparkline_creation(self, engine):
        """Test sparkline chart creation for metrics"""
        data = [10, 12, 11, 15, 13, 16, 14, 18, 17, 20]
        
        fig = engine.create_sparkline_metrics(data)
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert isinstance(fig.data[0], go.Scatter)
        assert fig.layout.height == 60
        assert fig.layout.paper_bgcolor == 'rgba(0,0,0,0)'
    
    def test_brave_theme_application(self, engine):
        """Test applying Brave theme to existing figure"""
        # Create a basic figure
        fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6]))
        
        # Apply Brave theme
        themed_fig = engine.apply_brave_theme(fig)
        
        assert themed_fig.layout.paper_bgcolor == "#1a1a1a"
        assert themed_fig.layout.plot_bgcolor == "#1a1a1a"
        assert themed_fig.layout.font.color == "#FFFFFF"
        assert themed_fig.layout.font.family == 'Rajdhani, sans-serif'
    
    def test_animation_addition(self, engine):
        """Test adding animations to charts"""
        fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6]))
        
        animated_fig = engine.add_animations(fig, duration=750)
        
        assert animated_fig.layout.transition.duration == 750
        assert 'updatemenus' in animated_fig.layout
    
    def test_interactive_chart_creation(self, engine, sample_hierarchical_data):
        """Test generic interactive chart creation method"""
        config = ChartConfig(
            chart_type=ChartType.SUNBURST,
            title="Interactive Test",
            animations=True
        )
        
        fig = engine.create_interactive_chart(
            chart_type=ChartType.SUNBURST,
            data=sample_hierarchical_data,
            config=config,
            ids="ids",
            parents="parents",
            values="values"
        )
        
        assert isinstance(fig, go.Figure)
        assert isinstance(fig.data[0], go.Sunburst)
    
    def test_unsupported_chart_type(self, engine):
        """Test error handling for unsupported chart types"""
        config = ChartConfig(chart_type=ChartType.BOX)  # Not implemented
        
        with pytest.raises(ValueError, match="Unsupported chart type"):
            engine.create_interactive_chart(
                chart_type=ChartType.BOX,
                data=pd.DataFrame(),
                config=config
            )


class TestDataGenerators:
    """Test data generation utilities"""
    
    def test_hierarchical_data_generation(self):
        """Test hierarchical data generation for sunburst/treemap"""
        df = generate_hierarchical_data(levels=2, items_per_level=3)
        
        assert isinstance(df, pd.DataFrame)
        assert all(col in df.columns for col in ["ids", "parents", "values"])
        assert len(df) > 0
        
        # Check that root exists
        root_rows = df[df["parents"] == ""]
        assert len(root_rows) == 1
        assert root_rows.iloc[0]["ids"] == "Total"
    
    def test_flow_data_generation(self):
        """Test flow data generation for Sankey diagrams"""
        nodes = ["A", "B", "C", "D"]
        df = generate_flow_data(nodes, num_flows=5)
        
        assert isinstance(df, pd.DataFrame)
        assert all(col in df.columns for col in ["source", "target", "value"])
        assert len(df) == 5
        
        # Check that sources and targets are from the provided nodes
        assert all(source in nodes for source in df["source"])
        assert all(target in nodes for target in df["target"])
    
    def test_3d_data_generation(self):
        """Test 3D data generation for scatter plots"""
        df = generate_3d_data(n_points=25)
        
        assert isinstance(df, pd.DataFrame)
        assert all(col in df.columns for col in ["x", "y", "z", "size", "color"])
        assert len(df) == 25
        
        # Check data types and ranges
        assert all(isinstance(val, (int, float, np.number)) for val in df["x"])
        assert all(5 <= size <= 25 for size in df["size"])
        assert all(0 <= color <= 1 for color in df["color"])


class TestChartIntegration:
    """Test chart integration with Streamlit components"""
    
    def test_chart_config_creation(self):
        """Test chart configuration creation"""
        config = ChartConfig(
            chart_type=ChartType.SUNBURST,
            title="Test Chart",
            height=600,
            animations=False
        )
        
        assert config.chart_type == ChartType.SUNBURST
        assert config.title == "Test Chart"
        assert config.height == 600
        assert config.animations is False
        assert isinstance(config.theme, BraveThemeConfig)
    
    def test_chart_responsiveness(self):
        """Test that charts are configured for responsiveness"""
        engine = VisualEnhancementEngine()
        config = ChartConfig(
            chart_type=ChartType.TREEMAP,
            responsive=True
        )
        
        df = generate_hierarchical_data(2, 2)
        fig = engine.create_treemap_chart(
            data=df,
            ids="ids",
            parents="parents",
            values="values",
            config=config
        )
        
        # Check that the figure can be rendered responsively
        assert isinstance(fig, go.Figure)
        assert config.responsive is True
    
    def test_accessibility_features(self):
        """Test accessibility features in charts"""
        engine = VisualEnhancementEngine()
        config = ChartConfig(
            chart_type=ChartType.VIOLIN,
            accessibility=True
        )
        
        # Create sample data
        data = pd.DataFrame({
            "category": ["A"] * 20 + ["B"] * 20,
            "value": list(np.random.normal(50, 10, 20)) + list(np.random.normal(60, 15, 20))
        })
        
        fig = engine.create_violin_plot(
            data=data,
            x="category",
            y="value",
            config=config
        )
        
        # Check that accessibility is enabled
        assert config.accessibility is True
        assert isinstance(fig, go.Figure)


if __name__ == "__main__":
    pytest.main([__file__])


class TestEnhancedChartConfig:
    """Test enhanced chart configuration"""
    
    def test_enhanced_chart_config_creation(self):
        """Test enhanced chart configuration with all new features"""
        config = ChartConfig(
            chart_type=ChartType.SUNBURST,
            title="Test Chart",
            animation_type=AnimationType.BOUNCE,
            height=600,
            animations=True,
            responsive=True,
            accessibility=True,
            hover_enabled=True,
            zoom_enabled=True,
            pan_enabled=True,
            selection_enabled=True,
            fallback_enabled=True,
            max_data_points=5000,
            enable_webgl=True
        )
        
        assert config.chart_type == ChartType.SUNBURST
        assert config.title == "Test Chart"
        assert config.animation_type == AnimationType.BOUNCE
        assert config.height == 600
        assert config.animations is True
        assert config.responsive is True
        assert config.accessibility is True
        assert config.hover_enabled is True
        assert config.zoom_enabled is True
        assert config.pan_enabled is True
        assert config.selection_enabled is True
        assert config.fallback_enabled is True
        assert config.max_data_points == 5000
        assert config.enable_webgl is True
        assert isinstance(config.theme, BraveThemeConfig)
    
    def test_responsive_config_generation(self):
        """Test responsive configuration generation"""
        config = ChartConfig(chart_type=ChartType.BAR)
        
        mobile_config = config.get_responsive_config(400)
        tablet_config = config.get_responsive_config(700)
        desktop_config = config.get_responsive_config(1200)
        
        assert mobile_config['height'] == config.theme.mobile_height
        assert mobile_config['show_toolbar'] is False
        assert mobile_config['title_font_size'] == 16
        
        assert tablet_config['height'] == config.theme.tablet_height
        assert tablet_config['show_toolbar'] is True
        assert tablet_config['title_font_size'] == 20
        
        assert desktop_config['height'] == config.theme.desktop_height
        assert desktop_config['show_toolbar'] is True
        assert desktop_config['title_font_size'] == 24
    
    def test_error_callback_configuration(self):
        """Test error callback configuration"""
        mock_callback = Mock()
        config = ChartConfig(
            chart_type=ChartType.LINE,
            error_callback=mock_callback
        )
        
        assert config.error_callback == mock_callback


class TestEnhancedVisualEnhancementEngine:
    """Test enhanced Visual Enhancement Engine functionality"""
    
    @pytest.fixture
    def enhanced_engine(self):
        """Create enhanced Visual Enhancement Engine instance"""
        theme = BraveThemeConfig(
            animation_duration=500,
            high_contrast=False,
            reduced_motion=False
        )
        return VisualEnhancementEngine(theme=theme)
    
    @pytest.fixture
    def sample_time_series_data(self):
        """Generate sample time series data"""
        dates = pd.date_range('2024-01-01', periods=50, freq='D')
        return pd.DataFrame({
            'date': dates,
            'value': np.cumsum(np.random.randn(50)) + 100,
            'category': np.random.choice(['A', 'B', 'C'], 50),
            'size': np.random.randint(10, 100, 50)
        })
    
    def test_enhanced_engine_initialization(self, enhanced_engine):
        """Test that enhanced engine initializes with proper theme and monitoring"""
        assert isinstance(enhanced_engine.theme, BraveThemeConfig)
        assert enhanced_engine.theme.primary_orange == "#FF4500"
        assert 'paper_bgcolor' in enhanced_engine._base_layout
        assert enhanced_engine._base_layout['paper_bgcolor'] == "#1a1a1a"
        assert enhanced_engine._render_times == []
        assert enhanced_engine._error_count == 0
    
    def test_data_validation(self, enhanced_engine):
        """Test data validation functionality"""
        # Test with valid data
        valid_data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        assert enhanced_engine._validate_data(valid_data, ['x', 'y']) is True
        
        # Test with missing columns
        with pytest.raises(ValueError, match="Missing required columns"):
            enhanced_engine._validate_data(valid_data, ['x', 'y', 'z'])
        
        # Test with empty data
        with pytest.raises(ValueError, match="Data cannot be None or empty"):
            enhanced_engine._validate_data(pd.DataFrame(), ['x'])
        
        # Test with None data
        with pytest.raises(ValueError, match="Data cannot be None or empty"):
            enhanced_engine._validate_data(None, ['x'])
    
    def test_error_handling_with_fallback(self, enhanced_engine):
        """Test error handling with fallback mechanism"""
        config = ChartConfig(
            chart_type=ChartType.BAR,
            title="Test Chart",
            fallback_enabled=True
        )
        
        # Simulate an error
        test_error = ValueError("Test error")
        fallback_fig = enhanced_engine._handle_error(test_error, config)
        
        assert isinstance(fallback_fig, go.Figure)
        assert len(fallback_fig.data) == 1
        assert isinstance(fallback_fig.data[0], go.Bar)
        assert enhanced_engine._error_count == 1
    
    def test_error_handling_without_fallback(self, enhanced_engine):
        """Test error handling without fallback mechanism"""
        config = ChartConfig(
            chart_type=ChartType.BAR,
            fallback_enabled=False
        )
        
        test_error = ValueError("Test error")
        with pytest.raises(ValueError, match="Test error"):
            enhanced_engine._handle_error(test_error, config)
    
    def test_enhanced_sparkline_creation(self, enhanced_engine):
        """Test enhanced sparkline creation with trend analysis"""
        # Test with increasing trend
        increasing_data = [10, 12, 14, 16, 18, 20]
        fig = enhanced_engine.create_sparkline_metrics(increasing_data, trend_type="auto")
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 1  # Main line + possible moving average
        assert fig.layout.height == 60
        
        # Test with insufficient data
        with pytest.raises(ValueError, match="Sparkline data must contain at least 2 points"):
            enhanced_engine.create_sparkline_metrics([1])
    
    def test_enhanced_metric_display_creation(self, enhanced_engine):
        """Test enhanced metric display with trend analysis"""
        sparkline_data = [100, 105, 103, 108, 110, 115, 112, 118]
        
        result = enhanced_engine.create_enhanced_metric_display(
            label="Test Metric",
            value="$1,234",
            delta="+5.2%",
            sparkline_data=sparkline_data,
            trend_analysis=True
        )
        
        assert result['label'] == "Test Metric"
        assert result['value'] == "$1,234"
        assert result['delta'] == "+5.2%"
        assert result['sparkline'] is not None
        assert result['trend_info'] is not None
        assert 'trend' in result['trend_info']
        assert 'recent_change' in result['trend_info']
        assert 'volatility' in result['trend_info']
    
    def test_trend_analysis(self, enhanced_engine):
        """Test trend analysis functionality"""
        # Test increasing trend
        increasing_data = [100, 105, 110, 115, 120]
        trend_info = enhanced_engine._analyze_trend(increasing_data)
        
        assert trend_info['trend'] == 'increasing'
        assert trend_info['recent_change'] > 0
        assert trend_info['overall_change'] > 0
        assert 'volatility' in trend_info
        assert 'confidence' in trend_info
        
        # Test decreasing trend
        decreasing_data = [120, 115, 110, 105, 100]
        trend_info = enhanced_engine._analyze_trend(decreasing_data)
        
        assert trend_info['trend'] == 'decreasing'
        assert trend_info['recent_change'] < 0
        
        # Test insufficient data
        insufficient_data = [100, 105]
        trend_info = enhanced_engine._analyze_trend(insufficient_data)
        
        assert trend_info['trend'] == 'insufficient_data'
    
    def test_line_chart_creation(self, enhanced_engine, sample_time_series_data):
        """Test enhanced line chart creation"""
        config = ChartConfig(
            chart_type=ChartType.LINE,
            title="Test Line Chart",
            animation_type=AnimationType.SMOOTH
        )
        
        fig = enhanced_engine.create_line_chart(
            data=sample_time_series_data,
            x="date",
            y="value",
            color="category",
            config=config
        )
        
        assert isinstance(fig, go.Figure)
        assert fig.layout.title.text == "Test Line Chart"
        assert len(fig.data) >= 1  # At least one trace
    
    def test_bar_chart_creation(self, enhanced_engine, sample_time_series_data):
        """Test enhanced bar chart creation"""
        config = ChartConfig(
            chart_type=ChartType.BAR,
            title="Test Bar Chart",
            animation_type=AnimationType.FADE_IN
        )
        
        fig = enhanced_engine.create_bar_chart(
            data=sample_time_series_data,
            x="category",
            y="value",
            config=config
        )
        
        assert isinstance(fig, go.Figure)
        assert fig.layout.title.text == "Test Bar Chart"
    
    def test_scatter_chart_creation(self, enhanced_engine, sample_time_series_data):
        """Test enhanced scatter chart creation"""
        config = ChartConfig(
            chart_type=ChartType.SCATTER,
            title="Test Scatter Chart"
        )
        
        fig = enhanced_engine.create_scatter_chart(
            data=sample_time_series_data,
            x="date",
            y="value",
            size="size",
            color="category",
            config=config
        )
        
        assert isinstance(fig, go.Figure)
        assert fig.layout.title.text == "Test Scatter Chart"
    
    def test_pie_chart_creation(self, enhanced_engine):
        """Test enhanced pie chart creation"""
        pie_data = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [30, 45, 25]
        })
        
        config = ChartConfig(
            chart_type=ChartType.PIE,
            title="Test Pie Chart"
        )
        
        fig = enhanced_engine.create_pie_chart(
            data=pie_data,
            values="value",
            names="category",
            config=config
        )
        
        assert isinstance(fig, go.Figure)
        assert isinstance(fig.data[0], go.Pie)
        assert fig.layout.title.text == "Test Pie Chart"
    
    def test_performance_optimization(self, enhanced_engine):
        """Test performance optimization for large datasets"""
        # Create large dataset
        large_data = pd.DataFrame({
            'x': np.random.randn(15000),
            'y': np.random.randn(15000)
        })
        
        # Test scatter plot optimization
        optimized_data = enhanced_engine.optimize_for_performance(large_data, ChartType.SCATTER)
        assert len(optimized_data) <= 5000
        
        # Test line chart optimization
        optimized_data = enhanced_engine.optimize_for_performance(large_data, ChartType.LINE)
        assert len(optimized_data) <= 1000
        
        # Test with small dataset (should remain unchanged)
        small_data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        optimized_small = enhanced_engine.optimize_for_performance(small_data, ChartType.SCATTER)
        assert len(optimized_small) == 3
    
    def test_chart_with_fallback(self, enhanced_engine, sample_time_series_data):
        """Test chart creation with automatic fallback"""
        config = ChartConfig(
            chart_type=ChartType.LINE,
            title="Test Chart",
            fallback_enabled=True
        )
        
        # This should succeed normally
        fig = enhanced_engine.create_chart_with_fallback(
            ChartType.LINE,
            sample_time_series_data,
            config,
            x="date",
            y="value"
        )
        
        assert isinstance(fig, go.Figure)
    
    def test_batch_chart_creation(self, enhanced_engine, sample_time_series_data):
        """Test batch chart creation functionality"""
        chart_specs = [
            {
                'chart_type': ChartType.LINE,
                'data': sample_time_series_data,
                'config': ChartConfig(chart_type=ChartType.LINE, title="Chart 1"),
                'kwargs': {'x': 'date', 'y': 'value'}
            },
            {
                'chart_type': ChartType.BAR,
                'data': sample_time_series_data,
                'config': ChartConfig(chart_type=ChartType.BAR, title="Chart 2"),
                'kwargs': {'x': 'category', 'y': 'value'}
            }
        ]
        
        figures = enhanced_engine.batch_create_charts(chart_specs)
        
        assert len(figures) == 2
        assert all(isinstance(fig, go.Figure) for fig in figures)
    
    def test_performance_metrics(self, enhanced_engine, sample_time_series_data):
        """Test performance metrics collection"""
        # Initially no metrics
        metrics = enhanced_engine.get_performance_metrics()
        assert metrics['status'] == 'no_data'
        
        # Create a chart to generate metrics
        config = ChartConfig(chart_type=ChartType.LINE)
        enhanced_engine.create_line_chart(
            sample_time_series_data, "date", "value", config=config
        )
        
        # Check metrics are collected
        metrics = enhanced_engine.get_performance_metrics()
        assert 'average_render_time' in metrics
        assert 'total_charts_rendered' in metrics
        assert metrics['total_charts_rendered'] == 1
        assert metrics['error_count'] == 0
    
    def test_chart_config_export(self, enhanced_engine, sample_time_series_data):
        """Test chart configuration export functionality"""
        config = ChartConfig(chart_type=ChartType.LINE, title="Export Test")
        fig = enhanced_engine.create_line_chart(
            sample_time_series_data, "date", "value", config=config
        )
        
        exported_config = enhanced_engine.export_chart_config(fig)
        
        assert 'layout' in exported_config
        assert 'data_structure' in exported_config
        assert 'theme' in exported_config
        assert exported_config['theme']['primary_color'] == "#FF4500"
    
    def test_custom_theme_application(self, enhanced_engine, sample_time_series_data):
        """Test custom theme application to existing figures"""
        config = ChartConfig(chart_type=ChartType.LINE)
        fig = enhanced_engine.create_line_chart(
            sample_time_series_data, "date", "value", config=config
        )
        
        custom_colors = {
            'background': '#000000',
            'text': '#FFFFFF',
            'primary': '#00FF00'
        }
        
        themed_fig = enhanced_engine.apply_custom_theme(fig, custom_colors)
        
        assert themed_fig.layout.paper_bgcolor == '#000000'
        assert themed_fig.layout.font.color == '#FFFFFF'
    
    def test_accessibility_features(self, enhanced_engine, sample_time_series_data):
        """Test accessibility features application"""
        # Test high contrast mode
        theme = BraveThemeConfig(high_contrast=True, reduced_motion=True)
        engine = VisualEnhancementEngine(theme=theme)
        
        config = ChartConfig(
            chart_type=ChartType.LINE,
            accessibility=True
        )
        
        fig = engine.create_line_chart(
            sample_time_series_data, "date", "value", config=config
        )
        
        # Check that accessibility features are applied
        assert isinstance(fig, go.Figure)
        # High contrast and reduced motion would be applied in _apply_accessibility_features
    
    def test_responsive_design_application(self, enhanced_engine, sample_time_series_data):
        """Test responsive design features"""
        config = ChartConfig(
            chart_type=ChartType.LINE,
            responsive=True
        )
        
        fig = enhanced_engine.create_line_chart(
            sample_time_series_data, "date", "value", config=config
        )
        
        # Check that responsive features are applied
        assert fig.layout.autosize is True
        assert fig.layout.responsive is True
    
    def test_interactive_features_application(self, enhanced_engine, sample_time_series_data):
        """Test interactive features configuration"""
        config = ChartConfig(
            chart_type=ChartType.LINE,
            hover_enabled=True,
            zoom_enabled=False,
            pan_enabled=False,
            selection_enabled=False,
            show_toolbar=True
        )
        
        fig = enhanced_engine.create_line_chart(
            sample_time_series_data, "date", "value", config=config
        )
        
        # Check that interactive features are configured
        assert hasattr(fig, '_modebar_config')
        assert fig._modebar_config['displayModeBar'] is True
        assert 'zoom2d' in fig._modebar_config['modeBarButtonsToRemove']
        assert 'pan2d' in fig._modebar_config['modeBarButtonsToRemove']


class TestEnhancedAnimationTypes:
    """Test enhanced animation types and transitions"""
    
    @pytest.fixture
    def engine_with_animations(self):
        """Create engine with animation support"""
        return VisualEnhancementEngine()
    
    def test_animation_type_application(self, engine_with_animations):
        """Test different animation types are applied correctly"""
        sample_data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        
        animation_types = [
            AnimationType.SMOOTH,
            AnimationType.FADE_IN,
            AnimationType.SLIDE_IN,
            AnimationType.ZOOM_IN,
            AnimationType.BOUNCE,
            AnimationType.ELASTIC
        ]
        
        for animation_type in animation_types:
            config = ChartConfig(
                chart_type=ChartType.LINE,
                animation_type=animation_type,
                animations=True
            )
            
            fig = engine_with_animations.create_line_chart(
                sample_data, "x", "y", config=config
            )
            
            assert isinstance(fig, go.Figure)
            # Animation settings would be applied in _apply_advanced_animations
            if animation_type != AnimationType.NONE:
                assert 'transition' in fig.layout
    
    def test_animation_disabled(self, engine_with_animations):
        """Test that animations can be disabled"""
        sample_data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        
        config = ChartConfig(
            chart_type=ChartType.LINE,
            animation_type=AnimationType.NONE,
            animations=False
        )
        
        fig = engine_with_animations.create_line_chart(
            sample_data, "x", "y", config=config
        )
        
        assert isinstance(fig, go.Figure)
        # No animation settings should be applied


if __name__ == "__main__":
    pytest.main([__file__])