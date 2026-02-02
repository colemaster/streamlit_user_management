"""
Dialog Showcase Component - Demonstrates Enhanced st.dialog Features.

This component showcases the various enhanced dialog types with Material Symbols
and emoji support for testing and demonstration purposes.
"""

import streamlit as st
import pandas as pd
from src.ui.enhanced_dialogs import (
    EnhancedDialogManager,
    MaterialSymbols,
    DialogType,
    show_confirmation_dialog,
    show_info_dialog,
    show_delete_confirmation,
    show_save_confirmation
)


def render_dialog_showcase():
    """Render the dialog showcase component."""
    st.markdown("## 🎭 Enhanced Dialog Showcase")
    st.markdown("Test the new Streamlit nightly dialog features with Material Symbols and emoji support.")
    
    # Basic Dialog Examples
    st.markdown("### Basic Dialogs")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Info Dialog", use_container_width=True):
            st.session_state["show_info_demo"] = True
    
    with col2:
        if st.button("❓ Confirmation Dialog", use_container_width=True):
            st.session_state["show_confirmation_demo"] = True
    
    with col3:
        if st.button("⚠️ Warning Dialog", use_container_width=True):
            st.session_state["show_warning_demo"] = True
    
    # Material Symbols Examples
    st.markdown("### Material Symbols Dialogs")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Delete Confirmation", use_container_width=True):
            st.session_state["show_delete_demo"] = True
    
    with col2:
        if st.button("💾 Save Dialog", use_container_width=True):
            st.session_state["show_save_demo"] = True
    
    with col3:
        if st.button("⚙️ Settings Form", use_container_width=True):
            st.session_state["show_form_demo"] = True
    
    # Advanced Dialog Examples
    st.markdown("### Advanced Dialogs")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Data Preview", use_container_width=True):
            st.session_state["show_data_demo"] = True
    
    with col2:
        if st.button("⏳ Progress Dialog", use_container_width=True):
            st.session_state["show_progress_demo"] = True
            st.session_state["progress_value"] = 0.0
    
    with col3:
        if st.button("🔐 Security Dialog", use_container_width=True):
            st.session_state["show_security_demo"] = True
    
    # Handle dialog displays
    _handle_dialog_displays()


def _handle_dialog_displays():
    """Handle all dialog display logic."""
    
    # Info Dialog Demo
    EnhancedDialogManager.info_dialog(
        title="Information",
        content="""
        ### Welcome to Enhanced Dialogs! 🎉
        
        This is an example of an **information dialog** with:
        - Markdown support
        - Emoji icons
        - Clean, modern styling
        
        The new Streamlit nightly features make dialogs more interactive and visually appealing.
        """,
        icon="ℹ️",
        session_key="show_info_demo"
    )
    
    # Confirmation Dialog Demo
    def on_confirm():
        st.toast("Action confirmed! ✅", icon="✅")
    
    def on_cancel():
        st.toast("Action cancelled.", icon="❌")
    
    EnhancedDialogManager.confirmation_dialog(
        title="Confirm Action",
        message="Do you want to proceed with this action?",
        icon="❓",
        confirm_text="Yes, Proceed",
        cancel_text="Cancel",
        on_confirm=on_confirm,
        on_cancel=on_cancel,
        session_key="show_confirmation_demo"
    )
    
    # Warning Dialog Demo
    EnhancedDialogManager.info_dialog(
        title="Warning",
        content="""
        ⚠️ **Important Warning**
        
        This is a warning dialog example. It uses the warning emoji and 
        provides important information that requires user attention.
        
        - Check system status
        - Verify configurations
        - Ensure data backup
        """,
        icon="⚠️",
        session_key="show_warning_demo"
    )
    
    # Delete Confirmation Demo
    def on_delete_confirm():
        st.toast("Item deleted successfully! 🗑️", icon="✅")
    
    show_delete_confirmation(
        item_name="Sample Data File",
        on_confirm=on_delete_confirm,
        session_key="show_delete_demo"
    )
    
    # Save Confirmation Demo
    def on_save_confirm():
        st.toast("Changes saved successfully! 💾", icon="✅")
    
    show_save_confirmation(
        on_confirm=on_save_confirm,
        session_key="show_save_demo"
    )
    
    # Form Dialog Demo
    form_fields = [
        {"key": "name", "label": "Name", "type": "text", "default": ""},
        {"key": "email", "label": "Email", "type": "text", "default": ""},
        {"key": "role", "label": "Role", "type": "select", "options": ["Admin", "User", "Viewer"]},
        {"key": "notifications", "label": "Enable Notifications", "type": "checkbox", "default": True},
        {"key": "notes", "label": "Notes", "type": "textarea", "default": ""}
    ]
    
    def on_form_submit(data):
        st.toast(f"Form submitted for {data['name']}! 📝", icon="✅")
        st.session_state["form_data"] = data
    
    EnhancedDialogManager.form_dialog(
        title="User Settings",
        fields=form_fields,
        icon=MaterialSymbols.SETTINGS,
        submit_text="Save Settings",
        on_submit=on_form_submit,
        session_key="show_form_demo"
    )
    
    # Data Preview Dialog Demo
    sample_data = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'Age': [25, 30, 35, 28],
        'Department': ['Engineering', 'Marketing', 'Sales', 'HR'],
        'Salary': [75000, 65000, 70000, 60000]
    })
    
    EnhancedDialogManager.data_preview_dialog(
        title="Employee Data Preview",
        data=sample_data,
        icon=MaterialSymbols.FOLDER,
        session_key="show_data_demo"
    )
    
    # Progress Dialog Demo
    if st.session_state.get("show_progress_demo", False):
        progress_value = st.session_state.get("progress_value", 0.0)
        
        # Simulate progress
        if progress_value < 1.0:
            progress_value += 0.1
            st.session_state["progress_value"] = progress_value
            st.rerun()
        
        status_messages = [
            "Initializing...",
            "Loading data...",
            "Processing records...",
            "Validating results...",
            "Generating reports...",
            "Finalizing...",
            "Complete!"
        ]
        
        status_index = min(int(progress_value * len(status_messages)), len(status_messages) - 1)
        status_text = status_messages[status_index]
        
        EnhancedDialogManager.progress_dialog(
            title="Processing Data",
            progress_value=progress_value,
            status_text=status_text,
            icon="⏳",
            session_key="show_progress_demo"
        )
    
    # Security Dialog Demo
    EnhancedDialogManager.info_dialog(
        title="Security Notice",
        content="""
        🔐 **Security Information**
        
        Your session is protected with:
        - Multi-factor authentication
        - End-to-end encryption
        - Session timeout protection
        - Audit logging
        
        **Session Details:**
        - Login time: 2026-01-31 10:30 AM
        - IP Address: 192.168.1.100
        - Device: Chrome on Windows
        - Location: San Francisco, CA
        """,
        icon=MaterialSymbols.SECURITY,
        session_key="show_security_demo"
    )
    
    # Display form data if available
    if "form_data" in st.session_state:
        st.markdown("### Last Form Submission")
        st.json(st.session_state["form_data"])


# Integration function for existing components
def add_dialog_examples_to_component(component_name: str):
    """Add dialog examples to existing UI components."""
    
    if component_name == "admin":
        # Add to admin dashboard
        st.markdown("### Dialog Examples")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh Tokens", use_container_width=True):
                st.session_state["show_token_refresh_dialog"] = True
        
        with col2:
            if st.button("🗑️ Clear Cache", use_container_width=True):
                st.session_state["show_cache_clear_dialog"] = True
        
        # Token refresh dialog
        def on_token_refresh():
            st.toast("Tokens refreshed successfully! 🔄", icon="✅")
        
        EnhancedDialogManager.confirmation_dialog(
            title="Refresh Access Tokens",
            message="This will refresh your access tokens and may require re-authentication.",
            icon=MaterialSymbols.REFRESH,
            confirm_text="Refresh",
            on_confirm=on_token_refresh,
            session_key="show_token_refresh_dialog"
        )
        
        # Cache clear dialog
        def on_cache_clear():
            st.toast("Cache cleared successfully! 🗑️", icon="✅")
        
        EnhancedDialogManager.confirmation_dialog(
            title="Clear Application Cache",
            message="This will clear all cached data and may slow down the next page load.",
            icon=MaterialSymbols.DELETE,
            confirm_text="Clear Cache",
            on_confirm=on_cache_clear,
            session_key="show_cache_clear_dialog"
        )