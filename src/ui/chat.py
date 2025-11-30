import streamlit as st
from src.finops.engine import FinOpsEngine
from src.auth.permissions import has_permission, get_current_permission
from src.auth.config import PermissionLevel


def render_chat():
    """Render the chat interface with permission checks."""

    # Check if user has at least VIEWER permission to access chat
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
        st.markdown(
            "Please contact your administrator if you believe this is an error."
        )
        return

    # Initialize Engine
    if "engine" not in st.session_state:
        st.session_state.engine = FinOpsEngine()

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Main Chat Container
    chat_container = st.container()

    with chat_container:
        # Display Chat History
        for message in st.session_state.messages:
            avatar = (
                "🧑‍💼" if message["role"] == "user" else "🟧"
            )  # Professional avatars
            with st.chat_message(message["role"], avatar=avatar):
                if message.get("thought_process"):
                    with st.status(
                        "Thinking Process", state="complete", expanded=False
                    ):
                        st.write(message["thought_process"])
                st.markdown(message["content"])

    # Handle User Input
    if prompt := st.chat_input("Ask about your cloud costs..."):
        # 1. Display User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user", avatar="🧑‍💼"):
                st.markdown(prompt)

            # 2. Generate Assistant Response
            with st.chat_message("assistant", avatar="🟧"):
                # Thinking UI Container
                status_container = st.status("Thinking...", expanded=True)
                thought_process_text = ""

                # Response Container
                response_placeholder = st.empty()
                full_response = ""

                # Stream from Engine
                for msg_type, content in st.session_state.engine.generate_response(
                    prompt
                ):
                    if msg_type == "thinking":
                        status_container.write(content)
                        thought_process_text += f"- {content}\n"
                    elif msg_type == "thinking_complete":
                        status_container.update(
                            label="Thinking Complete", state="complete", expanded=False
                        )
                    elif msg_type == "response":
                        full_response += content
                        response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)

                # 3. Save Assistant Message
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": full_response,
                        "thought_process": thought_process_text,
                    }
                )

                # Feedback (New in Streamlit 1.47+)
                st.feedback("thumbs")
