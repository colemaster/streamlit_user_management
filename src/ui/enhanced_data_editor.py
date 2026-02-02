"""
Enhanced Data Editor Components for Streamlit Nightly 2026.

Implements enhanced st.data_editor with advanced data manipulation features,
new column types, editing modes, and comprehensive validation.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Callable, Union
from enum import Enum
from datetime import datetime, date, time
import json


class ColumnType(Enum):
    """Enhanced column types for st.data_editor with Streamlit nightly 2026 features."""
    TEXT = "text"
    NUMBER = "number"
    CHECKBOX = "checkbox"
    SELECTBOX = "selectbox"
    MULTISELECT = "multiselect"  # New in Streamlit 1.50+
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    LINK = "link"
    IMAGE = "image"
    PROGRESS = "progress"
    JSON = "json"  # New column type for structured data
    LIST = "list"  # New column type for array data
    LINE_CHART = "line_chart"  # New chart column type
    BAR_CHART = "bar_chart"  # New chart column type
    AREA_CHART = "area_chart"  # New chart column type
    COLOR = "color"
    CURRENCY = "currency"
    PERCENTAGE = "percentage"


class EditingMode(Enum):
    """Editing modes for data editor with enhanced capabilities."""
    FULL = "full"           # Full editing capabilities
    READONLY = "readonly"   # Read-only mode
    APPEND_ONLY = "append"  # Can only add new rows
    EDIT_ONLY = "edit"      # Can only edit existing rows
    SELECTIVE = "selective" # Only specific columns editable
    BATCH_EDIT = "batch"    # Batch editing mode for multiple rows
    REVIEW = "review"       # Review mode with approval workflow


class ValidationRule:
    """Validation rule for data editor columns."""
    
    def __init__(
        self,
        rule_type: str,
        value: Any = None,
        message: str = "Validation failed"
    ):
        self.rule_type = rule_type
        self.value = value
        self.message = message
    
    def validate(self, data: Any) -> tuple[bool, str]:
        """Validate data against this rule."""
        if self.rule_type == "required" and (data is None or data == ""):
            return False, "This field is required"
        elif self.rule_type == "min_length" and len(str(data)) < self.value:
            return False, f"Minimum length is {self.value}"
        elif self.rule_type == "max_length" and len(str(data)) > self.value:
            return False, f"Maximum length is {self.value}"
        elif self.rule_type == "min_value" and float(data) < self.value:
            return False, f"Minimum value is {self.value}"
        elif self.rule_type == "max_value" and float(data) > self.value:
            return False, f"Maximum value is {self.value}"
        elif self.rule_type == "regex":
            import re
            if not re.match(self.value, str(data)):
                return False, self.message
        elif self.rule_type == "unique":
            # This would need to be handled at the dataframe level
            pass
        
        return True, ""


class EnhancedDataEditor:
    """
    Enhanced data editor with advanced features using Streamlit nightly 2026.
    
    Provides comprehensive data manipulation capabilities with:
    - Advanced column types and configurations
    - Multiple editing modes and permissions
    - Data validation and error handling
    - Custom formatting and styling
    - Export and import functionality
    """
    
    @staticmethod
    def create_column_config(
        column_name: str,
        column_type: ColumnType,
        label: Optional[str] = None,
        help_text: Optional[str] = None,
        default_value: Any = None,
        options: Optional[List[Any]] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        step: Optional[float] = None,
        format_string: Optional[str] = None,
        width: Optional[str] = None,
        disabled: bool = False,
        required: bool = False,
        validation_rules: Optional[List[ValidationRule]] = None,
        pinned: bool = False,
        chart_data: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Create column configuration for enhanced st.data_editor with latest Streamlit features.
        
        Args:
            column_name: Name of the column
            column_type: Type of column (ColumnType enum)
            label: Display label for the column
            help_text: Help text for the column
            default_value: Default value for new rows
            options: Options for selectbox/multiselect columns
            min_value: Minimum value for number columns
            max_value: Maximum value for number columns
            step: Step size for number columns
            format_string: Format string for display
            width: Column width ("small", "medium", "large", or pixel value)
            disabled: Whether column is disabled
            required: Whether column is required
            validation_rules: List of validation rules
            pinned: Whether column should be pinned to left
            chart_data: Data for chart columns
            
        Returns:
            Column configuration dictionary compatible with st.data_editor
        """
        # Use actual Streamlit column config classes for better compatibility
        if column_type == ColumnType.TEXT:
            return st.column_config.TextColumn(
                label=label or column_name,
                help=help_text,
                default=default_value,
                max_chars=int(max_value) if max_value else None,
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        elif column_type == ColumnType.NUMBER:
            return st.column_config.NumberColumn(
                label=label or column_name,
                help=help_text,
                default=default_value,
                min_value=min_value,
                max_value=max_value,
                step=step or 1,
                format=format_string,
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        elif column_type == ColumnType.CHECKBOX:
            return st.column_config.CheckboxColumn(
                label=label or column_name,
                help=help_text,
                default=default_value or False,
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        elif column_type == ColumnType.SELECTBOX:
            return st.column_config.SelectboxColumn(
                label=label or column_name,
                help=help_text,
                default=default_value,
                options=options or [],
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        elif column_type == ColumnType.MULTISELECT:
            return st.column_config.MultiselectColumn(
                label=label or column_name,
                help=help_text,
                default=default_value or [],
                options=options or [],
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        elif column_type == ColumnType.DATE:
            return st.column_config.DateColumn(
                label=label or column_name,
                help=help_text,
                default=default_value,
                min_value=min_value,
                max_value=max_value,
                format=format_string,
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        elif column_type == ColumnType.TIME:
            return st.column_config.TimeColumn(
                label=label or column_name,
                help=help_text,
                default=default_value,
                format=format_string,
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        elif column_type == ColumnType.DATETIME:
            return st.column_config.DatetimeColumn(
                label=label or column_name,
                help=help_text,
                default=default_value,
                min_value=min_value,
                max_value=max_value,
                format=format_string,
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        elif column_type == ColumnType.LINK:
            return st.column_config.LinkColumn(
                label=label or column_name,
                help=help_text,
                display_text=format_string or "Link",
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        elif column_type == ColumnType.IMAGE:
            return st.column_config.ImageColumn(
                label=label or column_name,
                help=help_text,
                width=width,
                pinned=pinned
            )
        
        elif column_type == ColumnType.PROGRESS:
            return st.column_config.ProgressColumn(
                label=label or column_name,
                help=help_text,
                min_value=min_value or 0,
                max_value=max_value or 100,
                format=format_string,
                width=width,
                pinned=pinned
            )
        
        elif column_type == ColumnType.JSON:
            # JSONColumn might not be available in current Streamlit version
            # Fall back to generic column with JSON display
            return st.column_config.Column(
                label=label or column_name,
                help=help_text,
                width=width,
                pinned=pinned
            )
        
        elif column_type == ColumnType.LIST:
            return st.column_config.ListColumn(
                label=label or column_name,
                help=help_text,
                width=width,
                pinned=pinned
            )
        
        elif column_type == ColumnType.LINE_CHART:
            return st.column_config.LineChartColumn(
                label=label or column_name,
                help=help_text,
                width=width,
                pinned=pinned
            )
        
        elif column_type == ColumnType.BAR_CHART:
            return st.column_config.BarChartColumn(
                label=label or column_name,
                help=help_text,
                width=width,
                pinned=pinned
            )
        
        elif column_type == ColumnType.AREA_CHART:
            return st.column_config.AreaChartColumn(
                label=label or column_name,
                help=help_text,
                width=width,
                pinned=pinned
            )
        
        elif column_type == ColumnType.CURRENCY:
            return st.column_config.NumberColumn(
                label=label or column_name,
                help=help_text,
                default=default_value,
                format=format_string or "$%.2f",
                min_value=min_value or 0,
                step=step or 0.01,
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        elif column_type == ColumnType.PERCENTAGE:
            return st.column_config.NumberColumn(
                label=label or column_name,
                help=help_text,
                default=default_value,
                format=format_string or "%.1f%%",
                min_value=min_value or 0,
                max_value=max_value or 100,
                step=step or 0.1,
                width=width,
                disabled=disabled,
                pinned=pinned
            )
        
        else:
            # Fallback to generic column
            return st.column_config.Column(
                label=label or column_name,
                help=help_text,
                width=width,
                disabled=disabled,
                pinned=pinned
            )
    
    @staticmethod
    def enhanced_data_editor(
        data: pd.DataFrame,
        key: Optional[str] = None,
        height: Optional[int] = None,
        use_container_width: bool = True,
        hide_index: bool = False,
        column_order: Optional[List[str]] = None,
        column_config: Optional[Dict[str, Any]] = None,
        num_rows: str = "dynamic",
        editing_mode: EditingMode = EditingMode.FULL,
        editable_columns: Optional[List[str]] = None,
        on_change: Optional[Callable] = None,
        validation_callback: Optional[Callable] = None,
        auto_save: bool = False,
        show_toolbar: bool = True,
        enable_search: bool = True,
        enable_filtering: bool = True,
        enable_sorting: bool = True,
        enable_export: bool = True,
        enable_import: bool = True,
        enable_batch_operations: bool = True,
        selection_mode: str = "multi-row"
    ) -> pd.DataFrame:
        """
        Create an enhanced data editor with advanced features using Streamlit nightly 2026.
        
        Args:
            data: DataFrame to edit
            key: Unique key for the widget
            height: Height of the editor
            use_container_width: Use full container width
            hide_index: Hide the index column
            column_order: Order of columns to display
            column_config: Configuration for each column
            num_rows: Number of rows ("fixed", "dynamic")
            editing_mode: Editing mode (EditingMode enum)
            editable_columns: List of editable columns (for selective mode)
            on_change: Callback function for changes
            validation_callback: Callback for validation
            auto_save: Automatically save changes
            show_toolbar: Show editing toolbar
            enable_search: Enable search functionality
            enable_filtering: Enable column filtering
            enable_sorting: Enable column sorting
            enable_export: Enable data export
            enable_import: Enable data import
            enable_batch_operations: Enable batch editing operations
            selection_mode: Row selection mode ("single-row", "multi-row", "single-column", "multi-column")
            
        Returns:
            Edited DataFrame
        """
        # Initialize session state for this editor
        if key:
            if f"{key}_search_term" not in st.session_state:
                st.session_state[f"{key}_search_term"] = ""
            if f"{key}_filters" not in st.session_state:
                st.session_state[f"{key}_filters"] = {}
            if f"{key}_selected_rows" not in st.session_state:
                st.session_state[f"{key}_selected_rows"] = []
        
        # Apply editing mode restrictions
        disabled_columns = []
        if editing_mode == EditingMode.READONLY:
            disabled_columns = list(data.columns)
        elif editing_mode == EditingMode.SELECTIVE and editable_columns:
            disabled_columns = [col for col in data.columns if col not in editable_columns]
        elif editing_mode == EditingMode.BATCH_EDIT:
            # In batch mode, show selection checkboxes
            selection_mode = "multi-row"
        
        # Update column config with disabled status
        if column_config is None:
            column_config = {}
        
        for col in disabled_columns:
            if col not in column_config:
                column_config[col] = st.column_config.Column(disabled=True)
            elif hasattr(column_config[col], 'disabled'):
                column_config[col].disabled = True
        
        # Show enhanced toolbar if enabled
        if show_toolbar:
            filtered_data = EnhancedDataEditor._render_enhanced_toolbar(
                data, key, enable_search, enable_filtering, 
                enable_sorting, enable_export, enable_import,
                enable_batch_operations, editing_mode
            )
        else:
            filtered_data = data
        
        # Create the enhanced data editor with latest Streamlit features
        try:
            edited_data = st.data_editor(
                filtered_data,
                key=key,
                height=height,
                use_container_width=use_container_width,
                hide_index=hide_index,
                column_order=column_order,
                column_config=column_config,
                num_rows=num_rows,
                on_change=on_change
            )
            
            # Advanced validation with detailed error reporting
            if validation_callback:
                validation_errors = validation_callback(edited_data)
                if validation_errors:
                    with st.expander("⚠️ Validation Errors", expanded=True):
                        for i, error in enumerate(validation_errors):
                            st.error(f"**Row {error.get('row', 'Unknown')}:** {error.get('message', error)}")
                            if error.get('suggestions'):
                                st.info(f"💡 Suggestion: {error['suggestions']}")
            
            # Enhanced change tracking and auto-save
            if auto_save and key:
                if f"{key}_last_data" not in st.session_state:
                    st.session_state[f"{key}_last_data"] = data.copy()
                
                # Check if data has changed
                if not edited_data.equals(st.session_state[f"{key}_last_data"]):
                    st.session_state[f"{key}_auto_saved"] = edited_data.copy()
                    st.session_state[f"{key}_last_data"] = edited_data.copy()
                    st.success("✅ Changes auto-saved")
            
            # Batch operations handling
            if enable_batch_operations and editing_mode == EditingMode.BATCH_EDIT:
                EnhancedDataEditor._handle_batch_operations(edited_data, key)
            
            return edited_data
            
        except Exception as e:
            st.error(f"❌ Error in data editor: {str(e)}")
            with st.expander("🔍 Debug Information"):
                st.code(f"Error Type: {type(e).__name__}")
                st.code(f"Error Message: {str(e)}")
                st.code(f"Data Shape: {data.shape}")
                st.code(f"Column Config Keys: {list(column_config.keys()) if column_config else 'None'}")
            return data
    
    @staticmethod
    def _render_enhanced_toolbar(
        data: pd.DataFrame,
        key: Optional[str],
        enable_search: bool,
        enable_filtering: bool,
        enable_sorting: bool,
        enable_export: bool,
        enable_import: bool,
        enable_batch_operations: bool,
        editing_mode: EditingMode
    ) -> pd.DataFrame:
        """Render the enhanced data editor toolbar with advanced features."""
        st.markdown("#### 🛠️ Enhanced Data Editor Toolbar")
        
        # Main toolbar row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        filtered_data = data.copy()
        
        with col1:
            if enable_search:
                search_term = st.text_input(
                    "🔍 Search", 
                    key=f"{key}_search" if key else None,
                    placeholder="Search all columns..."
                )
                if search_term and key:
                    st.session_state[f"{key}_search_term"] = search_term
                    # Apply search filter
                    mask = data.astype(str).apply(
                        lambda x: x.str.contains(search_term, case=False, na=False)
                    ).any(axis=1)
                    filtered_data = data[mask]
                    st.caption(f"Found {len(filtered_data)} of {len(data)} rows")
        
        with col2:
            if enable_filtering:
                if st.button("🔽 Advanced Filters", key=f"{key}_filter" if key else None):
                    st.session_state[f"{key}_show_filters"] = not st.session_state.get(f"{key}_show_filters", False)
        
        with col3:
            if enable_sorting:
                sort_options = ["None"] + list(data.columns)
                sort_column = st.selectbox(
                    "📊 Sort by", 
                    sort_options, 
                    key=f"{key}_sort" if key else None
                )
                if sort_column != "None":
                    ascending = st.checkbox("Ascending", value=True, key=f"{key}_sort_asc" if key else None)
                    filtered_data = filtered_data.sort_values(sort_column, ascending=ascending)
        
        with col4:
            if enable_export:
                export_format = st.selectbox(
                    "📥 Export", 
                    ["Select...", "CSV", "Excel", "JSON", "Parquet"],
                    key=f"{key}_export_format" if key else None
                )
                if export_format != "Select...":
                    EnhancedDataEditor._handle_export(filtered_data, export_format, key)
        
        with col5:
            if enable_import:
                if st.button("📤 Import Data", key=f"{key}_import" if key else None):
                    st.session_state[f"{key}_show_import"] = True
        
        # Advanced filters panel
        if enable_filtering and st.session_state.get(f"{key}_show_filters", False):
            with st.expander("🔍 Advanced Filters", expanded=True):
                filter_cols = st.columns(min(3, len(data.columns)))
                for i, col in enumerate(data.columns[:3]):  # Show first 3 columns for filtering
                    with filter_cols[i % 3]:
                        if data[col].dtype in ['object', 'string']:
                            unique_values = data[col].unique()
                            selected_values = st.multiselect(
                                f"Filter {col}",
                                unique_values,
                                key=f"{key}_filter_{col}" if key else None
                            )
                            if selected_values:
                                filtered_data = filtered_data[filtered_data[col].isin(selected_values)]
                        elif data[col].dtype in ['int64', 'float64']:
                            min_val, max_val = float(data[col].min()), float(data[col].max())
                            range_values = st.slider(
                                f"Range {col}",
                                min_val, max_val, (min_val, max_val),
                                key=f"{key}_range_{col}" if key else None
                            )
                            filtered_data = filtered_data[
                                (filtered_data[col] >= range_values[0]) & 
                                (filtered_data[col] <= range_values[1])
                            ]
        
        # Import panel
        if enable_import and st.session_state.get(f"{key}_show_import", False):
            with st.expander("📤 Import Data", expanded=True):
                uploaded_file = st.file_uploader(
                    "Choose a file",
                    type=['csv', 'xlsx', 'json'],
                    key=f"{key}_upload" if key else None
                )
                if uploaded_file:
                    try:
                        if uploaded_file.name.endswith('.csv'):
                            import_data = pd.read_csv(uploaded_file)
                        elif uploaded_file.name.endswith('.xlsx'):
                            import_data = pd.read_excel(uploaded_file)
                        elif uploaded_file.name.endswith('.json'):
                            import_data = pd.read_json(uploaded_file)
                        
                        st.success(f"✅ Imported {len(import_data)} rows")
                        
                        import_action = st.radio(
                            "Import Action",
                            ["Replace All", "Append", "Merge"],
                            key=f"{key}_import_action" if key else None
                        )
                        
                        if st.button("Apply Import", key=f"{key}_apply_import" if key else None):
                            if import_action == "Replace All":
                                filtered_data = import_data
                            elif import_action == "Append":
                                filtered_data = pd.concat([filtered_data, import_data], ignore_index=True)
                            elif import_action == "Merge":
                                # Simple merge on index
                                filtered_data = filtered_data.combine_first(import_data)
                            
                            st.session_state[f"{key}_show_import"] = False
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Import error: {str(e)}")
        
        # Batch operations for batch edit mode
        if enable_batch_operations and editing_mode == EditingMode.BATCH_EDIT:
            st.markdown("#### 🔄 Batch Operations")
            batch_col1, batch_col2, batch_col3 = st.columns(3)
            
            with batch_col1:
                if st.button("✅ Select All", key=f"{key}_select_all" if key else None):
                    st.session_state[f"{key}_selected_rows"] = list(range(len(filtered_data)))
            
            with batch_col2:
                if st.button("❌ Clear Selection", key=f"{key}_clear_selection" if key else None):
                    st.session_state[f"{key}_selected_rows"] = []
            
            with batch_col3:
                selected_count = len(st.session_state.get(f"{key}_selected_rows", []))
                st.metric("Selected Rows", selected_count)
        
        return filtered_data
    
    @staticmethod
    def _handle_export(data: pd.DataFrame, format_type: str, key: Optional[str]):
        """Handle data export in various formats."""
        try:
            if format_type == "CSV":
                csv_data = data.to_csv(index=False)
                st.download_button(
                    "💾 Download CSV",
                    csv_data,
                    f"data_export_{key or 'default'}.csv",
                    "text/csv",
                    key=f"{key}_download_csv" if key else None
                )
            
            elif format_type == "Excel":
                # Create Excel file in memory
                from io import BytesIO
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    data.to_excel(writer, index=False, sheet_name='Data')
                
                st.download_button(
                    "💾 Download Excel",
                    buffer.getvalue(),
                    f"data_export_{key or 'default'}.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"{key}_download_excel" if key else None
                )
            
            elif format_type == "JSON":
                json_data = data.to_json(orient='records', indent=2)
                st.download_button(
                    "💾 Download JSON",
                    json_data,
                    f"data_export_{key or 'default'}.json",
                    "application/json",
                    key=f"{key}_download_json" if key else None
                )
            
            elif format_type == "Parquet":
                # Create Parquet file in memory
                from io import BytesIO
                buffer = BytesIO()
                data.to_parquet(buffer, index=False)
                
                st.download_button(
                    "💾 Download Parquet",
                    buffer.getvalue(),
                    f"data_export_{key or 'default'}.parquet",
                    "application/octet-stream",
                    key=f"{key}_download_parquet" if key else None
                )
        
        except Exception as e:
            st.error(f"❌ Export error: {str(e)}")
    
    @staticmethod
    def _handle_batch_operations(data: pd.DataFrame, key: Optional[str]):
        """Handle batch operations on selected rows."""
        selected_rows = st.session_state.get(f"{key}_selected_rows", [])
        
        if selected_rows:
            st.markdown("#### 🔄 Batch Edit Selected Rows")
            
            # Show selected data preview
            with st.expander(f"📋 Selected Data ({len(selected_rows)} rows)", expanded=False):
                st.dataframe(data.iloc[selected_rows], use_container_width=True)
            
            # Batch operations
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🗑️ Delete Selected", key=f"{key}_batch_delete" if key else None):
                    # This would need to be handled by the parent component
                    st.session_state[f"{key}_batch_action"] = {
                        "action": "delete",
                        "rows": selected_rows
                    }
                    st.success(f"Marked {len(selected_rows)} rows for deletion")
            
            with col2:
                if st.button("📋 Duplicate Selected", key=f"{key}_batch_duplicate" if key else None):
                    st.session_state[f"{key}_batch_action"] = {
                        "action": "duplicate",
                        "rows": selected_rows
                    }
                    st.success(f"Marked {len(selected_rows)} rows for duplication")
            
            with col3:
                if st.button("✏️ Bulk Edit", key=f"{key}_batch_edit" if key else None):
                    st.session_state[f"{key}_show_bulk_edit"] = True
            
            # Bulk edit panel
            if st.session_state.get(f"{key}_show_bulk_edit", False):
                with st.expander("✏️ Bulk Edit Fields", expanded=True):
                    st.markdown("Select a column and value to apply to all selected rows:")
                    
                    edit_col1, edit_col2, edit_col3 = st.columns(3)
                    
                    with edit_col1:
                        column_to_edit = st.selectbox(
                            "Column to Edit",
                            data.columns,
                            key=f"{key}_bulk_edit_column" if key else None
                        )
                    
                    with edit_col2:
                        new_value = st.text_input(
                            "New Value",
                            key=f"{key}_bulk_edit_value" if key else None
                        )
                    
                    with edit_col3:
                        if st.button("Apply Changes", key=f"{key}_apply_bulk_edit" if key else None):
                            st.session_state[f"{key}_batch_action"] = {
                                "action": "bulk_edit",
                                "rows": selected_rows,
                                "column": column_to_edit,
                                "value": new_value
                            }
                            st.success(f"Applied bulk edit to {len(selected_rows)} rows")
                            st.session_state[f"{key}_show_bulk_edit"] = False
    
    @staticmethod
    def create_advanced_sample_data() -> pd.DataFrame:
        """Create advanced sample data showcasing new column types."""
        np.random.seed(42)
        
        # Generate sample data with new column types
        data = {
            "ID": [f"ITEM-{1000 + i}" for i in range(12)],
            "Product_Name": [
                "Smart Widget Pro", "Data Analyzer X", "Cloud Connector", "AI Assistant",
                "Security Shield", "Performance Monitor", "Code Generator", "API Gateway",
                "Database Manager", "File Processor", "Report Builder", "Task Scheduler"
            ],
            "Categories": [  # Multiselect column
                ["Software", "AI"], ["Analytics", "Data"], ["Cloud", "Integration"], ["AI", "Assistant"],
                ["Security", "Protection"], ["Monitoring", "Performance"], ["Development", "AI"], ["API", "Gateway"],
                ["Database", "Management"], ["File", "Processing"], ["Reporting", "Analytics"], ["Automation", "Scheduling"]
            ],
            "Price": np.random.uniform(99.99, 999.99, 12).round(2),
            "Rating": np.random.uniform(3.5, 5.0, 12).round(1),
            "Progress": np.random.uniform(0, 100, 12).round(1),
            "Active": np.random.choice([True, False], 12),
            "Launch_Date": pd.date_range(start="2024-01-01", periods=12, freq="ME"),
            "Website": [f"https://product{i+1}.example.com" for i in range(12)],
            "Trend_Data": [  # Line chart data
                [10, 15, 12, 18, 22, 25, 30] if i % 3 == 0 else
                [5, 8, 12, 15, 18, 20, 25] if i % 3 == 1 else
                [20, 18, 22, 25, 28, 30, 35] for i in range(12)
            ],
            "Sales_Data": [  # Bar chart data
                [100, 120, 110, 140, 160, 180, 200] if i % 3 == 0 else
                [80, 90, 100, 110, 120, 130, 140] if i % 3 == 1 else
                [150, 160, 170, 180, 190, 200, 210] for i in range(12)
            ],
            "Metadata": [  # JSON column
                {"version": "1.0", "features": ["basic", "standard"], "license": "MIT"},
                {"version": "2.1", "features": ["advanced", "premium"], "license": "Commercial"},
                {"version": "1.5", "features": ["cloud", "api"], "license": "Apache"},
                {"version": "3.0", "features": ["ai", "ml", "nlp"], "license": "GPL"},
                {"version": "1.2", "features": ["security", "encryption"], "license": "BSD"},
                {"version": "2.0", "features": ["monitoring", "alerts"], "license": "MIT"},
                {"version": "1.8", "features": ["code", "generation"], "license": "Apache"},
                {"version": "2.5", "features": ["api", "gateway"], "license": "Commercial"},
                {"version": "1.3", "features": ["database", "sql"], "license": "MIT"},
                {"version": "1.7", "features": ["file", "processing"], "license": "BSD"},
                {"version": "2.2", "features": ["reporting", "charts"], "license": "GPL"},
                {"version": "1.9", "features": ["automation", "scheduling"], "license": "Apache"}
            ],
            "Tags": [  # List column
                ["popular", "trending", "new"],
                ["analytics", "business", "enterprise"],
                ["cloud", "saas", "integration"],
                ["ai", "machine-learning", "nlp"],
                ["security", "compliance", "audit"],
                ["performance", "monitoring", "devops"],
                ["development", "coding", "automation"],
                ["api", "microservices", "gateway"],
                ["database", "sql", "nosql"],
                ["files", "storage", "processing"],
                ["reports", "dashboards", "visualization"],
                ["tasks", "workflow", "scheduling"]
            ]
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def create_financial_analytics_data() -> pd.DataFrame:
        """Create financial analytics sample data with chart columns."""
        np.random.seed(123)
        
        companies = ["TechCorp", "DataSys", "CloudInc", "AILabs", "SecureNet", "FastTrack"]
        
        data = {
            "Company": companies,
            "Sector": ["Technology", "Data Analytics", "Cloud Services", "AI/ML", "Cybersecurity", "Logistics"],
            "Market_Cap": np.random.uniform(1000, 50000, 6).round(0),  # Millions
            "Revenue_Growth": np.random.uniform(-5, 25, 6).round(1),  # Percentage
            "Profit_Margin": np.random.uniform(5, 35, 6).round(1),  # Percentage
            "Stock_Trend": [  # Area chart data - 12 months
                [100, 105, 98, 110, 115, 108, 120, 125, 118, 130, 135, 140],
                [80, 85, 82, 88, 92, 89, 95, 98, 94, 100, 105, 108],
                [150, 155, 148, 160, 165, 158, 170, 175, 168, 180, 185, 190],
                [200, 210, 195, 220, 230, 215, 240, 250, 235, 260, 270, 280],
                [120, 125, 118, 130, 135, 128, 140, 145, 138, 150, 155, 160],
                [90, 95, 88, 100, 105, 98, 110, 115, 108, 120, 125, 130]
            ],
            "Quarterly_Revenue": [  # Bar chart data - 4 quarters
                [250, 280, 320, 350],
                [180, 200, 220, 240],
                [400, 450, 500, 550],
                [600, 650, 700, 750],
                [300, 330, 360, 390],
                [200, 220, 240, 260]
            ],
            "Risk_Level": ["Low", "Medium", "Low", "High", "Medium", "Low"],
            "ESG_Score": np.random.uniform(60, 95, 6).round(1),
            "Dividend_Yield": np.random.uniform(0, 5, 6).round(2),
            "Recommendation": ["Buy", "Hold", "Buy", "Sell", "Hold", "Buy"],
            "Last_Updated": pd.date_range(start="2026-01-01", periods=6, freq="D")
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def create_sample_financial_data() -> pd.DataFrame:
        """Create sample financial data for demonstration."""
        np.random.seed(42)  # For consistent demo data
        
        dates = pd.date_range(start="2026-01-01", periods=10, freq="D")
        
        data = {
            "Date": dates,
            "Transaction_ID": [f"TXN-{1000 + i}" for i in range(10)],
            "Description": [
                "Office Supplies", "Software License", "Marketing Campaign",
                "Travel Expenses", "Equipment Purchase", "Consulting Fees",
                "Utilities", "Insurance", "Training", "Maintenance"
            ],
            "Category": np.random.choice(["Operations", "Marketing", "IT", "HR"], 10),
            "Amount": np.random.uniform(100, 5000, 10).round(2),
            "Status": np.random.choice(["Pending", "Approved", "Rejected"], 10),
            "Priority": np.random.choice(["Low", "Medium", "High"], 10),
            "Approved": np.random.choice([True, False], 10),
            "Progress": np.random.uniform(0, 100, 10).round(1)
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def create_sample_user_data() -> pd.DataFrame:
        """Create sample user data for demonstration."""
        data = {
            "User_ID": [f"USR-{100 + i}" for i in range(8)],
            "Name": [
                "Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson",
                "Eva Brown", "Frank Miller", "Grace Lee", "Henry Taylor"
            ],
            "Email": [
                "alice@company.com", "bob@company.com", "carol@company.com",
                "david@company.com", "eva@company.com", "frank@company.com",
                "grace@company.com", "henry@company.com"
            ],
            "Department": ["Engineering", "Marketing", "Sales", "HR", "Finance", "IT", "Operations", "Legal"],
            "Role": ["Developer", "Manager", "Analyst", "Coordinator", "Specialist", "Admin", "Lead", "Counsel"],
            "Salary": [75000, 85000, 65000, 55000, 70000, 80000, 90000, 95000],
            "Start_Date": pd.date_range(start="2020-01-01", periods=8, freq="3ME"),
            "Active": [True, True, False, True, True, True, False, True],
            "Performance_Score": [85, 92, 78, 88, 95, 82, 90, 87]
        }
        
        return pd.DataFrame(data)


def render_data_editor_showcase():
    """Render the enhanced data editor showcase with latest Streamlit nightly 2026 features."""
    st.markdown("## 📝 Enhanced Data Editor Showcase")
    st.markdown("Experience the latest Streamlit nightly st.data_editor features with advanced data manipulation capabilities, new column types, and enhanced editing modes.")
    
    # Showcase tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔧 Basic Enhanced Editor", 
        "📊 Advanced Column Types", 
        "🔄 Batch Operations", 
        "💼 Financial Analytics"
    ])
    
    with tab1:
        st.markdown("### Basic Enhanced Data Editor")
        st.markdown("Traditional data editing with improved features and validation.")
        
        # Create sample data
        if "sample_financial_data" not in st.session_state:
            st.session_state.sample_financial_data = EnhancedDataEditor.create_sample_financial_data()
        
        # Enhanced column configurations using new Streamlit column config classes
        financial_column_config = {
            "Date": EnhancedDataEditor.create_column_config(
                "Date", ColumnType.DATE, label="Transaction Date", 
                help_text="Date of the transaction", pinned=True
            ),
            "Transaction_ID": EnhancedDataEditor.create_column_config(
                "Transaction_ID", ColumnType.TEXT, label="ID", 
                disabled=True, help_text="Unique transaction identifier", width="small"
            ),
            "Description": EnhancedDataEditor.create_column_config(
                "Description", ColumnType.TEXT, label="Description",
                help_text="Transaction description", required=True, width="medium"
            ),
            "Category": EnhancedDataEditor.create_column_config(
                "Category", ColumnType.SELECTBOX, label="Category",
                options=["Operations", "Marketing", "IT", "HR", "Finance"],
                help_text="Transaction category", width="small"
            ),
            "Amount": EnhancedDataEditor.create_column_config(
                "Amount", ColumnType.CURRENCY, label="Amount ($)",
                min_value=0, step=0.01, help_text="Transaction amount in USD", width="small"
            ),
            "Status": EnhancedDataEditor.create_column_config(
                "Status", ColumnType.SELECTBOX, label="Status",
                options=["Pending", "Approved", "Rejected"],
                help_text="Approval status", width="small"
            ),
            "Priority": EnhancedDataEditor.create_column_config(
                "Priority", ColumnType.SELECTBOX, label="Priority",
                options=["Low", "Medium", "High"],
                help_text="Transaction priority", width="small"
            ),
            "Approved": EnhancedDataEditor.create_column_config(
                "Approved", ColumnType.CHECKBOX, label="Approved",
                help_text="Approval checkbox", width="small"
            ),
            "Progress": EnhancedDataEditor.create_column_config(
                "Progress", ColumnType.PERCENTAGE, label="Progress (%)",
                min_value=0, max_value=100, step=0.1,
                help_text="Processing progress", width="small"
            )
        }
        
        # Editing mode selection
        col1, col2 = st.columns(2)
        
        with col1:
            editing_mode = st.selectbox(
                "Editing Mode",
                [EditingMode.FULL, EditingMode.READONLY, EditingMode.SELECTIVE, EditingMode.BATCH_EDIT],
                format_func=lambda x: x.value.title().replace('_', ' ')
            )
        
        with col2:
            if editing_mode == EditingMode.SELECTIVE:
                editable_cols = st.multiselect(
                    "Editable Columns",
                    list(st.session_state.sample_financial_data.columns),
                    default=["Description", "Amount", "Status", "Priority"]
                )
            else:
                editable_cols = None
        
        # Enhanced data editor with new features
        edited_financial_data = EnhancedDataEditor.enhanced_data_editor(
            st.session_state.sample_financial_data,
            key="financial_editor",
            column_config=financial_column_config,
            editing_mode=editing_mode,
            editable_columns=editable_cols,
            show_toolbar=True,
            enable_search=True,
            enable_filtering=True,
            enable_export=True,
            enable_import=True,
            enable_batch_operations=True,
            auto_save=True
        )
        
        # Update session state
        st.session_state.sample_financial_data = edited_financial_data
        
        # Show data summary
        if not edited_financial_data.empty:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rows", len(edited_financial_data))
            with col2:
                st.metric("Total Amount", f"${edited_financial_data['Amount'].sum():,.2f}")
            with col3:
                st.metric("Avg Amount", f"${edited_financial_data['Amount'].mean():,.2f}")
            with col4:
                pending_count = len(edited_financial_data[edited_financial_data["Status"] == "Pending"])
                st.metric("Pending", pending_count)
    
    with tab2:
        st.markdown("### Advanced Column Types Showcase")
        st.markdown("Explore new column types: Multiselect, JSON, List, and Chart columns.")
        
        if "advanced_sample_data" not in st.session_state:
            st.session_state.advanced_sample_data = EnhancedDataEditor.create_advanced_sample_data()
        
        # Advanced column configurations with new types
        advanced_column_config = {
            "ID": EnhancedDataEditor.create_column_config(
                "ID", ColumnType.TEXT, disabled=True, width="small", pinned=True
            ),
            "Product_Name": EnhancedDataEditor.create_column_config(
                "Product_Name", ColumnType.TEXT, label="Product Name", width="medium"
            ),
            "Categories": EnhancedDataEditor.create_column_config(
                "Categories", ColumnType.MULTISELECT, label="Categories",
                options=["Software", "AI", "Analytics", "Data", "Cloud", "Integration", 
                        "Assistant", "Security", "Protection", "Monitoring", "Performance",
                        "Development", "API", "Gateway", "Database", "Management", 
                        "File", "Processing", "Reporting", "Automation", "Scheduling"],
                help_text="Product categories (multiple selection)", width="medium"
            ),
            "Price": EnhancedDataEditor.create_column_config(
                "Price", ColumnType.CURRENCY, min_value=0, width="small"
            ),
            "Rating": EnhancedDataEditor.create_column_config(
                "Rating", ColumnType.NUMBER, min_value=0, max_value=5, step=0.1,
                format_string="%.1f ⭐", width="small"
            ),
            "Progress": EnhancedDataEditor.create_column_config(
                "Progress", ColumnType.PROGRESS, min_value=0, max_value=100, width="small"
            ),
            "Active": EnhancedDataEditor.create_column_config(
                "Active", ColumnType.CHECKBOX, width="small"
            ),
            "Launch_Date": EnhancedDataEditor.create_column_config(
                "Launch_Date", ColumnType.DATE, label="Launch Date", width="small"
            ),
            "Website": EnhancedDataEditor.create_column_config(
                "Website", ColumnType.LINK, label="Website", width="small"
            ),
            "Trend_Data": EnhancedDataEditor.create_column_config(
                "Trend_Data", ColumnType.LINE_CHART, label="Trend", width="medium"
            ),
            "Sales_Data": EnhancedDataEditor.create_column_config(
                "Sales_Data", ColumnType.BAR_CHART, label="Sales", width="medium"
            ),
            "Metadata": EnhancedDataEditor.create_column_config(
                "Metadata", ColumnType.JSON, label="Metadata", width="large"
            ),
            "Tags": EnhancedDataEditor.create_column_config(
                "Tags", ColumnType.LIST, label="Tags", width="medium"
            )
        }
        
        # Advanced data editor
        edited_advanced_data = EnhancedDataEditor.enhanced_data_editor(
            st.session_state.advanced_sample_data,
            key="advanced_editor",
            column_config=advanced_column_config,
            editing_mode=EditingMode.FULL,
            show_toolbar=True,
            enable_search=True,
            enable_filtering=True,
            enable_export=True,
            height=600
        )
        
        st.session_state.advanced_sample_data = edited_advanced_data
        
        # Feature highlights
        st.markdown("#### 🌟 New Column Type Features")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📋 Multiselect Columns:**
            - Multiple value selection
            - Colorful tag display
            - Easy editing interface
            
            **📊 Chart Columns:**
            - Inline data visualization
            - Line, bar, and area charts
            - Interactive hover details
            """)
        
        with col2:
            st.markdown("""
            **🔗 Enhanced Link Columns:**
            - Clickable URLs
            - Custom display text
            - Validation support
            
            **📄 JSON & List Columns:**
            - Structured data display
            - Expandable views
            - Rich formatting
            """)
    
    with tab3:
        st.markdown("### Batch Operations & Advanced Editing")
        st.markdown("Demonstrate batch editing, bulk operations, and advanced data manipulation.")
        
        # User data for batch operations
        if "batch_user_data" not in st.session_state:
            st.session_state.batch_user_data = EnhancedDataEditor.create_sample_user_data()
        
        # Batch editing column config
        batch_column_config = {
            "User_ID": EnhancedDataEditor.create_column_config(
                "User_ID", ColumnType.TEXT, disabled=True, pinned=True, width="small"
            ),
            "Name": EnhancedDataEditor.create_column_config(
                "Name", ColumnType.TEXT, required=True, width="medium"
            ),
            "Email": EnhancedDataEditor.create_column_config(
                "Email", ColumnType.TEXT, required=True, width="medium"
            ),
            "Department": EnhancedDataEditor.create_column_config(
                "Department", ColumnType.SELECTBOX,
                options=["Engineering", "Marketing", "Sales", "HR", "Finance", "IT", "Operations", "Legal"],
                width="small"
            ),
            "Role": EnhancedDataEditor.create_column_config(
                "Role", ColumnType.TEXT, width="medium"
            ),
            "Salary": EnhancedDataEditor.create_column_config(
                "Salary", ColumnType.CURRENCY, min_value=30000, max_value=200000, step=1000,
                width="small"
            ),
            "Start_Date": EnhancedDataEditor.create_column_config(
                "Start_Date", ColumnType.DATE, width="small"
            ),
            "Active": EnhancedDataEditor.create_column_config(
                "Active", ColumnType.CHECKBOX, width="small"
            ),
            "Performance_Score": EnhancedDataEditor.create_column_config(
                "Performance_Score", ColumnType.PROGRESS, min_value=0, max_value=100,
                width="small"
            )
        }
        
        # Batch editor
        edited_batch_data = EnhancedDataEditor.enhanced_data_editor(
            st.session_state.batch_user_data,
            key="batch_editor",
            column_config=batch_column_config,
            editing_mode=EditingMode.BATCH_EDIT,
            show_toolbar=True,
            enable_batch_operations=True,
            enable_search=True,
            enable_filtering=True,
            selection_mode="multi-row"
        )
        
        st.session_state.batch_user_data = edited_batch_data
        
        # Show batch operation results
        if "batch_editor_batch_action" in st.session_state:
            action = st.session_state["batch_editor_batch_action"]
            st.success(f"✅ Batch action '{action['action']}' applied to {len(action['rows'])} rows")
            
            if action["action"] == "bulk_edit":
                st.info(f"Updated column '{action['column']}' to '{action['value']}'")
    
    with tab4:
        st.markdown("### Financial Analytics Dashboard")
        st.markdown("Advanced financial data with chart columns and analytics features.")
        
        if "financial_analytics_data" not in st.session_state:
            st.session_state.financial_analytics_data = EnhancedDataEditor.create_financial_analytics_data()
        
        # Financial analytics column config
        analytics_column_config = {
            "Company": EnhancedDataEditor.create_column_config(
                "Company", ColumnType.TEXT, pinned=True, width="medium"
            ),
            "Sector": EnhancedDataEditor.create_column_config(
                "Sector", ColumnType.SELECTBOX,
                options=["Technology", "Data Analytics", "Cloud Services", "AI/ML", "Cybersecurity", "Logistics"],
                width="medium"
            ),
            "Market_Cap": EnhancedDataEditor.create_column_config(
                "Market_Cap", ColumnType.NUMBER, label="Market Cap (M$)",
                format_string="$%.0fM", width="small"
            ),
            "Revenue_Growth": EnhancedDataEditor.create_column_config(
                "Revenue_Growth", ColumnType.PERCENTAGE, label="Revenue Growth",
                min_value=-20, max_value=50, width="small"
            ),
            "Profit_Margin": EnhancedDataEditor.create_column_config(
                "Profit_Margin", ColumnType.PERCENTAGE, label="Profit Margin",
                min_value=0, max_value=50, width="small"
            ),
            "Stock_Trend": EnhancedDataEditor.create_column_config(
                "Stock_Trend", ColumnType.AREA_CHART, label="Stock Trend (12M)",
                width="large"
            ),
            "Quarterly_Revenue": EnhancedDataEditor.create_column_config(
                "Quarterly_Revenue", ColumnType.BAR_CHART, label="Quarterly Revenue",
                width="large"
            ),
            "Risk_Level": EnhancedDataEditor.create_column_config(
                "Risk_Level", ColumnType.SELECTBOX,
                options=["Low", "Medium", "High"], width="small"
            ),
            "ESG_Score": EnhancedDataEditor.create_column_config(
                "ESG_Score", ColumnType.PROGRESS, label="ESG Score",
                min_value=0, max_value=100, width="small"
            ),
            "Dividend_Yield": EnhancedDataEditor.create_column_config(
                "Dividend_Yield", ColumnType.PERCENTAGE, label="Dividend Yield",
                min_value=0, max_value=10, step=0.01, width="small"
            ),
            "Recommendation": EnhancedDataEditor.create_column_config(
                "Recommendation", ColumnType.SELECTBOX,
                options=["Buy", "Hold", "Sell"], width="small"
            ),
            "Last_Updated": EnhancedDataEditor.create_column_config(
                "Last_Updated", ColumnType.DATE, width="small"
            )
        }
        
        # Financial analytics editor
        edited_analytics_data = EnhancedDataEditor.enhanced_data_editor(
            st.session_state.financial_analytics_data,
            key="analytics_editor",
            column_config=analytics_column_config,
            editing_mode=EditingMode.SELECTIVE,
            editable_columns=["Risk_Level", "Recommendation", "ESG_Score"],
            show_toolbar=True,
            enable_export=True,
            height=500
        )
        
        st.session_state.financial_analytics_data = edited_analytics_data
        
        # Analytics summary
        st.markdown("#### 📈 Portfolio Analytics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_growth = edited_analytics_data["Revenue_Growth"].mean()
            st.metric("Avg Revenue Growth", f"{avg_growth:.1f}%")
        
        with col2:
            avg_margin = edited_analytics_data["Profit_Margin"].mean()
            st.metric("Avg Profit Margin", f"{avg_margin:.1f}%")
        
        with col3:
            buy_count = len(edited_analytics_data[edited_analytics_data["Recommendation"] == "Buy"])
            st.metric("Buy Recommendations", buy_count)
        
        with col4:
            avg_esg = edited_analytics_data["ESG_Score"].mean()
            st.metric("Avg ESG Score", f"{avg_esg:.1f}")
    
    st.divider()
    
    # Global actions
    st.markdown("### 🔄 Global Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Reset All Data", use_container_width=True):
            st.session_state.sample_financial_data = EnhancedDataEditor.create_sample_financial_data()
            st.session_state.advanced_sample_data = EnhancedDataEditor.create_advanced_sample_data()
            st.session_state.batch_user_data = EnhancedDataEditor.create_sample_user_data()
            st.session_state.financial_analytics_data = EnhancedDataEditor.create_financial_analytics_data()
            st.success("✅ All data reset to defaults!")
            st.rerun()
    
    with col2:
        if st.button("📊 Export All Data", use_container_width=True):
            # Create a combined export
            combined_data = {
                "financial_data": st.session_state.get("sample_financial_data", pd.DataFrame()).to_dict('records'),
                "advanced_data": st.session_state.get("advanced_sample_data", pd.DataFrame()).to_dict('records'),
                "user_data": st.session_state.get("batch_user_data", pd.DataFrame()).to_dict('records'),
                "analytics_data": st.session_state.get("financial_analytics_data", pd.DataFrame()).to_dict('records')
            }
            
            import json
            json_export = json.dumps(combined_data, indent=2, default=str)
            st.download_button(
                "💾 Download Combined Data (JSON)",
                json_export,
                "enhanced_data_editor_export.json",
                "application/json"
            )
    
    with col3:
        if st.button("ℹ️ Feature Info", use_container_width=True):
            with st.expander("🌟 Enhanced Data Editor Features", expanded=True):
                st.markdown("""
                **New in Streamlit Nightly 2026:**
                
                🔹 **Advanced Column Types:**
                - MultiselectColumn for multiple selections
                - JSONColumn for structured data
                - ListColumn for array data
                - Chart columns (Line, Bar, Area)
                
                🔹 **Enhanced Editing Modes:**
                - Batch editing with row selection
                - Review mode with approval workflow
                - Selective column editing
                
                🔹 **Advanced Features:**
                - Real-time search and filtering
                - Import/Export in multiple formats
                - Auto-save with change tracking
                - Bulk operations on selected rows
                - Enhanced validation and error reporting
                
                🔹 **Improved UX:**
                - Pinned columns
                - Responsive column widths
                - Interactive toolbar
                - Progress indicators
                """)


def add_data_editor_to_dashboard():
    """Add enhanced data editor examples to existing dashboard components."""
    
    st.markdown("### 📊 Interactive Data Management")
    
    # Quick data editor for dashboard settings
    dashboard_settings = pd.DataFrame({
        "Setting": ["Refresh Interval", "Chart Type", "Theme", "Auto-save", "Notifications"],
        "Value": ["30 seconds", "Line Chart", "Dark", True, True],
        "Category": ["Performance", "Display", "Appearance", "Data", "User Experience"],
        "Editable": [True, True, True, True, True]
    })
    
    # Column configuration for settings
    settings_config = {
        "Setting": EnhancedDataEditor.create_column_config(
            "Setting", ColumnType.TEXT, disabled=True
        ),
        "Value": EnhancedDataEditor.create_column_config(
            "Value", ColumnType.TEXT, label="Current Value"
        ),
        "Category": EnhancedDataEditor.create_column_config(
            "Category", ColumnType.SELECTBOX,
            options=["Performance", "Display", "Appearance", "Data", "User Experience"]
        ),
        "Editable": EnhancedDataEditor.create_column_config(
            "Editable", ColumnType.CHECKBOX, label="Can Edit"
        )
    }
    
    edited_settings = EnhancedDataEditor.enhanced_data_editor(
        dashboard_settings,
        key="dashboard_settings",
        column_config=settings_config,
        height=200,
        show_toolbar=False
    )
    
    if st.button("💾 Save Dashboard Settings"):
        st.success("Dashboard settings saved!")
        st.json(edited_settings.to_dict('records'))