import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.finops.data import generate_mock_data
from src.auth.permissions import has_permission, get_current_permission
from src.auth.config import PermissionLevel


def render_dashboard():
    """Render the dashboard with permission checks."""

    # Check if user has at least ANALYST permission to access detailed dashboard
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
        st.markdown(
            "Please contact your administrator if you believe this is an error."
        )
        return

    st.markdown("## 📊 Cloud Cost Overview")
    st.space(1)  # New in 1.51

    # Load Data
    if "cost_data" not in st.session_state:
        st.session_state.cost_data = generate_mock_data()

    df = st.session_state.cost_data

    # Filters using st.pills (New in 1.40+)
    selected_service = st.pills(
        "Filter by Service",
        options=["All"] + list(df["Service"].unique()),
        default="All",
        selection_mode="single",
    )

    if selected_service and selected_service != "All":
        df = df[df["Service"] == selected_service]

    st.space(2)

    # Top Level KPIs
    total_cost = df["Unblended Cost"].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric("Total Cost (MTD)", f"${total_cost:,.2f}", "15.2%")

    with col2:
        with st.container(border=True):
            st.metric("Forecast", f"${total_cost * 1.2:,.2f}", "5%")

    with col3:
        with st.container(border=True):
            st.metric("Active Services", f"{df['Service'].nunique()}")

    with col4:
        with st.container(border=True):
            # Popover for details (New in 1.29+)
            with st.popover("Anomalies Detected", use_container_width=True):
                st.markdown("### 🚨 Recent Anomalies")
                st.warning("Spike in EC2 usage on Nov 28")
                st.info("Unusual S3 data transfer on Nov 27")
                st.caption("Threshold: > 20% daily deviation")
            st.metric("Anomalies", "3", "-1", delta_color="inverse")

    st.space(3)

    # Row 1: Trend & Breakdown
    c1, c2 = st.columns([2, 1])

    with c1:
        with st.container(border=True):
            st.subheader("Daily Cost Trend")
            daily_cost = df.groupby("Date")["Unblended Cost"].sum().reset_index()
            fig_trend = px.bar(
                daily_cost,
                x="Date",
                y="Unblended Cost",
                color="Unblended Cost",
                color_continuous_scale="Viridis",
            )
            fig_trend.update_layout(
                xaxis_title=None,
                yaxis_title=None,
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0),
            )
            st.plotly_chart(
                fig_trend,
                use_container_width=True,
                key="trend_chart",
                on_select="ignore",
            )  # on_select new in 1.35+

    with c2:
        with st.container(border=True):
            st.subheader("Service Breakdown")
            service_cost = df.groupby("Service")["Unblended Cost"].sum().reset_index()
            fig_pie = px.pie(
                service_cost, values="Unblended Cost", names="Service", hole=0.4
            )
            fig_pie.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_pie, use_container_width=True)

    st.space(2)

    # Row 2: Detailed Analysis (Admin only)
    if has_permission(PermissionLevel.ADMIN):
        with st.container(border=True):
            st.subheader("Cost by Region & Usage Type (Admin View)")
            fig_sunburst = px.sunburst(
                df,
                path=["Region", "Service", "Usage Type"],
                values="Unblended Cost",
                color="Unblended Cost",
                color_continuous_scale="RdBu",
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.info("ℹ️ Additional detailed analysis is available for administrators.")
