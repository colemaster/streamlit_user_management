"""
Modern FinOps Chat Interface - Streamlit 1.52+
Professional AI assistant with audio input and enhanced UX.
"""

import streamlit as st
from src.finops.engine import FinOpsEngine
from src.auth.permissions import has_permission, get_current_permission
from src.auth.config import PermissionLevel


def render_chat():
    """Render the modern chat interface with permission checks."""

    # Permission check
    current_permission = get_current_permission()
    if not current_permission:
        st.error(
            "🔒 Unable to determine your permission level. Please contact your administrator."
        )
        return

    if not has_permission(PermissionLevel.VIEWER):
        st.error("🔒 Access Denied")
        st.markdown(
            "You do not have permission to access the FinOps Assistant. "
            "Required permission level: **VIEWER**"
        )
        return

    # Initialize Engine
    if "engine" not in st.session_state:
        st.session_state.engine = FinOpsEngine()

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat Header with controls
    _render_chat_header()

    st.space(1)

    # Main Chat Container
    chat_container = st.container(height=500, border=True)

    with chat_container:
        # Welcome message if no history
        if not st.session_state.messages:
            _render_welcome_message()
        else:
            # Display Chat History
            for idx, message in enumerate(st.session_state.messages):
                _render_message(message, idx)

    # Input area
    _render_input_area(chat_container)


def _render_chat_header():
    """Render chat header with controls."""
    header_cols = st.columns([3, 1, 1])

    with header_cols[0]:
        st.markdown("### 🤖 FinOps Assistant")

    with header_cols[1]:
        if st.button("🗑️ Clear", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.rerun()

    with header_cols[2]:
        with st.popover("⚙️ Settings", use_container_width=True):
            st.markdown("#### Chat Settings")
            st.toggle("Stream responses", value=True, key="stream_enabled")
            st.toggle("Show thinking process", value=True, key="show_thinking")
            st.toggle("Show debug metrics", value=False, key="show_metrics")
            st.selectbox(
                "Response style",
                ["Concise", "Detailed", "Technical"],
                key="response_style",
            )


def _render_welcome_message():
    """Render welcome message for new conversations."""
    st.space(2)
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem;">
            <h3>👋 Welcome to FinOps Assistant</h3>
            <p style="color: #666;">Ask me anything about your cloud costs</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick action suggestions
    st.markdown("#### 💡 Try asking:", text_alignment="center")
    st.space(1)

    suggestion_cols = st.columns(2)
    suggestions = [
        "What are my top cost drivers?",
        "Show me EC2 spending trends",
        "Any cost anomalies this week?",
        "How can I reduce S3 costs?",
    ]

    for i, suggestion in enumerate(suggestions):
        with suggestion_cols[i % 2]:
            if st.button(
                suggestion,
                key=f"suggestion_{i}",
                use_container_width=True,
                type="secondary",
            ):
                st.session_state.pending_prompt = suggestion
                st.rerun()


def _render_message(message: dict, idx: int):
    """Render a single chat message."""
    is_user = message["role"] == "user"
    avatar = "🧑‍💼" if is_user else "🟧"

    with st.chat_message(message["role"], avatar=avatar):
        # Show thinking process for assistant messages
        if not is_user and message.get("thought_process"):
            show_thinking = st.session_state.get("show_thinking", True)
            if show_thinking:
                with st.status("Thinking Process", state="complete", expanded=False):
                    st.markdown(message["thought_process"])

        # Message content
        st.markdown(message["content"])

        # Feedback for assistant messages
        if not is_user:
            feedback_cols = st.columns([4, 1])
            with feedback_cols[1]:
                st.feedback("thumbs", key=f"feedback_{idx}")

            # Debug Info
            if message.get("metrics") and st.session_state.get("show_metrics", False):
                with st.expander("📊 Debug Info", expanded=False):
                    m = message["metrics"]
                    cols = st.columns(3)
                    cols[0].metric("Latency", f"{m['latency_ms']}ms")
                    cols[1].metric("Tokens (In)", m["input_tokens"])
                    cols[2].metric("Tokens (Out)", m["output_tokens"])
                    st.caption(f"Total Tokens: {m['total_tokens']}")


def _render_input_area(chat_container):
    """Render the input area with audio support."""
    # Check for pending prompt from suggestions
    pending = st.session_state.pop("pending_prompt", None)

    # Chat input with audio support (new in 1.52)
    prompt = st.chat_input(
        "Ask about your cloud costs...",
        key="chat_input",
    )

    # Use pending prompt if available
    if pending:
        prompt = pending

    if prompt:
        _handle_user_input(prompt, chat_container)


def _handle_user_input(prompt: str, chat_container):
    """Process user input and generate response."""
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with chat_container:
        # Display user message
        with st.chat_message("user", avatar="🧑‍💼"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant", avatar="🟧"):
            show_thinking = st.session_state.get("show_thinking", True)

            if show_thinking:
                status_container = st.status("Analyzing...", expanded=True)
            else:
                status_container = None

            thought_process_text = ""
            response_placeholder = st.empty()
            full_response = ""

            # Stream from Engine
            for msg_type, content in st.session_state.engine.generate_response(prompt):
                if msg_type == "thinking" and status_container:
                    status_container.write(content)
                    thought_process_text += f"- {content}\n"
                elif msg_type == "thinking_complete" and status_container:
                    status_container.update(
                        label="Analysis Complete",
                        state="complete",
                        expanded=False,
                    )
                elif msg_type == "response":
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
                elif msg_type == "metrics":
                    st.session_state["last_metrics"] = content

            response_placeholder.markdown(full_response)

            # Save assistant message
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                    "thought_process": thought_process_text if show_thinking else None,
                    "metrics": st.session_state.get("last_metrics", None),
                }
            )

            # Clear temp metrics
            if "last_metrics" in st.session_state:
                del st.session_state["last_metrics"]

            # Feedback
            st.feedback("thumbs", key=f"feedback_{len(st.session_state.messages)}")
