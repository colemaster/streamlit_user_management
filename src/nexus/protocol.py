from typing import List, Optional, Dict, Any, Literal
from dataclasses import dataclass, field
import uuid


@dataclass
class NexusCardState:
    """Represents the state of a single card on the dashboard."""

    id: str
    type: str  # Maps to a registry key
    title: str
    data: Dict[str, Any] = field(default_factory=dict)
    layout: Dict[str, int] = field(
        default_factory=lambda: {"w": 1, "h": 1}
    )  # Grid units


@dataclass
class NexusState:
    """Global state of the Nexus engine (Agentic UI)."""

    cards: List[NexusCardState] = field(default_factory=list)

    def add_card(self, card_type: str, title: str, data: Dict = None, width: int = 1):
        new_card = NexusCardState(
            id=str(uuid.uuid4())[:8],
            type=card_type,
            title=title,
            data=data or {},
            layout={"w": width, "h": 1},
        )
        self.cards.insert(0, new_card)  # Add to top
        return new_card

    def remove_card(self, card_id: str):
        self.cards = [c for c in self.cards if c.id != card_id]

    def update_card(self, card_id: str, data_update: Dict):
        for card in self.cards:
            if card.id == card_id:
                card.data.update(data_update)
                return True
        return False
