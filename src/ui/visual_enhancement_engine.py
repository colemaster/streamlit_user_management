"""
Visual Enhancement Engine - Plotly 6.5.2+ Integration
Enhanced visualization components with advanced interactive features, animations,
sparkline integration, and comprehensive error handling.

Features:
- Interactive chart creation with modern Plotly features
- Advanced animation and transition support
- Sparkline integration for st.metric enhancement
- Responsive design and accessibility features
- Comprehensive error handling and fallback mechanisms
- Brave Design theme integration
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import warnings


class ChartType(Enum):
    """Supported chart types in the Visual Enhancement Engine"""
    SUNBURST = "sunburst"
    SANKEY = "sankey"
    TREEMAP = "treemap"
    VIOLIN = "violin"
    SCATTER_3D = "scatter_3d"
    SURFACE_3D = "surface_3d"
    MESH_3D = "mesh_3d"
    BOX = "box"
    HISTOGRAM = "histogram"
    DENSITY_HEATMAP = "density_heatmap"
    LINE = "line"
    BAR = "bar"
    SCATTER = "scatter"
    PIE = "pie"
    AREA = "area"
    FUNNEL = "funnel"
    WATERFALL = "waterfall"
    CANDLESTICK = "candlestick"
    OHLC = "ohlc"


class AnimationType(Enum):
    """Animation types for enhanced transitions"""
    FADE_IN = "fade_in"
    SLIDE_IN = "slide_in"
    ZOOM_IN = "zoom_in"
    BOUNCE = "bounce"
    ELASTIC = "elastic"
    SMOOTH = "smooth"
    NONE = "none"


class ResponsiveBreakpoint(Enum):
    """Responsive design breakpoints"""
    MOBILE = 480
    TABLET = 768
    DESKTOP = 1024
    LARGE = 1440


@dataclass
class BraveThemeConfig:
    """Brave Design theme configuration for charts"""
    primary_orange: str = "#FF4500"
    secondary_orange: str = "#FF8C00"
    dark_background: str = "#1a1a1a"
    glass_overlay: str = "rgba(255, 255, 255, 0.1)"
    text_primary: str = "#FFFFFF"
    text_secondary: str = "#888888"
    success_color: str = "#00FF9D"
    warning_color: str = "#FFD700"
    error_color: str = "#FF0055"
    
    # Enhanced color palette for multi-series charts
    color_palette: List[str] = field(default_factory=list)
    
    # Animation settings
    animation_duration: int = 500
    transition_easing: str = "cubic-in-out"
    
    # Responsive settings
    mobile_height: int = 300
    tablet_height: int = 400
    desktop_height: int = 500
    
    # Accessibility settings
    high_contrast: bool = False
    reduced_motion: bool = False
    
    def __post_init__(self):
        if not self.color_palette:
            self.color_palette = [
                self.primary_orange,
                self.secondary_orange,
                self.success_color,
                self.warning_color,
                self.error_color,
                "#00BFFF",  # Deep Sky Blue
                "#9370DB",  # Medium Purple
                "#32CD32",  # Lime Green
                "#FF69B4",  # Hot Pink
                "#FFA500",  # Orange
                "#20B2AA",  # Light Sea Green
                "#DDA0DD",  # Plum
            ]
    
    def get_responsive_height(self, breakpoint: ResponsiveBreakpoint) -> int:
        """Get height based on responsive breakpoint"""
        if breakpoint == ResponsiveBreakpoint.MOBILE:
            return self.mobile_height
        elif breakpoint == ResponsiveBreakpoint.TABLET:
            return self.tablet_height
        else:
            return self.desktop_height


@dataclass
class ChartConfig:
    """Enhanced configuration for chart creation"""
    chart_type: ChartType
    title: str = ""
    theme: BraveThemeConfig = field(default_factory=BraveThemeConfig)
    animations: bool = True
    animation_type: AnimationType = AnimationType.SMOOTH
    responsive: bool = True
    accessibility: bool = True
    sparkline_enabled: bool = False
    height: int = 400
    width: Optional[int] = None
    
    # Interactive features
    hover_enabled: bool = True
    zoom_enabled: bool = True
    pan_enabled: bool = True
    selection_enabled: bool = True
    
    # Error handling
    fallback_enabled: bool = True
    error_callback: Optional[Callable] = None
    
    # Performance settings
    max_data_points: int = 10000
    enable_webgl: bool = False
    
    # Custom styling
    custom_css: Optional[str] = None
    show_toolbar: bool = True
    
    def get_responsive_config(self, viewport_width: int) -> Dict[str, Any]:
        """Get responsive configuration based on viewport width"""
        if viewport_width <= ResponsiveBreakpoint.MOBILE.value:
            return {
                'height': self.theme.mobile_height,
                'show_toolbar': False,
                'title_font_size': 16
            }
        elif viewport_width <= ResponsiveBreakpoint.TABLET.value:
            return {
                'height': self.theme.tablet_height,
                'show_toolbar': True,
                'title_font_size': 20
            }
        else:
            return {
                'height': self.theme.desktop_height,
                'show_toolbar': True,
                'title_font_size': 24
            }


class VisualEnhancementEngine:
    """
    Enhanced visualization engine leveraging Plotly 6.5.2+ features
    with comprehensive interactive capabilities, animations, and error handling.
    """
    
    def __init__(self, theme: BraveThemeConfig = None):
        self.theme = theme or BraveThemeConfig()
        self._base_layout = self._create_base_layout()
        self.logger = logging.getLogger(__name__)
        
        # Performance monitoring
        self._render_times = []
        self._error_count = 0
        
        # Cache for frequently used configurations
        self._layout_cache = {}
    
    def _handle_error(self, error: Exception, config: ChartConfig, 
                     fallback_chart_type: ChartType = ChartType.BAR) -> go.Figure:
        """Handle errors with graceful fallbacks"""
        self._error_count += 1
        self.logger.error(f"Chart creation error: {str(error)}")
        
        if config.error_callback:
            config.error_callback(error)
        
        if config.fallback_enabled:
            try:
                # Create a simple fallback chart
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=["Error"],
                    y=[1],
                    marker_color=self.theme.error_color,
                    text=["Chart Error - Using Fallback"],
                    textposition="inside"
                ))
                
                fig.update_layout(
                    title=f"Error in {config.title or 'Chart'}",
                    paper_bgcolor=self.theme.dark_background,
                    plot_bgcolor=self.theme.dark_background,
                    font_color=self.theme.text_primary,
                    height=config.height
                )
                
                return fig
            except Exception as fallback_error:
                self.logger.error(f"Fallback chart creation failed: {str(fallback_error)}")
                # Return minimal figure as last resort
                return go.Figure()
        else:
            raise error
    
    def _validate_data(self, data: pd.DataFrame, required_columns: List[str]) -> bool:
        """Validate input data for chart creation"""
        if data is None or data.empty:
            raise ValueError("Data cannot be None or empty")
        
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check for reasonable data size
        if len(data) > 50000:  # Large dataset warning
            warnings.warn(f"Large dataset ({len(data)} rows) may impact performance")
        
        return True
    
    def _apply_responsive_design(self, fig: go.Figure, config: ChartConfig) -> go.Figure:
        """Apply responsive design configurations"""
        if not config.responsive:
            return fig
        
        # Add responsive configuration to layout
        fig.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        # Add CSS for responsive behavior
        if config.custom_css:
            # This would be handled by Streamlit's custom CSS injection
            pass
        
        return fig
    
    def _apply_accessibility_features(self, fig: go.Figure, config: ChartConfig) -> go.Figure:
        """Apply accessibility enhancements"""
        if not config.accessibility:
            return fig
        
        # High contrast mode
        if self.theme.high_contrast:
            fig.update_layout(
                font_color="#FFFFFF",
                paper_bgcolor="#000000",
                plot_bgcolor="#000000"
            )
        
        # Reduced motion
        if self.theme.reduced_motion:
            fig.update_layout(transition_duration=0)
        
        # Enhanced hover information
        for trace in fig.data:
            if hasattr(trace, 'hovertemplate') and not trace.hovertemplate:
                trace.hovertemplate = '<b>%{fullData.name}</b><br>Value: %{y}<extra></extra>'
        
        return fig
    
    def _apply_advanced_animations(self, fig: go.Figure, config: ChartConfig) -> go.Figure:
        """Apply advanced animation and transition effects"""
        if not config.animations or config.animation_type == AnimationType.NONE:
            return fig
        
        duration = self.theme.animation_duration
        easing = self.theme.transition_easing
        
        if config.animation_type == AnimationType.FADE_IN:
            fig.update_layout(
                transition={
                    'duration': duration,
                    'easing': 'ease-in-out'
                }
            )
        elif config.animation_type == AnimationType.SLIDE_IN:
            fig.update_layout(
                transition={
                    'duration': duration,
                    'easing': 'ease-out'
                }
            )
        elif config.animation_type == AnimationType.ZOOM_IN:
            fig.update_layout(
                transition={
                    'duration': duration * 1.5,
                    'easing': 'ease-in-out'
                }
            )
        elif config.animation_type == AnimationType.BOUNCE:
            fig.update_layout(
                transition={
                    'duration': duration * 2,
                    'easing': 'bounce-in-out'
                }
            )
        elif config.animation_type == AnimationType.ELASTIC:
            fig.update_layout(
                transition={
                    'duration': duration * 1.8,
                    'easing': 'elastic-in-out'
                }
            )
        else:  # SMOOTH
            fig.update_layout(
                transition={
                    'duration': duration,
                    'easing': easing
                }
            )
        
        return fig
    
    def _apply_interactive_features(self, fig: go.Figure, config: ChartConfig) -> go.Figure:
        """Apply interactive features to charts"""
        # Configure modebar (toolbar)
        modebar_config = {
            'displayModeBar': config.show_toolbar,
            'displaylogo': False,
            'modeBarButtonsToRemove': []
        }
        
        if not config.zoom_enabled:
            modebar_config['modeBarButtonsToRemove'].extend(['zoom2d', 'zoomIn2d', 'zoomOut2d'])
        
        if not config.pan_enabled:
            modebar_config['modeBarButtonsToRemove'].append('pan2d')
        
        if not config.selection_enabled:
            modebar_config['modeBarButtonsToRemove'].extend(['select2d', 'lasso2d'])
        
        # Apply hover settings
        if config.hover_enabled:
            fig.update_layout(hovermode='closest')
        else:
            fig.update_layout(hovermode=False)
        
        # Store config for use in Streamlit
        fig._modebar_config = modebar_config
        
        return fig
    
    def _apply_layout(self, fig: go.Figure, config: ChartConfig) -> go.Figure:
        """Apply comprehensive layout configuration to figure"""
        try:
            # Create a copy of base layout
            layout_updates = self._base_layout.copy()
            
            # Update title configuration
            if config.title:
                layout_updates['title'].update({'text': config.title})
            
            # Add height and width if specified
            if config.height:
                layout_updates['height'] = config.height
            if config.width:
                layout_updates['width'] = config.width
                
            fig.update_layout(**layout_updates)
            
            # Apply all enhancements
            fig = self._apply_responsive_design(fig, config)
            fig = self._apply_accessibility_features(fig, config)
            fig = self._apply_advanced_animations(fig, config)
            fig = self._apply_interactive_features(fig, config)
            
            return fig
            
        except Exception as e:
            return self._handle_error(e, config)
    
    def _create_base_layout(self) -> Dict[str, Any]:
        """Create base layout with Brave Design theme"""
        return {
            'paper_bgcolor': self.theme.dark_background,
            'plot_bgcolor': self.theme.dark_background,
            'font': {
                'family': 'Rajdhani, sans-serif',
                'size': 12,
                'color': self.theme.text_primary
            },
            'title': {
                'font': {
                    'family': 'Rajdhani, sans-serif',
                    'size': 24,
                    'color': self.theme.text_primary
                },
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'gridcolor': 'rgba(255, 255, 255, 0.1)',
                'zerolinecolor': 'rgba(255, 255, 255, 0.2)',
                'color': self.theme.text_secondary
            },
            'yaxis': {
                'gridcolor': 'rgba(255, 255, 255, 0.1)',
                'zerolinecolor': 'rgba(255, 255, 255, 0.2)',
                'color': self.theme.text_secondary
            },
            'legend': {
                'font': {'color': self.theme.text_primary},
                'bgcolor': 'rgba(0, 0, 0, 0.5)',
                'bordercolor': self.theme.primary_orange,
                'borderwidth': 1
            }
        }
    
    def create_sunburst_chart(self, data: pd.DataFrame, 
                            ids: str, parents: str, values: str,
                            config: ChartConfig = None) -> go.Figure:
        """
        Create an interactive sunburst chart for hierarchical data visualization.
        
        Args:
            data: DataFrame with hierarchical data
            ids: Column name for unique identifiers
            parents: Column name for parent relationships
            values: Column name for values/sizes
            config: Chart configuration
        """
        if config is None:
            config = ChartConfig(chart_type=ChartType.SUNBURST)
            
        fig = go.Figure(go.Sunburst(
            ids=data[ids],
            labels=data[ids],
            parents=data[parents],
            values=data[values],
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percentParent}<extra></extra>',
            maxdepth=4,
            insidetextorientation='radial'
        ))
        
        # Apply Brave theme
        fig.update_traces(
            marker=dict(
                colors=self.theme.color_palette,
                line=dict(color=self.theme.primary_orange, width=2)
            )
        )
        
        return self._apply_layout(fig, config)
    
    def create_sankey_diagram(self, data: pd.DataFrame,
                            source: str, target: str, value: str,
                            config: ChartConfig = None) -> go.Figure:
        """
        Create a Sankey diagram for flow visualization.
        
        Args:
            data: DataFrame with flow data
            source: Column name for source nodes
            target: Column name for target nodes  
            value: Column name for flow values
            config: Chart configuration
        """
        if config is None:
            config = ChartConfig(chart_type=ChartType.SANKEY)
            
        # Create unique node list
        all_nodes = list(set(data[source].tolist() + data[target].tolist()))
        node_dict = {node: i for i, node in enumerate(all_nodes)}
        
        # Map source and target to indices
        source_indices = [node_dict[node] for node in data[source]]
        target_indices = [node_dict[node] for node in data[target]]
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color=self.theme.primary_orange, width=2),
                label=all_nodes,
                color=[self.theme.primary_orange if i % 2 == 0 else self.theme.secondary_orange 
                      for i in range(len(all_nodes))]
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=data[value].tolist(),
                color=[f"rgba(255, 69, 0, 0.3)" for _ in range(len(data))]
            )
        )])
        
        return self._apply_layout(fig, config)
    
    def create_treemap_chart(self, data: pd.DataFrame,
                           ids: str, parents: str, values: str,
                           config: ChartConfig = None) -> go.Figure:
        """
        Create a treemap chart for hierarchical data with area-based visualization.
        
        Args:
            data: DataFrame with hierarchical data
            ids: Column name for unique identifiers
            parents: Column name for parent relationships
            values: Column name for values/sizes
            config: Chart configuration
        """
        if config is None:
            config = ChartConfig(chart_type=ChartType.TREEMAP)
            
        fig = go.Figure(go.Treemap(
            ids=data[ids],
            labels=data[ids],
            parents=data[parents],
            values=data[values],
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percentParent}<extra></extra>',
            maxdepth=4,
            textinfo="label+value+percent parent"
        ))
        
        # Apply Brave theme colors
        fig.update_traces(
            marker=dict(
                colors=self.theme.color_palette,
                line=dict(color=self.theme.primary_orange, width=2)
            ),
            textfont=dict(color=self.theme.text_primary, size=12)
        )
        
        return self._apply_layout(fig, config)
    
    def create_violin_plot(self, data: pd.DataFrame,
                         x: str, y: str, color: Optional[str] = None,
                         config: ChartConfig = None) -> go.Figure:
        """
        Create violin plots for distribution visualization.
        
        Args:
            data: DataFrame with data
            x: Column name for x-axis (categorical)
            y: Column name for y-axis (numerical)
            color: Optional column name for color grouping
            config: Chart configuration
        """
        if config is None:
            config = ChartConfig(chart_type=ChartType.VIOLIN)
            
        if color:
            fig = px.violin(data, x=x, y=y, color=color,
                          color_discrete_sequence=self.theme.color_palette)
        else:
            fig = px.violin(data, x=x, y=y)
            fig.update_traces(fillcolor=self.theme.primary_orange,
                            line_color=self.theme.secondary_orange)
        
        # Enhance with box plot overlay
        fig.update_traces(
            meanline_visible=True,
            box_visible=True,
            box_fillcolor=self.theme.glass_overlay,
            box_line_color=self.theme.text_primary
        )
        
        return self._apply_layout(fig, config)
    
    def create_3d_scatter(self, data: pd.DataFrame,
                        x: str, y: str, z: str,
                        size: Optional[str] = None,
                        color: Optional[str] = None,
                        config: ChartConfig = None) -> go.Figure:
        """
        Create 3D scatter plot for multidimensional data visualization.
        
        Args:
            data: DataFrame with data
            x, y, z: Column names for 3D coordinates
            size: Optional column name for marker size
            color: Optional column name for color mapping
            config: Chart configuration
        """
        if config is None:
            config = ChartConfig(chart_type=ChartType.SCATTER_3D)
            
        fig = px.scatter_3d(
            data, x=x, y=y, z=z,
            size=size, color=color,
            color_continuous_scale=[[0, self.theme.primary_orange], 
                                  [1, self.theme.secondary_orange]]
        )
        
        fig.update_traces(
            marker=dict(
                line=dict(color=self.theme.text_primary, width=1),
                opacity=0.8
            )
        )
        
        # Apply base layout first
        fig = self._apply_layout(fig, config)
        
        # Then add 3D scene configuration
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    backgroundcolor=self.theme.dark_background,
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showbackground=True,
                    zerolinecolor='rgba(255, 255, 255, 0.2)',
                    color=self.theme.text_secondary
                ),
                yaxis=dict(
                    backgroundcolor=self.theme.dark_background,
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showbackground=True,
                    zerolinecolor='rgba(255, 255, 255, 0.2)',
                    color=self.theme.text_secondary
                ),
                zaxis=dict(
                    backgroundcolor=self.theme.dark_background,
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showbackground=True,
                    zerolinecolor='rgba(255, 255, 255, 0.2)',
                    color=self.theme.text_secondary
                ),
                bgcolor=self.theme.dark_background
            )
        )
        
        return fig
    
    def create_3d_surface(self, z_data: np.ndarray,
                        x_labels: Optional[List] = None,
                        y_labels: Optional[List] = None,
                        config: ChartConfig = None) -> go.Figure:
        """
        Create 3D surface plot for continuous data visualization.
        
        Args:
            z_data: 2D numpy array for surface heights
            x_labels: Optional labels for x-axis
            y_labels: Optional labels for y-axis
            config: Chart configuration
        """
        if config is None:
            config = ChartConfig(chart_type=ChartType.SURFACE_3D)
            
        fig = go.Figure(data=[go.Surface(
            z=z_data,
            x=x_labels,
            y=y_labels,
            colorscale=[[0, self.theme.primary_orange], 
                       [0.5, self.theme.secondary_orange],
                       [1, self.theme.success_color]],
            opacity=0.9,
            contours={
                "z": {"show": True, "usecolormap": True,
                      "highlightcolor": self.theme.text_primary, "project": {"z": True}}
            }
        )])
        
        # Apply base layout first
        fig = self._apply_layout(fig, config)
        
        # Then add 3D scene configuration
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    backgroundcolor=self.theme.dark_background,
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showbackground=True,
                    color=self.theme.text_secondary
                ),
                yaxis=dict(
                    backgroundcolor=self.theme.dark_background,
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showbackground=True,
                    color=self.theme.text_secondary
                ),
                zaxis=dict(
                    backgroundcolor=self.theme.dark_background,
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showbackground=True,
                    color=self.theme.text_secondary
                ),
                bgcolor=self.theme.dark_background
            )
        )
        
        return fig
    
    def create_sparkline_metrics(self, data: List[float], 
                               color: str = None,
                               trend_type: str = "auto") -> go.Figure:
        """
        Create enhanced sparkline charts for st.metric integration.
        
        Args:
            data: List of numerical values for the sparkline
            color: Optional color override
            trend_type: Type of trend visualization ('auto', 'positive', 'negative', 'neutral')
        """
        try:
            if not data or len(data) < 2:
                raise ValueError("Sparkline data must contain at least 2 points")
            
            # Determine color based on trend
            if color is None:
                if trend_type == "auto":
                    # Auto-detect trend
                    trend = data[-1] - data[0]
                    if trend > 0:
                        color = self.theme.success_color
                    elif trend < 0:
                        color = self.theme.error_color
                    else:
                        color = self.theme.primary_orange
                elif trend_type == "positive":
                    color = self.theme.success_color
                elif trend_type == "negative":
                    color = self.theme.error_color
                else:
                    color = self.theme.primary_orange
            
            fig = go.Figure()
            
            # Add main sparkline
            fig.add_trace(go.Scatter(
                y=data,
                mode='lines',
                line=dict(color=color, width=2),
                fill='tonexty',
                fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.3)',
                showlegend=False,
                hovertemplate='Value: %{y}<extra></extra>'
            ))
            
            # Add trend indicators
            if len(data) > 5:
                # Add moving average line
                window = min(3, len(data) // 3)
                moving_avg = pd.Series(data).rolling(window=window, center=True).mean().bfill().ffill()
                
                fig.add_trace(go.Scatter(
                    y=moving_avg,
                    mode='lines',
                    line=dict(color=color, width=1, dash='dot'),
                    opacity=0.7,
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
            fig.update_layout(
                height=60,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Sparkline creation error: {str(e)}")
            # Return minimal sparkline
            return self._create_minimal_sparkline(data or [0, 1])
    
    def _create_minimal_sparkline(self, data: List[float]) -> go.Figure:
        """Create a minimal sparkline as fallback"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=data,
            mode='lines',
            line=dict(color=self.theme.primary_orange, width=1),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            height=60,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )
        
        return fig
    
    def create_enhanced_metric_display(self, 
                                     label: str,
                                     value: Union[str, int, float],
                                     delta: Optional[str] = None,
                                     sparkline_data: Optional[List[float]] = None,
                                     trend_analysis: bool = True) -> Dict[str, Any]:
        """
        Create enhanced metric display with integrated sparkline and trend analysis.
        
        Args:
            label: Metric label
            value: Current metric value
            delta: Change indicator (e.g., "+12.5%")
            sparkline_data: Historical data for sparkline
            trend_analysis: Whether to include trend analysis
            
        Returns:
            Dictionary with metric data and sparkline figure
        """
        try:
            result = {
                'label': label,
                'value': value,
                'delta': delta,
                'sparkline': None,
                'trend_info': None
            }
            
            if sparkline_data and len(sparkline_data) >= 2:
                # Create sparkline
                result['sparkline'] = self.create_sparkline_metrics(sparkline_data)
                
                if trend_analysis:
                    # Perform trend analysis
                    trend_info = self._analyze_trend(sparkline_data)
                    result['trend_info'] = trend_info
            
            return result
            
        except Exception as e:
            self.logger.error(f"Enhanced metric creation error: {str(e)}")
            return {
                'label': label,
                'value': value,
                'delta': delta,
                'sparkline': None,
                'trend_info': None
            }
    
    def _analyze_trend(self, data: List[float]) -> Dict[str, Any]:
        """Analyze trend in data for enhanced metrics"""
        if len(data) < 3:
            return {'trend': 'insufficient_data'}
        
        # Calculate various trend indicators
        recent_trend = (data[-1] - data[-3]) / data[-3] if data[-3] != 0 else 0
        overall_trend = (data[-1] - data[0]) / data[0] if data[0] != 0 else 0
        
        # Calculate volatility
        volatility = np.std(data) / np.mean(data) if np.mean(data) != 0 else 0
        
        # Determine trend direction
        if recent_trend > 0.05:
            direction = 'increasing'
        elif recent_trend < -0.05:
            direction = 'decreasing'
        else:
            direction = 'stable'
        
        return {
            'trend': direction,
            'recent_change': recent_trend,
            'overall_change': overall_trend,
            'volatility': volatility,
            'confidence': min(1.0, len(data) / 10)  # More data = higher confidence
        }
    
    def apply_brave_theme(self, figure: go.Figure) -> go.Figure:
        """
        Apply Brave Design theme to any existing Plotly figure.
        
        Args:
            figure: Existing Plotly figure
        """
        figure.update_layout(**self._base_layout)
        
        # Update trace colors if not already set
        for i, trace in enumerate(figure.data):
            if hasattr(trace, 'marker') and trace.marker.color is None:
                trace.marker.color = self.theme.color_palette[i % len(self.theme.color_palette)]
        
        return figure
    
    def add_animations(self, figure: go.Figure, 
                      duration: int = 500) -> go.Figure:
        """
        Add smooth animations and transitions to charts.
        
        Args:
            figure: Plotly figure to animate
            duration: Animation duration in milliseconds
        """
        figure.update_layout(
            transition_duration=duration,
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=list([
                        dict(
                            args=[{"visible": [True] * len(figure.data)}],
                            label="Play",
                            method="restyle"
                        )
                    ]),
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.01,
                    xanchor="left",
                    y=1.02,
                    yanchor="top"
                ),
            ]
        )
        
        return figure
    
    def create_interactive_chart(self, chart_type: ChartType, 
                               data: pd.DataFrame,
                               config: ChartConfig,
                               **kwargs) -> go.Figure:
        """
        Create enhanced interactive charts with modern features, comprehensive error handling,
        and performance monitoring.
        
        Args:
            chart_type: Type of chart to create
            data: DataFrame with chart data
            config: Chart configuration
            **kwargs: Additional arguments specific to chart type
        """
        import time
        start_time = time.time()
        
        try:
            # Validate inputs
            if data is not None:
                self._validate_data(data, kwargs.get('required_columns', []))
            
            # Performance check for large datasets
            if data is not None and len(data) > config.max_data_points:
                if config.enable_webgl:
                    # Use WebGL for better performance with large datasets
                    kwargs['render_mode'] = 'webgl'
                else:
                    # Sample data to improve performance
                    data = data.sample(n=config.max_data_points)
                    self.logger.warning(f"Data sampled to {config.max_data_points} points for performance")
            
            # Route to appropriate chart creation method
            if chart_type == ChartType.SUNBURST:
                fig = self.create_sunburst_chart(data, config=config, **kwargs)
            elif chart_type == ChartType.SANKEY:
                fig = self.create_sankey_diagram(data, config=config, **kwargs)
            elif chart_type == ChartType.TREEMAP:
                fig = self.create_treemap_chart(data, config=config, **kwargs)
            elif chart_type == ChartType.VIOLIN:
                fig = self.create_violin_plot(data, config=config, **kwargs)
            elif chart_type == ChartType.SCATTER_3D:
                fig = self.create_3d_scatter(data, config=config, **kwargs)
            elif chart_type == ChartType.SURFACE_3D:
                fig = self.create_3d_surface(config=config, **kwargs)
            elif chart_type == ChartType.LINE:
                fig = self.create_line_chart(data, config=config, **kwargs)
            elif chart_type == ChartType.BAR:
                fig = self.create_bar_chart(data, config=config, **kwargs)
            elif chart_type == ChartType.SCATTER:
                fig = self.create_scatter_chart(data, config=config, **kwargs)
            elif chart_type == ChartType.PIE:
                fig = self.create_pie_chart(data, config=config, **kwargs)
            elif chart_type == ChartType.AREA:
                fig = self.create_area_chart(data, config=config, **kwargs)
            elif chart_type == ChartType.BOX:
                fig = self.create_box_plot(data, config=config, **kwargs)
            elif chart_type == ChartType.HISTOGRAM:
                fig = self.create_histogram(data, config=config, **kwargs)
            else:
                raise ValueError(f"Unsupported chart type: {chart_type}")
            
            # Record performance metrics
            render_time = time.time() - start_time
            self._render_times.append(render_time)
            
            if render_time > 2.0:  # Warn if rendering takes more than 2 seconds
                self.logger.warning(f"Slow chart rendering: {render_time:.2f}s for {chart_type}")
            
            return fig
            
        except Exception as e:
            return self._handle_error(e, config)
    
    def create_line_chart(self, data: pd.DataFrame, 
                         x: str, y: str, 
                         color: Optional[str] = None,
                         config: ChartConfig = None) -> go.Figure:
        """Create enhanced line chart with animations and interactions"""
        if config is None:
            config = ChartConfig(chart_type=ChartType.LINE)
        
        try:
            self._validate_data(data, [x, y])
            
            if color:
                fig = px.line(data, x=x, y=y, color=color,
                            color_discrete_sequence=self.theme.color_palette)
            else:
                fig = px.line(data, x=x, y=y)
                fig.update_traces(line_color=self.theme.primary_orange)
            
            return self._apply_layout(fig, config)
            
        except Exception as e:
            return self._handle_error(e, config)
    
    def create_bar_chart(self, data: pd.DataFrame,
                        x: str, y: str,
                        color: Optional[str] = None,
                        config: ChartConfig = None) -> go.Figure:
        """Create enhanced bar chart with animations and interactions"""
        if config is None:
            config = ChartConfig(chart_type=ChartType.BAR)
        
        try:
            self._validate_data(data, [x, y])
            
            if color:
                fig = px.bar(data, x=x, y=y, color=color,
                           color_discrete_sequence=self.theme.color_palette)
            else:
                fig = px.bar(data, x=x, y=y)
                fig.update_traces(marker_color=self.theme.primary_orange)
            
            return self._apply_layout(fig, config)
            
        except Exception as e:
            return self._handle_error(e, config)
    
    def create_scatter_chart(self, data: pd.DataFrame,
                           x: str, y: str,
                           size: Optional[str] = None,
                           color: Optional[str] = None,
                           config: ChartConfig = None) -> go.Figure:
        """Create enhanced scatter chart with animations and interactions"""
        if config is None:
            config = ChartConfig(chart_type=ChartType.SCATTER)
        
        try:
            self._validate_data(data, [x, y])
            
            fig = px.scatter(data, x=x, y=y, size=size, color=color,
                           color_continuous_scale=[[0, self.theme.primary_orange], 
                                                 [1, self.theme.secondary_orange]])
            
            return self._apply_layout(fig, config)
            
        except Exception as e:
            return self._handle_error(e, config)
    
    def create_pie_chart(self, data: pd.DataFrame,
                        values: str, names: str,
                        config: ChartConfig = None) -> go.Figure:
        """Create enhanced pie chart with animations and interactions"""
        if config is None:
            config = ChartConfig(chart_type=ChartType.PIE)
        
        try:
            self._validate_data(data, [values, names])
            
            fig = px.pie(data, values=values, names=names,
                        color_discrete_sequence=self.theme.color_palette)
            
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
            
            return self._apply_layout(fig, config)
            
        except Exception as e:
            return self._handle_error(e, config)
    
    def create_area_chart(self, data: pd.DataFrame,
                         x: str, y: str,
                         color: Optional[str] = None,
                         config: ChartConfig = None) -> go.Figure:
        """Create enhanced area chart with animations and interactions"""
        if config is None:
            config = ChartConfig(chart_type=ChartType.AREA)
        
        try:
            self._validate_data(data, [x, y])
            
            if color:
                fig = px.area(data, x=x, y=y, color=color,
                            color_discrete_sequence=self.theme.color_palette)
            else:
                fig = px.area(data, x=x, y=y)
                fig.update_traces(fill='tonexty', fillcolor=f'rgba({int(self.theme.primary_orange[1:3], 16)}, {int(self.theme.primary_orange[3:5], 16)}, {int(self.theme.primary_orange[5:7], 16)}, 0.6)')
            
            return self._apply_layout(fig, config)
            
        except Exception as e:
            return self._handle_error(e, config)
    
    def create_box_plot(self, data: pd.DataFrame,
                       x: str, y: str,
                       color: Optional[str] = None,
                       config: ChartConfig = None) -> go.Figure:
        """Create enhanced box plot with animations and interactions"""
        if config is None:
            config = ChartConfig(chart_type=ChartType.BOX)
        
        try:
            self._validate_data(data, [x, y])
            
            if color:
                fig = px.box(data, x=x, y=y, color=color,
                           color_discrete_sequence=self.theme.color_palette)
            else:
                fig = px.box(data, x=x, y=y)
                fig.update_traces(marker_color=self.theme.primary_orange,
                                line_color=self.theme.secondary_orange)
            
            return self._apply_layout(fig, config)
            
        except Exception as e:
            return self._handle_error(e, config)
    
    def create_histogram(self, data: pd.DataFrame,
                        x: str,
                        color: Optional[str] = None,
                        config: ChartConfig = None) -> go.Figure:
        """Create enhanced histogram with animations and interactions"""
        if config is None:
            config = ChartConfig(chart_type=ChartType.HISTOGRAM)
        
        try:
            self._validate_data(data, [x])
            
            if color:
                fig = px.histogram(data, x=x, color=color,
                                 color_discrete_sequence=self.theme.color_palette)
            else:
                fig = px.histogram(data, x=x)
                fig.update_traces(marker_color=self.theme.primary_orange,
                                marker_line_color=self.theme.secondary_orange,
                                marker_line_width=1)
            
            return self._apply_layout(fig, config)
            
        except Exception as e:
            return self._handle_error(e, config)

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the visualization engine"""
        if not self._render_times:
            return {'status': 'no_data'}
        
        return {
            'average_render_time': np.mean(self._render_times),
            'max_render_time': max(self._render_times),
            'min_render_time': min(self._render_times),
            'total_charts_rendered': len(self._render_times),
            'error_count': self._error_count,
            'error_rate': self._error_count / len(self._render_times) if self._render_times else 0
        }
    
    def optimize_for_performance(self, data: pd.DataFrame, 
                               chart_type: ChartType) -> pd.DataFrame:
        """Optimize data for better chart performance"""
        if data is None or data.empty:
            return data
        
        # For large datasets, apply sampling strategies
        if len(data) > 10000:
            if chart_type in [ChartType.SCATTER, ChartType.SCATTER_3D]:
                # For scatter plots, use systematic sampling
                step = len(data) // 5000
                return data.iloc[::step]
            elif chart_type in [ChartType.LINE, ChartType.AREA]:
                # For time series, preserve temporal structure
                return data.iloc[::max(1, len(data) // 1000)]
            else:
                # For other charts, use random sampling
                return data.sample(n=min(5000, len(data)))
        
        return data
    
    def create_chart_with_fallback(self, chart_type: ChartType,
                                 data: pd.DataFrame,
                                 config: ChartConfig,
                                 fallback_type: ChartType = ChartType.BAR,
                                 **kwargs) -> go.Figure:
        """Create chart with automatic fallback to simpler chart type on error"""
        try:
            return self.create_interactive_chart(chart_type, data, config, **kwargs)
        except Exception as e:
            self.logger.warning(f"Primary chart creation failed, using fallback: {str(e)}")
            
            # Try fallback chart type
            try:
                fallback_config = ChartConfig(
                    chart_type=fallback_type,
                    title=f"{config.title} (Simplified)",
                    theme=config.theme,
                    height=config.height
                )
                return self.create_interactive_chart(fallback_type, data, fallback_config, **kwargs)
            except Exception as fallback_error:
                self.logger.error(f"Fallback chart creation also failed: {str(fallback_error)}")
                return self._handle_error(fallback_error, config)
    
    def batch_create_charts(self, chart_specs: List[Dict[str, Any]]) -> List[go.Figure]:
        """Create multiple charts efficiently in batch"""
        figures = []
        
        for spec in chart_specs:
            try:
                chart_type = spec.get('chart_type')
                data = spec.get('data')
                config = spec.get('config')
                kwargs = spec.get('kwargs', {})
                
                fig = self.create_interactive_chart(chart_type, data, config, **kwargs)
                figures.append(fig)
                
            except Exception as e:
                self.logger.error(f"Batch chart creation error: {str(e)}")
                # Add error placeholder
                error_fig = go.Figure()
                error_fig.add_annotation(
                    text=f"Chart Error: {str(e)[:50]}...",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False,
                    font=dict(color=self.theme.error_color)
                )
                figures.append(error_fig)
        
        return figures
    
    def export_chart_config(self, fig: go.Figure) -> Dict[str, Any]:
        """Export chart configuration for reuse or sharing"""
        return {
            'layout': fig.layout.to_dict(),
            'data_structure': [trace.to_dict() for trace in fig.data],
            'theme': {
                'primary_color': self.theme.primary_orange,
                'secondary_color': self.theme.secondary_orange,
                'background': self.theme.dark_background
            }
        }
    
    def apply_custom_theme(self, fig: go.Figure, 
                          custom_colors: Dict[str, str]) -> go.Figure:
        """Apply custom color theme to existing figure"""
        try:
            # Update layout colors
            fig.update_layout(
                paper_bgcolor=custom_colors.get('background', self.theme.dark_background),
                plot_bgcolor=custom_colors.get('plot_background', self.theme.dark_background),
                font_color=custom_colors.get('text', self.theme.text_primary)
            )
            
            # Update trace colors
            primary_color = custom_colors.get('primary', self.theme.primary_orange)
            for i, trace in enumerate(fig.data):
                if hasattr(trace, 'marker'):
                    trace.marker.color = primary_color
                if hasattr(trace, 'line'):
                    trace.line.color = primary_color
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Custom theme application error: {str(e)}")
            return fig


# Utility functions for generating sample data
def generate_hierarchical_data(levels: int = 3, items_per_level: int = 5) -> pd.DataFrame:
    """Generate sample hierarchical data for sunburst/treemap charts"""
    data = []
    
    # Root level
    data.append({"ids": "Total", "parents": "", "values": 1000})
    
    # Generate hierarchical structure
    for level in range(1, levels + 1):
        if level == 1:
            parents = ["Total"]
        else:
            parents = [row["ids"] for row in data if len(row["ids"].split("-")) == level]
        
        for parent in parents:
            for i in range(items_per_level):
                item_id = f"{parent}-L{level}I{i}" if parent != "Total" else f"L{level}I{i}"
                value = np.random.randint(10, 100)
                data.append({"ids": item_id, "parents": parent, "values": value})
    
    return pd.DataFrame(data)


def generate_flow_data(nodes: List[str], num_flows: int = 10) -> pd.DataFrame:
    """Generate sample flow data for Sankey diagrams"""
    data = []
    for _ in range(num_flows):
        source = np.random.choice(nodes[:len(nodes)//2])
        target = np.random.choice(nodes[len(nodes)//2:])
        value = np.random.randint(1, 50)
        data.append({"source": source, "target": target, "value": value})
    
    return pd.DataFrame(data)


def generate_3d_data(n_points: int = 100) -> pd.DataFrame:
    """Generate sample 3D data for scatter plots"""
    return pd.DataFrame({
        'x': np.random.randn(n_points),
        'y': np.random.randn(n_points),
        'z': np.random.randn(n_points),
        'size': np.random.randint(5, 25, n_points),
        'color': np.random.rand(n_points)
    })

