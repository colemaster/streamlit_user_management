"""
Modern FinOps Dashboard - Streamlit 1.52+
"""

import streamlit as st
import plotly.graph_objects as go

from src.auth.permissions import get_current_permission, has_permission, PermissionLevel
from src.nexus.protocol import NexusState
from src.nexus.orchestrator import NexusOrchestrator
from src.ui.cards.engine import render_card
from src.ui.components import animated_header
import src.ui.cards.impl  # Register cards


def render_dashboard():
    """
    The Nexus Canvas.
    Renders the UI based dynamically on state controlled by the AI Orchestrator.
    """
    current_permission = get_current_permission()
    if not current_permission or not has_permission(PermissionLevel.ANALYST):
        st.error("🔒 Access Denied: Requires ANALYST permission level.")
        return

    # 1. Header Section
    animated_header("NEXUS COMMAND", "AI-Driven Interface")

    # 2. Initialize Nexus State (The "Truth")
    if "nexus_state" not in st.session_state:
        state = NexusState()
        # Initial Default Layout
        state.add_card(
            "metric-card",
            "Total Spend",
            {"value": "$45k", "delta": "+12%", "color": "error"},
            width=1,
        )
        state.add_card(
            "metric-card",
            "Forecast",
            {"value": "$52k", "delta": "+8%", "color": "neutral"},
            width=1,
        )
        state.add_card(
            "cost-chart", "Monthly Trend", {"filter_service": "All"}, width=2
        )
        st.session_state.nexus_state = state

    nexus_state = st.session_state.nexus_state

    # 2. Initialize Orchestrator
    if "nexus_orch" not in st.session_state:
        st.session_state.nexus_orch = NexusOrchestrator(nexus_state)

    orch = st.session_state.nexus_orch

    # 3. Canvas Controls (The "Chat with Dashboard" Interface)
    st.markdown('<div class="brave-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        prompt = st.chat_input(
            "Command the Nexus (e.g., 'Add EC2 chart', 'Show Anomalies')"
        )
    with col2:
        if st.button("RESET VIEW", use_container_width=True):
            nexus_state.cards = []
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if prompt:
        with st.status("Nexus AI Processing...", expanded=True) as status:
            for s_type, msg in orch.process_query(prompt):
                if s_type == "thinking":
                    st.write(f"🧠 {msg}")
                elif s_type == "response":
                    # Just accumulating response for now, usually shown in chat
                    pass
            status.update(label="Layout Updated", state="complete", expanded=False)
        st.rerun()

    st.divider()

    # 4. Render the Grid
    # Simple Masonry-like grid for v1
    # We iterate cards and pack them into columns

    if not nexus_state.cards:
        st.info("Canvas is empty. Ask the AI to 'Show me costs'.")
        return

    # Create 2 main columns for layout
    left_col, right_col = st.columns([2, 2])
    cols = [left_col, right_col]

    for i, card in enumerate(nexus_state.cards):
        # Determine column based on index (simple alternation)
        target_col = cols[i % 2]

        with target_col:
            render_card(card)
