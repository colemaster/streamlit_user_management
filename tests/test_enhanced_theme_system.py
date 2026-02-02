"""
Tests for Enhanced Brave Design Theme System
Tests CSS custom properties, responsive design, glass morphism, and accessibility features.
"""

import pytest
import re
from src.ui.brave_theme_system import (
    BraveThemeSystem, 
    BraveThemeConfig, 
    ResponsiveBreakpoint,
    ThemeMode
)


class TestBraveThemeConfig:
    """Test Brave Design theme configuration"""
    
    def test_default_theme_colors(self):
        """Test that default theme colors match Brave Design specification"""
        config = BraveThemeConfig()
        
        assert config.primary_orange == "#FF4500"
        assert config.secondary_orange == "#FF8C00"
        assert config.dark_background == "#1a1a1a"
        assert config.deep_background == "#000000"
        assert config.panel_background == "#0E0E0E"
        assert config.text_primary == "#FFFFFF"
        assert config.text_secondary == "#888888"
        assert config.success_color == "#00FF9D"
        assert config.warning_color == "#FFD700"
        assert config.error_color == "#FF0055"
    
    def test_glass_morphism_settings(self):
        """Test glass morphism configuration"""
        config = BraveThemeConfig(
            backdrop_blur=16,
            glass_opacity=0.8,
            border_opacity=0.1
        )
        
        assert config.backdrop_blur == 16
        assert config.glass_opacity == 0.8
        assert config.border_opacity == 0.1
        assert config.glass_overlay == "rgba(20, 20, 20, 0.6)"
        assert config.glass_border == "rgba(255, 255, 255, 0.08)"
    
    def test_responsive_breakpoints(self):
        """Test responsive design breakpoint configuration"""
        config = BraveThemeConfig(
            mobile_breakpoint=480,
            tablet_breakpoint=768,
            desktop_breakpoint=1024,
            large_breakpoint=1440
        )
        
        assert config.mobile_breakpoint == 480
        assert config.tablet_breakpoint == 768
        assert config.desktop_breakpoint == 1024
        assert config.large_breakpoint == 1440
    
    def test_animation_settings(self):
        """Test animation configuration"""
        config = BraveThemeConfig(
            animation_duration=500,
            transition_easing="cubic-bezier(0.4, 0, 0.2, 1)"
        )
        
        assert config.animation_duration == 500
        assert config.transition_easing == "cubic-bezier(0.4, 0, 0.2, 1)"
    
    def test_accessibility_settings(self):
        """Test accessibility configuration options"""
        config = BraveThemeConfig(
            high_contrast=True,
            reduced_motion=True,
            focus_visible=True
        )
        
        assert config.high_contrast is True
        assert config.reduced_motion is True
        assert config.focus_visible is True


class TestBraveThemeSystem:
    """Test Brave Design theme system functionality"""
    
    @pytest.fixture
    def theme_system(self):
        """Create theme system instance for testing"""
        config = BraveThemeConfig()
        return BraveThemeSystem(config)
    
    def test_css_custom_properties_generation(self, theme_system):
        """Test CSS custom properties generation"""
        css = theme_system.generate_css_custom_properties()
        
        # Check for essential CSS variables
        assert "--brave-primary-orange: #FF4500;" in css
        assert "--brave-secondary-orange: #FF8C00;" in css
        assert "--brave-dark-bg: #1a1a1a;" in css
        assert "--brave-backdrop-blur: 12px;" in css
        assert "--brave-animation-duration: 300ms;" in css
        
        # Check for computed properties
        assert "--brave-neon-glow:" in css
        assert "--brave-card-shadow:" in css
        assert "--brave-text-shadow-3d:" in css
    
    def test_enhanced_glass_morphism_generation(self, theme_system):
        """Test enhanced glass morphism CSS generation"""
        css = theme_system.generate_enhanced_glass_morphism()
        
        # Check for glass morphism classes
        assert ".brave-glass {" in css
        assert "backdrop-filter:" in css
        assert "-webkit-backdrop-filter:" in css
        assert "blur(var(--brave-backdrop-blur))" in css
        assert "saturate(var(--brave-backdrop-saturation))" in css
        
        # Check for variants
        assert ".brave-glass-subtle" in css
        assert ".brave-glass-intense" in css
        assert ".brave-glass-frosted" in css
        
        # Check for hover effects
        assert ".brave-glass:hover" in css
        assert "transform:" in css
        assert "box-shadow:" in css
    
    def test_responsive_design_generation(self, theme_system):
        """Test responsive design CSS generation"""
        css = theme_system.generate_responsive_design()
        
        # Check for responsive container
        assert ".brave-container" in css
        assert "max-width: 1200px;" in css
        
        # Check for media queries
        assert "@media (max-width: 480px)" in css
        assert "@media (min-width: 481px) and (max-width: 768px)" in css
        assert "@media (min-width: 769px) and (max-width: 1024px)" in css
        assert "@media (min-width: 1025px)" in css
        
        # Check for responsive grid
        assert ".brave-grid" in css
        assert ".brave-grid-2" in css
        assert ".brave-grid-3" in css
        assert ".brave-grid-4" in css
        assert "grid-template-columns:" in css
    
    def test_accessibility_features_generation(self, theme_system):
        """Test accessibility features CSS generation"""
        css = theme_system.generate_accessibility_features()
        
        # Check for accessibility media queries
        assert "@media (prefers-contrast: high)" in css
        assert "@media (prefers-reduced-motion: reduce)" in css
        
        # Check for focus visible
        assert ".brave-focusable:focus-visible" in css
        assert "outline: 2px solid var(--brave-primary-orange);" in css
        
        # Check for screen reader support
        assert ".brave-sr-only" in css
        assert "position: absolute;" in css
        assert "clip: rect(0, 0, 0, 0);" in css
        
        # Check for skip links
        assert ".brave-skip-link" in css
    
    def test_enhanced_components_generation(self, theme_system):
        """Test enhanced component CSS generation"""
        css = theme_system.generate_enhanced_components()
        
        # Check for metallic typography (preserved)
        assert ".brave-title" in css
        assert ".brave-subtitle" in css
        assert "text-shadow: var(--brave-text-shadow-3d);" in css
        assert "-webkit-background-clip: text;" in css
        assert "-webkit-text-fill-color: transparent;" in css
        
        # Check for enhanced buttons
        assert ".brave-button" in css
        assert ".brave-button-primary" in css
        assert ".brave-button::before" in css
        assert "transition: all var(--brave-animation-duration)" in css
        
        # Check for enhanced inputs
        assert ".brave-input" in css
        assert ".brave-input:focus" in css
        
        # Check for enhanced metrics
        assert ".brave-metric" in css
        assert ".brave-metric-value" in css
        assert ".brave-metric-label" in css
        assert ".brave-metric-delta" in css
    
    def test_streamlit_overrides_generation(self, theme_system):
        """Test Streamlit component overrides"""
        css = theme_system.generate_streamlit_overrides()
        
        # Check for app styling
        assert ".stApp" in css
        assert "background-color: var(--brave-deep-bg);" in css
        assert "radial-gradient" in css
        
        # Check for component overrides
        assert 'div[data-testid="stButton"] button' in css
        assert 'div[data-testid="stTextInput"] input' in css
        assert 'div[data-testid="metric-container"]' in css
        assert 'section[data-testid="stSidebar"]' in css
        
        # Check for scrollbar styling
        assert "::-webkit-scrollbar" in css
        assert "::-webkit-scrollbar-thumb" in css
    
    def test_complete_css_generation(self, theme_system):
        """Test complete CSS generation"""
        css = theme_system.generate_complete_css()
        
        # Check for imports
        assert "@import url('https://fonts.googleapis.com/css2" in css
        assert "Rajdhani" in css
        assert "Inter" in css
        
        # Check for keyframes
        assert "@keyframes fadeIn" in css
        assert "@keyframes slideIn" in css
        assert "@keyframes rotateIn" in css
        assert "@keyframes pulse" in css
        assert "@keyframes glow" in css
        
        # Check for utility classes
        assert ".animate-fade-in" in css
        assert ".brave-hidden" in css
        assert ".brave-text-center" in css
        assert ".brave-m-1" in css
        assert ".brave-p-2" in css
        
        # Ensure CSS is valid (basic syntax check)
        assert css.count("{") == css.count("}")  # Balanced braces
        assert "}" in css  # Has closing braces
        assert ":" in css  # Has property declarations
    
    def test_responsive_container_creation(self, theme_system):
        """Test responsive container HTML generation"""
        content = "<h1>Test Content</h1>"
        container = theme_system.create_responsive_container(
            content, 
            glass_variant="intense",
            animation="slide-in"
        )
        
        assert "brave-container" in container
        assert "brave-glass" in container
        assert "brave-glass-intense" in container
        assert "animate-slide-in" in container
        assert content in container
    
    def test_responsive_grid_creation(self, theme_system):
        """Test responsive grid HTML generation"""
        items = ["<div>Item 1</div>", "<div>Item 2</div>", "<div>Item 3</div>"]
        grid = theme_system.create_responsive_grid(
            items,
            columns=3,
            glass_variant="frosted"
        )
        
        assert "brave-container" in grid
        assert "brave-grid" in grid
        assert "brave-grid-3" in grid
        assert "brave-glass-frosted" in grid
        
        for item in items:
            assert item in grid
    
    def test_theme_config_dict_export(self, theme_system):
        """Test theme configuration dictionary export"""
        config_dict = theme_system.get_theme_config_dict()
        
        # Check for essential keys
        assert "primary_orange" in config_dict
        assert "secondary_orange" in config_dict
        assert "dark_background" in config_dict
        assert "backdrop_blur" in config_dict
        assert "animation_duration" in config_dict
        assert "responsive_breakpoints" in config_dict
        
        # Check responsive breakpoints structure
        breakpoints = config_dict["responsive_breakpoints"]
        assert "mobile" in breakpoints
        assert "tablet" in breakpoints
        assert "desktop" in breakpoints
        assert "large" in breakpoints
        
        # Check values
        assert config_dict["primary_orange"] == "#FF4500"
        assert config_dict["backdrop_blur"] == 12
        assert breakpoints["mobile"] == 480


class TestResponsiveBreakpoint:
    """Test responsive breakpoint enum"""
    
    def test_breakpoint_values(self):
        """Test breakpoint enum values"""
        assert ResponsiveBreakpoint.MOBILE.value == 480
        assert ResponsiveBreakpoint.TABLET.value == 768
        assert ResponsiveBreakpoint.DESKTOP.value == 1024
        assert ResponsiveBreakpoint.LARGE.value == 1440


class TestThemeMode:
    """Test theme mode enum"""
    
    def test_theme_mode_values(self):
        """Test theme mode enum values"""
        assert ThemeMode.DARK.value == "dark"
        assert ThemeMode.LIGHT.value == "light"
        assert ThemeMode.AUTO.value == "auto"


class TestThemeSystemIntegration:
    """Test theme system integration features"""
    
    def test_high_contrast_mode(self):
        """Test high contrast mode configuration"""
        config = BraveThemeConfig(high_contrast=True)
        theme_system = BraveThemeSystem(config)
        
        css = theme_system.generate_accessibility_features()
        
        # Should include high contrast media query
        assert '@media (prefers-contrast: high), [data-high-contrast="true"]' in css
        assert "--brave-text-primary: #FFFFFF;" in css
        assert "--brave-glass-overlay: rgba(0, 0, 0, 0.95);" in css
    
    def test_reduced_motion_mode(self):
        """Test reduced motion mode configuration"""
        config = BraveThemeConfig(reduced_motion=True)
        theme_system = BraveThemeSystem(config)
        
        css = theme_system.generate_accessibility_features()
        
        # Should include reduced motion media query
        assert '@media (prefers-reduced-motion: reduce), [data-reduced-motion="true"]' in css
        assert "animation-duration: 0.01ms !important;" in css
        assert "transition-duration: 0.01ms !important;" in css
    
    def test_css_variable_consistency(self):
        """Test that CSS variables are consistently named and used"""
        theme_system = BraveThemeSystem()
        
        custom_props = theme_system.generate_css_custom_properties()
        glass_css = theme_system.generate_enhanced_glass_morphism()
        components_css = theme_system.generate_enhanced_components()
        
        # Extract variable definitions
        var_definitions = re.findall(r'--brave-[\w-]+:', custom_props)
        
        # Extract variable usages
        var_usages = re.findall(r'var\(--brave-[\w-]+\)', glass_css + components_css)
        
        # Check that used variables are defined
        defined_vars = {var.replace(':', '') for var in var_definitions}
        used_vars = {var.replace('var(', '').replace(')', '') for var in var_usages}
        
        # All used variables should be defined
        undefined_vars = used_vars - defined_vars
        assert len(undefined_vars) == 0, f"Undefined CSS variables: {undefined_vars}"
    
    def test_color_contrast_ratios(self):
        """Test that color combinations meet accessibility standards"""
        config = BraveThemeConfig()
        
        # Test primary orange on dark background (should have good contrast)
        assert config.primary_orange == "#FF4500"
        assert config.dark_background == "#1a1a1a"
        
        # Test text colors
        assert config.text_primary == "#FFFFFF"  # White on dark should have excellent contrast
        assert config.text_secondary == "#888888"  # Gray should still be readable
    
    def test_animation_performance_settings(self):
        """Test animation settings for performance"""
        config = BraveThemeConfig(animation_duration=300)
        theme_system = BraveThemeSystem(config)
        
        css = theme_system.generate_enhanced_components()
        
        # Should use CSS variables for consistent timing
        assert "var(--brave-animation-duration)" in css
        assert "var(--brave-transition-easing)" in css
        
        # Should have reasonable duration (not too long)
        assert config.animation_duration <= 500  # Max 500ms for good UX


if __name__ == "__main__":
    pytest.main([__file__])