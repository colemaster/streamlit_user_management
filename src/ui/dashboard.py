"""
Modern FinOps Dashboard - Streamlit 1.52+
Professional layout with advanced visualizations and interactive tables.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from src.finops.data import generate_mock_data
from src.auth.permissions import has_permission, get_current_permission
from src.auth.config import PermissionLevel


def render_dashboard():
    """Render the modern FinOps dashboard with permission checks."""

    # Permission check
    current_permission = get_current_permission()
    if not current_permission:
        st.error(
            "🔒 Unable to determine your permission level. Please contact your administrator."
        )
        return

    if not has_permission(PermissionLevel.ANALYST):
        st.error("🔒 Access Denied")
        st.markdown(
            "You do not have permission to access the detailed dashboard. "
            "Required permission level: **ANALYST**"
        )
        return

    # Load Data
    if "cost_data" not in st.session_state:
        st.session_state.cost_data = generate_mock_data()

    df = st.session_state.cost_data

    # Header with badge
    col_title, col_badge = st.columns([4, 1])
    with col_title:
        st.markdown("## ☁️ Cloud Cost Intelligence", text_alignment="left")
    with col_badge:
        st.badge("Live", icon="🟢")

    st.space(1)

    # Smart Filters Row
    filter_cols = st.columns([2, 2, 2, 1])

    with filter_cols[0]:
        selected_service = st.selectbox(
            "Service",
            options=["All Services"] + list(df["Service"].unique()),
            index=0,
        )

    with filter_cols[1]:
        selected_region = st.selectbox(
            "Region",
            options=["All Regions"] + list(df["Region"].unique()),
            index=0,
        )

    with filter_cols[2]:
        date_range = st.date_input(
            "Date Range",
            value=(df["Date"].min(), df["Date"].max()),
            format="MM/DD/YYYY",
        )

    with filter_cols[3]:
        st.space(2)
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.cost_data = generate_mock_data()
            st.rerun()

    # Apply filters
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

    st.space(2)

    # KPI Cards Row
    _render_kpi_cards(filtered_df, df)

    st.space(2)

    # Main Charts Row
    _render_main_charts(filtered_df)

    st.space(2)

    # Data Table Section
    _render_data_table(filtered_df)

    st.space(2)

    # Admin-only detailed analysis
    if has_permission(PermissionLevel.ADMIN):
        _render_admin_section(filtered_df)


def _render_kpi_cards(filtered_df: pd.DataFrame, full_df: pd.DataFrame):
    """Render KPI metric cards."""
    total_cost = filtered_df["Unblended Cost"].sum()
    prev_period_cost = full_df["Unblended Cost"].sum() * 0.87  # Mock previous period
    cost_change = ((total_cost - prev_period_cost) / prev_period_cost) * 100

    avg_daily = filtered_df.groupby("Date")["Unblended Cost"].sum().mean()
    forecast = total_cost * 1.15

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        with st.container(border=True):
            st.metric(
                "Total Spend (MTD)",
                f"${total_cost:,.0f}",
                f"{cost_change:+.1f}%",
                delta_arrow="up" if cost_change > 0 else "down",
            )

    with col2:
        with st.container(border=True):
            st.metric(
                "Daily Average",
                f"${avg_daily:,.0f}",
                delta_arrow="off",
            )

    with col3:
        with st.container(border=True):
            st.metric(
                "Forecast (EOM)",
                f"${forecast:,.0f}",
                "+15%",
                delta_arrow="up",
            )

    with col4:
        with st.container(border=True):
            st.metric(
                "Active Services",
                f"{filtered_df['Service'].nunique()}",
                delta_arrow="off",
            )

    with col5:
        with st.container(border=True):
            with st.popover("⚠️ Anomalies", use_container_width=True):
                st.markdown("### 🚨 Cost Anomalies Detected", text_alignment="center")
                st.space(1)
                _render_anomaly_list()
            st.metric(
                "Anomalies",
                "3",
                "-2 vs last week",
                delta_color="inverse",
                delta_arrow="down",
            )


def _render_anomaly_list():
    """Render anomaly details in popover."""
    anomalies = [
        {"service": "EC2", "date": "Dec 3", "severity": "high", "change": "+156%"},
        {"service": "S3", "date": "Dec 2", "severity": "medium", "change": "+45%"},
        {"service": "RDS", "date": "Dec 1", "severity": "low", "change": "+22%"},
    ]

    for a in anomalies:
        with st.container(border=True):
            cols = st.columns([2, 1, 1])
            with cols[0]:
                st.markdown(f"**{a['service']}**")
                st.caption(a["date"])
            with cols[1]:
                st.badge(a["severity"].upper(), icon="⚡")
            with cols[2]:
                st.markdown(f"**{a['change']}**")


@st.fragment
def _render_main_charts(df: pd.DataFrame):
    """Render main visualization charts."""
    chart_col1, chart_col2 = st.columns([2, 1])

    with chart_col1:
        with st.container(border=True):
            st.subheader("📈 Cost Trend Analysis")

            # Segmented control for chart type
            chart_type = st.segmented_control(
                "View",
                options=["Daily", "By Service", "By Region"],
                default="Daily",
                selection_mode="single",
            )

            if chart_type == "Daily":
                daily_cost = df.groupby("Date")["Unblended Cost"].sum().reset_index()
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=daily_cost["Date"],
                        y=daily_cost["Unblended Cost"],
                        mode="lines+markers",
                        fill="tozeroy",
                        line=dict(color="#E35302", width=2),
                        marker=dict(size=6),
                        name="Daily Cost",
                    )
                )
                fig.update_layout(
                    xaxis_title=None,
                    yaxis_title="Cost ($)",
                    showlegend=False,
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=350,
                    hovermode="x unified",
                )

            elif chart_type == "By Service":
                service_daily = (
                    df.groupby(["Date", "Service"])["Unblended Cost"]
                    .sum()
                    .reset_index()
                )
                fig = px.area(
                    service_daily,
                    x="Date",
                    y="Unblended Cost",
                    color="Service",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                )
                fig.update_layout(
                    xaxis_title=None,
                    yaxis_title="Cost ($)",
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=350,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02),
                )

            else:  # By Region
                region_daily = (
                    df.groupby(["Date", "Region"])["Unblended Cost"].sum().reset_index()
                )
                fig = px.line(
                    region_daily,
                    x="Date",
                    y="Unblended Cost",
                    color="Region",
                    markers=True,
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                )
                fig.update_layout(
                    xaxis_title=None,
                    yaxis_title="Cost ($)",
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=350,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02),
                )

            st.plotly_chart(fig, use_container_width=True, key="trend_chart")

    with chart_col2:
        with st.container(border=True):
            st.subheader("🍩 Service Distribution")

            service_cost = df.groupby("Service")["Unblended Cost"].sum().reset_index()
            service_cost = service_cost.sort_values("Unblended Cost", ascending=False)

            fig_donut = go.Figure(
                data=[
                    go.Pie(
                        labels=service_cost["Service"],
                        values=service_cost["Unblended Cost"],
                        hole=0.6,
                        marker=dict(
                            colors=px.colors.qualitative.Set2,
                        ),
                        textinfo="percent",
                        textposition="outside",
                    )
                ]
            )
            fig_donut.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="top", y=-0.1),
                margin=dict(l=0, r=0, t=10, b=60),
                height=350,
                annotations=[
                    dict(
                        text=f"${service_cost['Unblended Cost'].sum():,.0f}",
                        x=0.5,
                        y=0.5,
                        font_size=18,
                        showarrow=False,
                    )
                ],
            )
            st.plotly_chart(fig_donut, use_container_width=True)


def _render_data_table(df: pd.DataFrame):
    """Render interactive data table with modern styling."""
    with st.container(border=True):
        table_header = st.columns([3, 1])
        with table_header[0]:
            st.subheader("📋 Cost Details")
        with table_header[1]:
            export_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export CSV",
                data=export_data,
                file_name=f"cost_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        # Aggregated view
        agg_df = (
            df.groupby(["Service", "Region", "Usage Type"])
            .agg(
                {
                    "Unblended Cost": "sum",
                    "Usage Quantity": "sum",
                    "Date": "count",
                }
            )
            .reset_index()
            .rename(columns={"Date": "Records"})
        )
        agg_df["Avg Cost/Record"] = agg_df["Unblended Cost"] / agg_df["Records"]

        # Modern dataframe with column config
        st.dataframe(
            agg_df,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config={
                "Service": st.column_config.TextColumn("Service", width="medium"),
                "Region": st.column_config.TextColumn("Region", width="small"),
                "Usage Type": st.column_config.TextColumn("Type", width="small"),
                "Unblended Cost": st.column_config.NumberColumn(
                    "Total Cost",
                    format="$%.2f",
                    width="small",
                ),
                "Usage Quantity": st.column_config.NumberColumn(
                    "Usage",
                    format="%.1f",
                    width="small",
                ),
                "Records": st.column_config.NumberColumn(
                    "Records",
                    format="%d",
                    width="small",
                ),
                "Avg Cost/Record": st.column_config.NumberColumn(
                    "Avg Cost",
                    format="$%.2f",
                    width="small",
                ),
            },
            column_order=[
                "Service",
                "Region",
                "Usage Type",
                "Unblended Cost",
                "Usage Quantity",
                "Records",
                "Avg Cost/Record",
            ],
        )


def _render_admin_section(df: pd.DataFrame):
    """Render admin-only detailed analysis section."""
    st.markdown("---")
    st.subheader("🔐 Admin Analytics")
    st.caption("Detailed breakdowns available only to administrators")

    admin_cols = st.columns(2)

    with admin_cols[0]:
        with st.container(border=True):
            st.markdown("#### Regional Heatmap")
            pivot_df = df.pivot_table(
                values="Unblended Cost",
                index="Service",
                columns="Region",
                aggfunc="sum",
            ).fillna(0)

            fig_heatmap = px.imshow(
                pivot_df,
                color_continuous_scale="RdYlGn_r",
                aspect="auto",
                labels=dict(color="Cost ($)"),
            )
            fig_heatmap.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=300,
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

    with admin_cols[1]:
        with st.container(border=True):
            st.markdown("#### Cost Hierarchy")
            fig_sunburst = px.sunburst(
                df,
                path=["Region", "Service", "Usage Type"],
                values="Unblended Cost",
                color="Unblended Cost",
                color_continuous_scale="Viridis",
            )
            fig_sunburst.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=300,
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)

    # Top cost drivers table
    with st.container(border=True):
        st.markdown("#### 🔝 Top Cost Drivers")
        top_costs = (
            df.groupby(["Service", "Region"])["Unblended Cost"]
            .sum()
            .reset_index()
            .sort_values("Unblended Cost", ascending=False)
            .head(10)
        )
        top_costs["% of Total"] = (
            top_costs["Unblended Cost"] / top_costs["Unblended Cost"].sum() * 100
        )

        st.dataframe(
            top_costs,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Service": st.column_config.TextColumn("Service"),
                "Region": st.column_config.TextColumn("Region"),
                "Unblended Cost": st.column_config.NumberColumn("Cost", format="$%.2f"),
                "% of Total": st.column_config.ProgressColumn(
                    "Share",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
            },
        )
