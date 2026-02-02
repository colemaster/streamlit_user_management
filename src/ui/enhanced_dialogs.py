"""
Enhanced Dialog Components for Streamlit Nightly 2026.

Implements enhanced st.dialog with comprehensive icon support including
Material Symbols and emoji for better modal interactions.
"""

import streamlit as st
from typing import Optional, Dict, Any, Callable, List
from enum import Enum


class DialogType(Enum):
    """Dialog types with default icons."""
    CONFIRMATION = "❓"
    WARNING = "⚠️"
    ERROR = "❌"
    SUCCESS = "✅"
    INFO = "ℹ️"
    LOGOUT = "🚪"
    DELETE = "🗑️"
    SAVE = "💾"
    SETTINGS = "⚙️"
    HELP = "❓"


class MaterialSymbols:
    """Material Symbols for enhanced dialog icons."""
    # Navigation
    CLOSE = ":material/close:"
    ARROW_BACK = ":material/arrow_back:"
    ARROW_FORWARD = ":material/arrow_forward:"
    
    # Actions
    DELETE = ":material/delete:"
    EDIT = ":material/edit:"
    SAVE = ":material/save:"
    SETTINGS = ":material/settings:"
    REFRESH = ":material/refresh:"
    
    # Status
    CHECK_CIRCLE = ":material/check_circle:"
    ERROR = ":material/error:"
    WARNING = ":material/warning:"
    INFO = ":material/info:"
    
    # Security
    LOCK = ":material/lock:"
    LOGOUT = ":material/logout:"
    SECURITY = ":material/security:"
    
    # Data
    UPLOAD = ":material/upload:"
    DOWNLOAD = ":material/download:"
    FOLDER = ":material/folder:"
    
    # Communication
    NOTIFICATIONS = ":material/notifications:"
    EMAIL = ":material/email:"
    CHAT = ":material/chat:"


class EnhancedDialogManager:
    """
    Manager for enhanced st.dialog components with comprehensive icon support.
    
    Provides methods to create various types of dialogs with Material Symbols
    and emoji support for better user experience.
    """
    
    @staticmethod
    def confirmation_dialog(
        title: str,
        message: str,
        icon: Optional[str] = None,
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        confirm_type: str = "primary",
        on_confirm: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        session_key: str = "show_confirmation_dialog"
    ) -> None:
        """
        Create a confirmation dialog with enhanced icon support.
        
        Args:
            title: Dialog title
            message: Dialog message content
            icon: Icon to display (emoji or Material Symbol)
            confirm_text: Text for confirm button
            cancel_text: Text for cancel button
            confirm_type: Streamlit button type for confirm button
            on_confirm: Callback function when confirmed
            on_cancel: Callback function when cancelled
            session_key: Session state key for dialog visibility
        """
        if not st.session_state.get(session_key, False):
            return
            
        dialog_icon = icon or DialogType.CONFIRMATION.value
        
        @st.dialog(title, icon=dialog_icon)
        def _show_confirmation():
            st.markdown(f"### {message}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(cancel_text, use_container_width=True):
                    st.session_state[session_key] = False
                    if on_cancel:
                        on_cancel()
                    st.rerun()
            
            with col2:
                if st.button(confirm_text, type=confirm_type, use_container_width=True):
                    st.session_state[session_key] = False
                    if on_confirm:
                        on_confirm()
                    st.rerun()
        
        _show_confirmation()
    
    @staticmethod
    def info_dialog(
        title: str,
        content: str,
        icon: Optional[str] = None,
        session_key: str = "show_info_dialog"
    ) -> None:
        """
        Create an information dialog.
        
        Args:
            title: Dialog title
            content: Information content
            icon: Icon to display
            session_key: Session state key for dialog visibility
        """
        if not st.session_state.get(session_key, False):
            return
            
        dialog_icon = icon or DialogType.INFO.value
        
        @st.dialog(title, icon=dialog_icon)
        def _show_info():
            st.markdown(content)
            
            if st.button("Close", use_container_width=True):
                st.session_state[session_key] = False
                st.rerun()
        
        _show_info()
    
    @staticmethod
    def form_dialog(
        title: str,
        fields: List[Dict[str, Any]],
        icon: Optional[str] = None,
        submit_text: str = "Submit",
        cancel_text: str = "Cancel",
        on_submit: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        session_key: str = "show_form_dialog"
    ) -> None:
        """
        Create a form dialog with multiple input fields.
        
        Args:
            title: Dialog title
            fields: List of field configurations
            icon: Icon to display
            submit_text: Text for submit button
            cancel_text: Text for cancel button
            on_submit: Callback function with form data
            on_cancel: Callback function when cancelled
            session_key: Session state key for dialog visibility
        """
        if not st.session_state.get(session_key, False):
            return
            
        dialog_icon = icon or DialogType.SETTINGS.value
        
        @st.dialog(title, icon=dialog_icon)
        def _show_form():
            form_data = {}
            
            with st.form("dialog_form"):
                for field in fields:
                    field_type = field.get("type", "text")
                    field_key = field["key"]
                    field_label = field["label"]
                    field_default = field.get("default", "")
                    
                    if field_type == "text":
                        form_data[field_key] = st.text_input(field_label, value=field_default)
                    elif field_type == "number":
                        form_data[field_key] = st.number_input(field_label, value=field_default)
                    elif field_type == "select":
                        options = field.get("options", [])
                        form_data[field_key] = st.selectbox(field_label, options, index=0)
                    elif field_type == "checkbox":
                        form_data[field_key] = st.checkbox(field_label, value=field_default)
                    elif field_type == "textarea":
                        form_data[field_key] = st.text_area(field_label, value=field_default)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    cancel_clicked = st.form_submit_button(cancel_text, use_container_width=True)
                
                with col2:
                    submit_clicked = st.form_submit_button(submit_text, type="primary", use_container_width=True)
                
                if cancel_clicked:
                    st.session_state[session_key] = False
                    if on_cancel:
                        on_cancel()
                    st.rerun()
                
                if submit_clicked:
                    st.session_state[session_key] = False
                    if on_submit:
                        on_submit(form_data)
                    st.rerun()
        
        _show_form()
    
    @staticmethod
    def progress_dialog(
        title: str,
        progress_value: float,
        status_text: str = "",
        icon: Optional[str] = None,
        session_key: str = "show_progress_dialog"
    ) -> None:
        """
        Create a progress dialog for long-running operations.
        
        Args:
            title: Dialog title
            progress_value: Progress value (0.0 to 1.0)
            status_text: Current status text
            icon: Icon to display
            session_key: Session state key for dialog visibility
        """
        if not st.session_state.get(session_key, False):
            return
            
        dialog_icon = icon or "⏳"
        
        @st.dialog(title, icon=dialog_icon)
        def _show_progress():
            st.progress(progress_value)
            if status_text:
                st.text(status_text)
            
            # Auto-close when complete
            if progress_value >= 1.0:
                st.success("Operation completed!")
                if st.button("Close", use_container_width=True):
                    st.session_state[session_key] = False
                    st.rerun()
        
        _show_progress()
    
    @staticmethod
    def data_preview_dialog(
        title: str,
        data: Any,
        icon: Optional[str] = None,
        session_key: str = "show_data_preview_dialog"
    ) -> None:
        """
        Create a data preview dialog for displaying data.
        
        Args:
            title: Dialog title
            data: Data to display (DataFrame, dict, etc.)
            icon: Icon to display
            session_key: Session state key for dialog visibility
        """
        if not st.session_state.get(session_key, False):
            return
            
        dialog_icon = icon or MaterialSymbols.FOLDER
        
        @st.dialog(title, icon=dialog_icon)
        def _show_data_preview():
            import pandas as pd
            
            if isinstance(data, pd.DataFrame):
                st.dataframe(data, use_container_width=True)
            elif isinstance(data, dict):
                st.json(data)
            elif isinstance(data, (list, tuple)):
                for i, item in enumerate(data):
                    st.write(f"**Item {i+1}:** {item}")
            else:
                st.write(data)
            
            if st.button("Close", use_container_width=True):
                st.session_state[session_key] = False
                st.rerun()
        
        _show_data_preview()


# Convenience functions for common dialog patterns
def show_confirmation_dialog(
    title: str,
    message: str,
    icon: Optional[str] = None,
    session_key: str = "show_confirmation_dialog"
) -> None:
    """Show a confirmation dialog. Set session_key to True to display."""
    EnhancedDialogManager.confirmation_dialog(
        title=title,
        message=message,
        icon=icon,
        session_key=session_key
    )


def show_info_dialog(
    title: str,
    content: str,
    icon: Optional[str] = None,
    session_key: str = "show_info_dialog"
) -> None:
    """Show an info dialog. Set session_key to True to display."""
    EnhancedDialogManager.info_dialog(
        title=title,
        content=content,
        icon=icon,
        session_key=session_key
    )


def show_delete_confirmation(
    item_name: str,
    on_confirm: Optional[Callable] = None,
    session_key: str = "show_delete_confirmation"
) -> None:
    """Show a delete confirmation dialog."""
    EnhancedDialogManager.confirmation_dialog(
        title="Confirm Deletion",
        message=f"Are you sure you want to delete '{item_name}'? This action cannot be undone.",
        icon=MaterialSymbols.DELETE,
        confirm_text="Delete",
        cancel_text="Cancel",
        confirm_type="primary",
        on_confirm=on_confirm,
        session_key=session_key
    )


def show_save_confirmation(
    on_confirm: Optional[Callable] = None,
    session_key: str = "show_save_confirmation"
) -> None:
    """Show a save confirmation dialog."""
    EnhancedDialogManager.confirmation_dialog(
        title="Save Changes",
        message="Do you want to save your changes?",
        icon=MaterialSymbols.SAVE,
        confirm_text="Save",
        cancel_text="Discard",
        confirm_type="primary",
        on_confirm=on_confirm,
        session_key=session_key
    )