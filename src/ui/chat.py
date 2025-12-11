"""
Modern FinOps Chat Interface - Streamlit 1.52+
"""

import streamlit as st
from src.finops.engine import FinOpsEngine
from src.auth.permissions import has_permission, get_current_permission
from src.auth.config import PermissionLevel
from src.ui.components import animated_header


@st.fragment
def render_chat():
    """Render the modern chat interface."""
    current_permission = get_current_permission()

    if not current_permission or not has_permission(PermissionLevel.VIEWER):
        st.error("🔒 Access Denied: Requires VIEWER permission level.")
        return

    # Initialize Engine
    if "engine" not in st.session_state:
        st.session_state.engine = FinOpsEngine()

    # Initialize History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Layout
    col1, col2 = st.columns([3, 1])
    with col1:
        animated_header("FinOps Assistant", " AI-powered cost optimization expert")

    with col2:
        with st.popover("⚙️ Settings", use_container_width=True):
            st.caption("Assistant Configuration")
            show_thought = st.toggle("Show Reasoning", value=True)
            st.toggle("Stream Responses", value=True)
            if st.button("🗑️ Clear History", type="primary", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    # Chat Container
    chat_container = st.container(height=600, border=False)

    # Custom CSS for chat bubbles (Scoped here for specific override if needed, though general is in styles.py)
    st.markdown(
        """
    <style>
    .user-bubble {
        background-color: #2A3036;
        color: #EDEDED;
        padding: 12px 16px;
        border-radius: 12px 12px 0 12px;
        margin-bottom: 8px;
        display: inline-block;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .bot-bubble {
        background: linear-gradient(135deg, #FF5500 0%, #E04000 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 12px 12px 12px 0;
        margin-bottom: 8px;
        display: inline-block;
        max-width: 80%;
        float: left;
        clear: both;
        box-shadow: 0 4px 12px rgba(255, 85, 0, 0.3);
    }
    .thought-bubble {
        background-color: #14181C;
        border-left: 3px solid #FF5500;
        color: #A0A5AA;
        padding: 8px 12px;
        font-family: monospace;
        font-size: 0.85rem;
        margin-bottom: 8px;
        clear: both;
        margin-left: 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with chat_container:
        if not st.session_state.messages:
            _render_empty_state()

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="user-bubble">{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                if msg.get("thought") and show_thought:
                    with st.expander("💭 Reasoning Process", expanded=False):
                        st.markdown(f"```text\n{msg['thought']}\n```")
                st.markdown(
                    f'<div class="bot-bubble">{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div style="clear: both;"></div>', unsafe_allow_html=True
                )  # Clear float

    # Input Area
    prompt = st.chat_input("Ask about your AWS/Azure spend...", key="chat_input")

    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.markdown(
                f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True
            )

        # Generate response
        response_placeholder = st.empty()
        thought_placeholder = st.empty()

        full_response = ""
        full_thought = ""

        # Fake streaming visualization since the engine generator yields chunks
        # Adapt this loop based on actual engine.py yield structure
        for msg_type, content in st.session_state.engine.generate_response(prompt):
            if msg_type == "thinking":
                full_thought += content + "\n"
                if show_thought:
                    thought_placeholder.markdown(
                        f'<div class="thought-bubble">Thinking... {len(full_thought)} chars</div>',
                        unsafe_allow_html=True,
                    )
            elif msg_type == "response":
                full_response += content
                response_placeholder.markdown(
                    f'<div class="bot-bubble">{full_response}▌</div>',
                    unsafe_allow_html=True,
                )

        # Finalize
        if show_thought:
            thought_placeholder.empty()  # Clear the temp thinking bubble

        response_placeholder.markdown(
            f'<div class="bot-bubble">{full_response}</div>', unsafe_allow_html=True
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response, "thought": full_thought}
        )
        st.rerun()


def _render_empty_state():
    st.markdown(
        """
    <div style="text-align: center; margin-top: 4rem; opacity: 0.7;">
        <h1>👋</h1>
        <h3>How can I help optimize your cloud costs?</h3>
        <p>Try asking about <b>EC2 trends</b>, <b>anomaly detection</b>, or <b>budget forecasts</b>.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
