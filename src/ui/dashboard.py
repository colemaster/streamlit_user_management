"""
Modern FinOps Dashboard - Streamlit 1.52+
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.finops.data import generate_mock_data
from src.auth.permissions import has_permission, get_current_permission
from src.auth.config import PermissionLevel
from src.ui.components import render_metric_card, render_status_badge, animated_header


def render_dashboard():
    """Render the modern FinOps dashboard with permission checks."""
    current_permission = get_current_permission()

    if not current_permission or not has_permission(PermissionLevel.ANALYST):
        st.error("🔒 Access Denied: Requires ANALYST permission level.")
        return

    # Initialize Data
    # usage of st.cache_data handles persistence; no need for manual session state check
    df = generate_mock_data()

    # 1. Header Section
    col1, col2 = st.columns([5, 1])
    with col1:
        animated_header(
            "Cloud Intelligence", "Real-time cost analytics and forecasting"
        )
    with col2:
        st.write("")  # Spacer
        if st.button("🔄 Refresh Data", type="secondary", use_container_width=True):
            generate_mock_data.clear()
            st.rerun()

    # 2. Filters (Glass Look)
    with st.container():
        st.markdown(
            '<div class="glass-card" style="padding: 1rem; margin-bottom: 2rem;">',
            unsafe_allow_html=True,
        )
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            selected_service = st.selectbox(
                "Service", ["All Services"] + list(df["Service"].unique())
            )
        with f_col2:
            selected_region = st.selectbox(
                "Region", ["All Regions"] + list(df["Region"].unique())
            )
        with f_col3:
            date_range = st.datetime_input(
                "Date Range", (df["Date"].min(), df["Date"].max())
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # Apply Filters
    filtered_df = df.copy()
    if selected_service != "All Services":
        filtered_df = filtered_df[filtered_df["Service"] == selected_service]
    if selected_region != "All Regions":
        filtered_df = filtered_df[filtered_df["Region"] == selected_region]
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["Date"].dt.date >= date_range[0])
            & (filtered_df["Date"].dt.date <= date_range[1])
        ]

    # 3. KPI Cards
    _render_kpi_section(filtered_df, df)

    # 4. Main Charts
    st.markdown("### Cost Analysis")
    st.markdown("---")
    _render_main_charts(filtered_df)

    # 5. Data Table
    st.markdown("### Detailed Breakdown")
    _render_data_table(filtered_df)

    # 6. Admin Section
    if has_permission(PermissionLevel.ADMIN):
        _render_admin_section(filtered_df)


def _render_kpi_section(filtered_df, full_df):
    total_cost = filtered_df["Unblended Cost"].sum()
    prev_cost = total_cost * 0.92  # Mock
    change = ((total_cost - prev_cost) / prev_cost) * 100

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card(
            "Total Spend",
            f"${total_cost:,.0f}",
            f"{change:+.1f}%",
            "success" if change < 0 else "error",
        )
    with col2:
        avg_daily = filtered_df.groupby("Date")["Unblended Cost"].sum().mean()
        render_metric_card("Daily Avg", f"${avg_daily:,.0f}", None, "neutral")
    with col3:
        forecast = total_cost * 1.12
        render_metric_card("Forecast (EOM)", f"${forecast:,.0f}", "+12%", "error")
    with col4:
        services_count = filtered_df["Service"].nunique()
        render_metric_card("Active Services", str(services_count), None, "neutral")

    st.markdown("<br>", unsafe_allow_html=True)


def _render_main_charts(df):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.caption("Daily Cost Trend")

        daily_cost = df.groupby("Date")["Unblended Cost"].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=daily_cost["Date"],
                y=daily_cost["Unblended Cost"],
                mode="lines",
                line=dict(color="#FF5500", width=3, shape="spline"),
                fill="tozeroy",
                fillcolor="rgba(255, 85, 0, 0.1)",
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            height=350,
            xaxis=dict(showgrid=False, gridcolor="#333"),
            yaxis=dict(showgrid=True, gridcolor="#333", zeroline=False),
            font=dict(color="#A0A5AA"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.caption("Service Distribution")

        service_cost = (
            df.groupby("Service")["Unblended Cost"]
            .sum()
            .reset_index()
            .sort_values("Unblended Cost", ascending=False)
        )

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=service_cost["Service"],
                    values=service_cost["Unblended Cost"],
                    hole=0.7,
                    marker=dict(colors=px.colors.qualitative.Bold),
                    textinfo="none",
                )
            ]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=10),
            height=350,
            showlegend=True,
            legend=dict(orientation="h", x=0, y=-0.1, font=dict(color="#A0A5AA")),
            annotations=[
                dict(
                    text=f"${df['Unblended Cost'].sum():,.0f}",
                    x=0.5,
                    y=0.5,
                    font_size=20,
                    showarrow=False,
                    font_color="#fff",
                )
            ],
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


def _render_data_table(df):
    with st.container():
        # Aggregation
        agg = (
            df.groupby(["Service", "Region"])
            .agg({"Unblended Cost": "sum", "Usage Quantity": "sum"})
            .reset_index()
        )

        st.dataframe(
            agg,
            use_container_width=True,
            column_config={
                "Unblended Cost": st.column_config.NumberColumn(format="$%.2f"),
                "Usage Quantity": st.column_config.ProgressColumn(
                    format="%.2f", min_value=0, max_value=df["Usage Quantity"].max()
                ),
            },
            hide_index=True,
        )


def _render_admin_section(df):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="glass-card" style="border-color: var(--accent-primary);">',
        unsafe_allow_html=True,
    )
    st.markdown("### 🔐 Admin Insights")

    col1, col2 = st.columns(2)
    with col1:
        st.info("Anomaly Detection Model: Active (v2.1)")
        render_status_badge("active", "Inference Engine")
    with col2:
        st.warning("Budget Threshold: 85% Reached")
        render_status_badge("warning", "Budget Alert")

    st.markdown("</div>", unsafe_allow_html=True)
