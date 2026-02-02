"""
Brave Design Theme System v2 - Enhanced CSS Theme Management
Modern CSS features with dynamic theming, responsive design, and accessibility.

Features:
- CSS custom properties (CSS variables) for dynamic theming
- Enhanced glass morphism effects with improved backdrop blur
- Responsive design breakpoints for mobile, tablet, and desktop
- Accessibility improvements (WCAG 2.1 AA compliance)
- Preserved Brave Design aesthetic with orange accents and dark background
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import streamlit as st


class ResponsiveBreakpoint(Enum):
    """Responsive design breakpoints"""
    MOBILE = 480
    TABLET = 768
    DESKTOP = 1024
    LARGE = 1440


class ThemeMode(Enum):
    """Theme modes for dynamic switching"""
    DARK = "dark"
    LIGHT = "light"
    AUTO = "auto"


@dataclass
class BraveThemeConfig:
    """Enhanced Brave Design theme configuration"""
    # Core Brave Design Colors (preserved)
    primary_orange: str = "#FF4500"
    secondary_orange: str = "#FF8C00"
    dark_background: str = "#1a1a1a"
    deep_background: str = "#000000"
    panel_background: str = "#0E0E0E"
    
    # Glass morphism colors
    glass_overlay: str = "rgba(20, 20, 20, 0.6)"
    glass_border: str = "rgba(255, 255, 255, 0.08)"
    glass_highlight: str = "rgba(255, 255, 255, 0.05)"
    
    # Text colors
    text_primary: str = "#FFFFFF"
    text_secondary: str = "#888888"
    text_orange: str = "#FF5500"
    
    # Status colors
    success_color: str = "#00FF9D"
    warning_color: str = "#FFD700"
    error_color: str = "#FF0055"
    
    # Enhanced glass morphism settings
    backdrop_blur: int = 12
    backdrop_saturation: float = 1.8
    glass_opacity: float = 0.7
    border_opacity: float = 0.08
    
    # Animation settings
    animation_duration: int = 300
    transition_easing: str = "cubic-bezier(0.4, 0, 0.2, 1)"
    
    # Responsive settings
    mobile_breakpoint: int = 480
    tablet_breakpoint: int = 768
    desktop_breakpoint: int = 1024
    large_breakpoint: int = 1440
    
    # Accessibility settings
    high_contrast: bool = False
    reduced_motion: bool = False
    focus_visible: bool = True
    
    # Theme mode
    mode: ThemeMode = ThemeMode.DARK


class BraveThemeSystem:
    """
    Enhanced Brave Design Theme System with modern CSS features
    """
    
    def __init__(self, config: BraveThemeConfig = None):
        self.config = config or BraveThemeConfig()
        self._css_cache = {}
    
    def generate_css_custom_properties(self) -> str:
        """Generate CSS custom properties (CSS variables) for dynamic theming"""
        return f"""
        :root {{
            /* Core Brave Design Colors */
            --brave-primary-orange: {self.config.primary_orange};
            --brave-secondary-orange: {self.config.secondary_orange};
            --brave-dark-bg: {self.config.dark_background};
            --brave-deep-bg: {self.config.deep_background};
            --brave-panel-bg: {self.config.panel_background};
            
            /* Glass Morphism Properties */
            --brave-glass-overlay: {self.config.glass_overlay};
            --brave-glass-border: {self.config.glass_border};
            --brave-glass-highlight: {self.config.glass_highlight};
            --brave-backdrop-blur: {self.config.backdrop_blur}px;
            --brave-backdrop-saturation: {self.config.backdrop_saturation};
            --brave-glass-opacity: {self.config.glass_opacity};
            --brave-border-opacity: {self.config.border_opacity};
            
            /* Text Colors */
            --brave-text-primary: {self.config.text_primary};
            --brave-text-secondary: {self.config.text_secondary};
            --brave-text-orange: {self.config.text_orange};
            
            /* Status Colors */
            --brave-success: {self.config.success_color};
            --brave-warning: {self.config.warning_color};
            --brave-error: {self.config.error_color};
            
            /* Animation Properties */
            --brave-animation-duration: {self.config.animation_duration}ms;
            --brave-transition-easing: {self.config.transition_easing};
            
            /* Responsive Breakpoints */
            --brave-mobile: {self.config.mobile_breakpoint}px;
            --brave-tablet: {self.config.tablet_breakpoint}px;
            --brave-desktop: {self.config.desktop_breakpoint}px;
            --brave-large: {self.config.large_breakpoint}px;
            
            /* Enhanced Effects */
            --brave-neon-glow: 0 0 10px var(--brave-primary-orange), 0 0 20px var(--brave-primary-orange);
            --brave-card-shadow: 
                0 20px 40px rgba(0,0,0,0.8),
                0 0 0 1px var(--brave-glass-highlight) inset;
            --brave-text-shadow-3d: 
                1px 1px 0px #AA2200, 
                2px 2px 0px #AA2200, 
                3px 3px 0px #AA2200;
            
            /* Border Radius */
            --brave-radius-sm: 8px;
            --brave-radius-md: 16px;
            --brave-radius-lg: 24px;
            --brave-radius-xl: 32px;
        }}
        """
    
    def generate_enhanced_glass_morphism(self) -> str:
        """Generate enhanced glass morphism effects with improved backdrop blur"""
        return f"""
        /* Enhanced Glass Morphism System */
        .brave-glass {{
            background: var(--brave-glass-overlay);
            backdrop-filter: 
                blur(var(--brave-backdrop-blur)) 
                saturate(var(--brave-backdrop-saturation));
            -webkit-backdrop-filter: 
                blur(var(--brave-backdrop-blur)) 
                saturate(var(--brave-backdrop-saturation));
            border: 1px solid var(--brave-glass-border);
            border-radius: var(--brave-radius-md);
            position: relative;
            overflow: hidden;
            transition: all var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        .brave-glass::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(
                90deg, 
                transparent, 
                var(--brave-primary-orange), 
                transparent
            );
            opacity: 0.5;
            transition: opacity var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        .brave-glass:hover {{
            transform: translateY(-2px) scale(1.005);
            border-color: rgba(255, 69, 0, 0.3);
            box-shadow: 
                var(--brave-card-shadow),
                0 0 20px rgba(255, 69, 0, 0.2);
        }}
        
        .brave-glass:hover::before {{
            opacity: 1;
        }}
        
        /* Glass Variants */
        .brave-glass-subtle {{
            background: rgba(20, 20, 20, 0.4);
            backdrop-filter: blur(8px) saturate(1.2);
            -webkit-backdrop-filter: blur(8px) saturate(1.2);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        .brave-glass-intense {{
            background: rgba(20, 20, 20, 0.8);
            backdrop-filter: blur(16px) saturate(2.0);
            -webkit-backdrop-filter: blur(16px) saturate(2.0);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }}
        
        .brave-glass-frosted {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px) saturate(1.5) brightness(1.1);
            -webkit-backdrop-filter: blur(20px) saturate(1.5) brightness(1.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        """
    
    def generate_responsive_design(self) -> str:
        """Generate responsive design breakpoints and layouts"""
        return f"""
        /* Responsive Design System */
        .brave-container {{
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
            transition: padding var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        /* Mobile First Approach */
        @media (max-width: 480px) {{
            .brave-container {{
                padding: 0 0.75rem;
            }}
            
            .brave-glass {{
                margin: 0.5rem 0;
                padding: 1rem;
                border-radius: var(--brave-radius-sm);
            }}
            
            .brave-title {{
                font-size: 2.5rem !important;
                line-height: 1.2;
            }}
            
            .brave-subtitle {{
                font-size: 1rem !important;
            }}
            
            /* Reduce animations on mobile for performance */
            .brave-glass:hover {{
                transform: none;
            }}
        }}
        
        /* Tablet */
        @media (min-width: 481px) and (max-width: 768px) {{
            .brave-container {{
                padding: 0 1rem;
            }}
            
            .brave-glass {{
                margin: 0.75rem 0;
                padding: 1.25rem;
                border-radius: var(--brave-radius-md);
            }}
            
            .brave-title {{
                font-size: 3.5rem !important;
            }}
            
            .brave-subtitle {{
                font-size: 1.1rem !important;
            }}
        }}
        
        /* Desktop */
        @media (min-width: 769px) and (max-width: 1024px) {{
            .brave-container {{
                padding: 0 1.5rem;
            }}
            
            .brave-glass {{
                margin: 1rem 0;
                padding: 1.5rem;
                border-radius: var(--brave-radius-md);
            }}
            
            .brave-title {{
                font-size: 4.5rem !important;
            }}
            
            .brave-subtitle {{
                font-size: 1.2rem !important;
            }}
        }}
        
        /* Large Desktop */
        @media (min-width: 1025px) {{
            .brave-container {{
                padding: 0 2rem;
            }}
            
            .brave-glass {{
                margin: 1.5rem 0;
                padding: 2rem;
                border-radius: var(--brave-radius-lg);
            }}
            
            .brave-title {{
                font-size: 5.5rem !important;
            }}
            
            .brave-subtitle {{
                font-size: 1.2rem !important;
            }}
        }}
        
        /* Responsive Grid System */
        .brave-grid {{
            display: grid;
            gap: 1rem;
            grid-template-columns: 1fr;
        }}
        
        @media (min-width: 481px) {{
            .brave-grid-2 {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (min-width: 769px) {{
            .brave-grid-3 {{
                grid-template-columns: repeat(3, 1fr);
            }}
            
            .brave-grid-4 {{
                grid-template-columns: repeat(4, 1fr);
            }}
        }}
        
        @media (min-width: 1025px) {{
            .brave-grid {{
                gap: 1.5rem;
            }}
        }}
        """
    
    def generate_accessibility_features(self) -> str:
        """Generate accessibility improvements (WCAG 2.1 AA compliance)"""
        high_contrast = "true" if self.config.high_contrast else "false"
        reduced_motion = "true" if self.config.reduced_motion else "false"
        
        return f"""
        /* Accessibility Features */
        
        /* High Contrast Mode */
        @media (prefers-contrast: high), [data-high-contrast="{high_contrast}"] {{
            :root {{
                --brave-text-primary: #FFFFFF;
                --brave-text-secondary: #CCCCCC;
                --brave-glass-border: rgba(255, 255, 255, 0.3);
                --brave-glass-overlay: rgba(0, 0, 0, 0.9);
            }}
            
            .brave-glass {{
                border-width: 2px;
                background: rgba(0, 0, 0, 0.95);
            }}
        }}
        
        /* Reduced Motion */
        @media (prefers-reduced-motion: reduce), [data-reduced-motion="{reduced_motion}"] {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
                scroll-behavior: auto !important;
            }}
            
            .brave-glass:hover {{
                transform: none;
            }}
        }}
        
        /* Focus Visible */
        .brave-focusable:focus-visible {{
            outline: 2px solid var(--brave-primary-orange);
            outline-offset: 2px;
            border-radius: var(--brave-radius-sm);
        }}
        
        /* Screen Reader Only */
        .brave-sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}
        
        /* Skip Links */
        .brave-skip-link {{
            position: absolute;
            top: -40px;
            left: 6px;
            background: var(--brave-primary-orange);
            color: var(--brave-deep-bg);
            padding: 8px;
            text-decoration: none;
            border-radius: var(--brave-radius-sm);
            z-index: 1000;
            transition: top var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        .brave-skip-link:focus {{
            top: 6px;
        }}
        
        /* Enhanced Color Contrast */
        .brave-high-contrast {{
            --brave-text-primary: #FFFFFF;
            --brave-text-secondary: #E0E0E0;
            --brave-glass-overlay: rgba(0, 0, 0, 0.95);
            --brave-glass-border: rgba(255, 255, 255, 0.4);
        }}
        """
    
    def generate_enhanced_components(self) -> str:
        """Generate enhanced component styles with modern CSS features"""
        return f"""
        /* Enhanced Component System */
        
        /* Metallic Typography (Preserved) */
        .brave-title {{
            font-family: 'Rajdhani', sans-serif;
            font-weight: 800;
            text-transform: uppercase;
            background: linear-gradient(
                to bottom,
                var(--brave-text-primary) 0%,
                #CCCCCC 50%,
                #999999 51%,
                var(--brave-text-primary) 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: var(--brave-text-shadow-3d);
            letter-spacing: 0.05em;
            filter: drop-shadow(0 0 5px rgba(255, 69, 0, 0.4));
            transition: filter var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        .brave-subtitle {{
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            background: linear-gradient(90deg, var(--brave-primary-orange), var(--brave-secondary-orange));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0px 0px 10px rgba(255, 69, 0, 0.5);
        }}
        
        /* Enhanced Buttons */
        .brave-button {{
            background: var(--brave-panel-bg);
            border: 1px solid var(--brave-text-secondary);
            color: var(--brave-text-primary);
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            border-radius: var(--brave-radius-sm);
            padding: 0.75rem 1.5rem;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: all var(--brave-animation-duration) var(--brave-transition-easing);
            box-shadow: 0 4px 0 #333;
        }}
        
        .brave-button::before {{
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.1),
                transparent
            );
            transition: left var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        .brave-button:hover {{
            border-color: var(--brave-primary-orange);
            color: var(--brave-primary-orange);
            transform: translateY(-2px);
            box-shadow: 
                0 6px 0 var(--brave-primary-orange), 
                var(--brave-neon-glow);
        }}
        
        .brave-button:hover::before {{
            left: 100%;
        }}
        
        .brave-button:active {{
            transform: translateY(4px);
            box-shadow: 0 0 0 transparent;
        }}
        
        .brave-button-primary {{
            background: var(--brave-primary-orange);
            border-color: var(--brave-primary-orange);
            color: var(--brave-deep-bg);
            box-shadow: 0 4px 0 #cc3700;
        }}
        
        .brave-button-primary:hover {{
            background: var(--brave-secondary-orange);
            color: var(--brave-text-primary);
            box-shadow: 
                0 6px 0 #cc3700, 
                0 0 20px var(--brave-primary-orange);
        }}
        
        /* Enhanced Input Fields */
        .brave-input {{
            background: var(--brave-panel-bg);
            border: 1px solid #333;
            color: var(--brave-text-primary);
            border-radius: var(--brave-radius-sm);
            padding: 0.75rem 1rem;
            font-family: 'Inter', sans-serif;
            transition: all var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        .brave-input:focus {{
            outline: none;
            border-color: var(--brave-primary-orange);
            box-shadow: 0 0 10px rgba(255, 69, 0, 0.3);
            background: rgba(255, 69, 0, 0.05);
        }}
        
        /* Enhanced Metrics */
        .brave-metric {{
            background: var(--brave-glass-overlay);
            backdrop-filter: blur(var(--brave-backdrop-blur));
            -webkit-backdrop-filter: blur(var(--brave-backdrop-blur));
            border: 1px solid var(--brave-glass-border);
            border-radius: var(--brave-radius-md);
            padding: 1.5rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        .brave-metric::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(
                90deg,
                transparent,
                var(--brave-primary-orange),
                transparent
            );
            opacity: 0.5;
        }}
        
        .brave-metric:hover {{
            transform: translateY(-3px);
            border-color: rgba(255, 69, 0, 0.3);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }}
        
        .brave-metric-value {{
            font-family: 'Rajdhani', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1;
            background: linear-gradient(90deg, var(--brave-text-primary), #bbb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0.5rem 0;
        }}
        
        .brave-metric-label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: var(--brave-text-secondary);
            margin-bottom: 0.5rem;
        }}
        
        .brave-metric-delta {{
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }}
        
        .brave-metric-delta.positive {{
            color: var(--brave-success);
        }}
        
        .brave-metric-delta.negative {{
            color: var(--brave-error);
        }}
        
        .brave-metric-delta.neutral {{
            color: var(--brave-text-secondary);
        }}
        """
    
    def generate_streamlit_overrides(self) -> str:
        """Generate Streamlit component overrides with enhanced styling"""
        return f"""
        /* Streamlit Component Overrides */
        
        /* App Background */
        .stApp {{
            background-color: var(--brave-deep-bg);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 69, 0, 0.05) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(255, 140, 0, 0.05) 0%, transparent 20%);
            color: var(--brave-text-primary);
            font-family: 'Inter', sans-serif;
        }}
        
        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: var(--brave-dark-bg);
            border-right: 1px solid var(--brave-glass-border);
        }}
        
        section[data-testid="stSidebar"] .stSelectbox > div > div {{
            background-color: var(--brave-panel-bg);
            border-color: #333;
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Rajdhani', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--brave-text-primary) !important;
        }}
        
        /* Buttons */
        div[data-testid="stButton"] button {{
            background: var(--brave-panel-bg);
            border: 1px solid var(--brave-text-secondary);
            color: var(--brave-text-primary);
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            border-radius: var(--brave-radius-sm);
            transition: all var(--brave-animation-duration) var(--brave-transition-easing);
            box-shadow: 0 4px 0 #333;
            width: 100%;
            margin-top: 4px;
        }}
        
        div[data-testid="stButton"] button:hover {{
            border-color: var(--brave-primary-orange);
            color: var(--brave-primary-orange);
            transform: translateY(-2px);
            box-shadow: 
                0 6px 0 var(--brave-primary-orange), 
                var(--brave-neon-glow);
        }}
        
        div[data-testid="stButton"] button:active {{
            transform: translateY(4px);
            box-shadow: 0 0 0 transparent;
        }}
        
        div[data-testid="stButton"] button[kind="primary"] {{
            background: var(--brave-primary-orange);
            border-color: var(--brave-primary-orange);
            color: var(--brave-deep-bg);
            box-shadow: 0 4px 0 #cc3700;
        }}
        
        div[data-testid="stButton"] button[kind="primary"]:hover {{
            background: var(--brave-secondary-orange);
            color: var(--brave-text-primary);
            box-shadow: 
                0 6px 0 #cc3700, 
                0 0 20px var(--brave-primary-orange);
        }}
        
        /* Input Fields */
        div[data-testid="stTextInput"] input,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        div[data-testid="stTextArea"] textarea {{
            background: var(--brave-panel-bg) !important;
            border: 1px solid #333 !important;
            color: var(--brave-text-primary) !important;
            border-radius: var(--brave-radius-sm) !important;
            transition: all var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stTextArea"] textarea:focus {{
            border-color: var(--brave-primary-orange) !important;
            box-shadow: 0 0 10px rgba(255, 69, 0, 0.3) !important;
            background: rgba(255, 69, 0, 0.05) !important;
        }}
        
        /* Metrics */
        div[data-testid="metric-container"] {{
            background: var(--brave-glass-overlay);
            backdrop-filter: blur(var(--brave-backdrop-blur));
            -webkit-backdrop-filter: blur(var(--brave-backdrop-blur));
            border: 1px solid var(--brave-glass-border);
            border-radius: var(--brave-radius-md);
            padding: 1rem;
            transition: all var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        div[data-testid="metric-container"]:hover {{
            transform: translateY(-2px);
            border-color: rgba(255, 69, 0, 0.3);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        }}
        
        /* Tabs */
        div[data-testid="stTabs"] button {{
            background: transparent !important;
            border: none !important;
            color: var(--brave-text-secondary) !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            transition: all var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        div[data-testid="stTabs"] button[aria-selected="true"] {{
            color: var(--brave-primary-orange) !important;
            border-bottom: 2px solid var(--brave-primary-orange) !important;
        }}
        
        div[data-testid="stTabs"] button:hover {{
            color: var(--brave-primary-orange) !important;
        }}
        
        /* Scrollbars */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--brave-dark-bg);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: #333;
            border-radius: 4px;
            transition: background var(--brave-animation-duration) var(--brave-transition-easing);
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--brave-primary-orange);
        }}
        
        /* Container Borders */
        div[data-testid="stContainer"] {{
            border: 1px solid var(--brave-glass-border);
            border-radius: var(--brave-radius-md);
            background: var(--brave-glass-overlay);
            backdrop-filter: blur(var(--brave-backdrop-blur));
            -webkit-backdrop-filter: blur(var(--brave-backdrop-blur));
        }}
        """
    
    def generate_complete_css(self) -> str:
        """Generate complete enhanced CSS with all modern features"""
        css_parts = [
            "/* Brave Design Theme System v2 - Enhanced CSS */",
            "@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');",
            "",
            self.generate_css_custom_properties(),
            "",
            self.generate_enhanced_glass_morphism(),
            "",
            self.generate_responsive_design(),
            "",
            self.generate_accessibility_features(),
            "",
            self.generate_enhanced_components(),
            "",
            self.generate_streamlit_overrides(),
            "",
            "/* Animation Keyframes */",
            """
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            @keyframes rotateIn {
                from { transform: perspective(1000px) rotateX(10deg); opacity: 0; }
                to { transform: perspective(1000px) rotateX(0); opacity: 1; }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            
            @keyframes glow {
                0%, 100% { box-shadow: 0 0 5px var(--brave-primary-orange); }
                50% { box-shadow: 0 0 20px var(--brave-primary-orange), 0 0 30px var(--brave-primary-orange); }
            }
            
            /* Utility Classes */
            .animate-fade-in { animation: fadeIn 0.8s ease-out forwards; }
            .animate-slide-in { animation: slideIn 0.6s ease-out forwards; }
            .animate-rotate-in { animation: rotateIn 0.8s ease-out forwards; }
            .animate-pulse { animation: pulse 2s infinite; }
            .animate-glow { animation: glow 2s infinite; }
            
            .brave-hidden { display: none !important; }
            .brave-visible { display: block !important; }
            .brave-flex { display: flex !important; }
            .brave-grid { display: grid !important; }
            
            .brave-text-center { text-align: center !important; }
            .brave-text-left { text-align: left !important; }
            .brave-text-right { text-align: right !important; }
            
            .brave-m-0 { margin: 0 !important; }
            .brave-m-1 { margin: 0.5rem !important; }
            .brave-m-2 { margin: 1rem !important; }
            .brave-m-3 { margin: 1.5rem !important; }
            .brave-m-4 { margin: 2rem !important; }
            
            .brave-p-0 { padding: 0 !important; }
            .brave-p-1 { padding: 0.5rem !important; }
            .brave-p-2 { padding: 1rem !important; }
            .brave-p-3 { padding: 1.5rem !important; }
            .brave-p-4 { padding: 2rem !important; }
            """
        ]
        
        return "\n".join(css_parts)
    
    def apply_theme_to_streamlit(self) -> None:
        """Apply the enhanced theme to Streamlit using st.markdown"""
        css = self.generate_complete_css()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    def create_responsive_container(self, content: str, 
                                  glass_variant: str = "default",
                                  animation: str = "fade-in") -> str:
        """Create a responsive container with glass morphism"""
        glass_class = {
            "default": "brave-glass",
            "subtle": "brave-glass brave-glass-subtle",
            "intense": "brave-glass brave-glass-intense",
            "frosted": "brave-glass brave-glass-frosted"
        }.get(glass_variant, "brave-glass")
        
        animation_class = f"animate-{animation}" if animation else ""
        
        return f"""
        <div class="brave-container">
            <div class="{glass_class} {animation_class}">
                {content}
            </div>
        </div>
        """
    
    def create_responsive_grid(self, items: List[str], 
                             columns: int = 3,
                             glass_variant: str = "default") -> str:
        """Create a responsive grid layout"""
        glass_class = {
            "default": "brave-glass",
            "subtle": "brave-glass brave-glass-subtle",
            "intense": "brave-glass brave-glass-intense",
            "frosted": "brave-glass brave-glass-frosted"
        }.get(glass_variant, "brave-glass")
        
        grid_class = f"brave-grid brave-grid-{columns}"
        
        grid_items = "\n".join([
            f'<div class="{glass_class} animate-fade-in">{item}</div>'
            for item in items
        ])
        
        return f"""
        <div class="brave-container">
            <div class="{grid_class}">
                {grid_items}
            </div>
        </div>
        """
    
    def get_theme_config_dict(self) -> Dict[str, Any]:
        """Get theme configuration as dictionary for external use"""
        return {
            "primary_orange": self.config.primary_orange,
            "secondary_orange": self.config.secondary_orange,
            "dark_background": self.config.dark_background,
            "glass_overlay": self.config.glass_overlay,
            "text_primary": self.config.text_primary,
            "text_secondary": self.config.text_secondary,
            "success_color": self.config.success_color,
            "warning_color": self.config.warning_color,
            "error_color": self.config.error_color,
            "backdrop_blur": self.config.backdrop_blur,
            "animation_duration": self.config.animation_duration,
            "responsive_breakpoints": {
                "mobile": self.config.mobile_breakpoint,
                "tablet": self.config.tablet_breakpoint,
                "desktop": self.config.desktop_breakpoint,
                "large": self.config.large_breakpoint
            }
        }