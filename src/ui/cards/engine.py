from typing import Callable, Dict, Any
import streamlit as st
from src.nexus.protocol import NexusCardState

# Registry of Card Renderers
# Signature: (card_state: NexusCardState) -> None
_CARD_REGISTRY: Dict[str, Callable] = {}


def register_card(name: str):
    """Decorator to register a UI component as a Nexus Card."""

    def decorator(func):
        _CARD_REGISTRY[name] = func
        return func

    return decorator


def get_renderer(card_type: str) -> Callable:
    return _CARD_REGISTRY.get(card_type)


def render_card(card: NexusCardState):
    """Renders a card by looking up its type in the registry."""
    renderer = get_renderer(card.type)
    if not renderer:
        st.error(f"Unknown Card Type: {card.type}")
        return

    # Wrap in a container/frame
    with st.container():
        # Using st.fragment for independent updates if desired,
        # but the renderer itself can also be fragmented.
        renderer(card)
