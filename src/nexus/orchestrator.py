import time
import random
from typing import Generator, Tuple
from src.nexus.protocol import NexusState
import streamlit as st


class NexusOrchestrator:
    """
    AI Agent that controls the UI Layout.
    Simulates parsing user intent and modifying NexusState.
    """

    def __init__(self, nexus_state: NexusState):
        self.state = nexus_state
        self.knowledge_base = {
            "ec2": "I've added a cost chart for EC2.",
            "s3": "Here is the S3 usage breakdown.",
            "forecast": "Projecting next month's spend.",
            "anomaly": "Monitoring for live anomalies.",
        }

    def process_query(self, query: str) -> Generator[Tuple[str, str], None, None]:
        """
        Processes a prompt and potentially mutates the UI state.
        Yields (status, message).
        """
        query = query.lower()

        # 1. Thinking
        yield ("thinking", "Parsing intent...")
        time.sleep(0.5)

        # 2. Action Determination (Simulated)
        if "ec2" in query:
            yield ("thinking", "Detected Service: EC2")
            self.state.add_card(
                "cost-chart",
                "EC2 Cost Trend",
                {"filter_service": "EC2", "days": 30},
                width=2,
            )
            response = "I've simulated adding an EC2 Cost Chart to your dashboard."

        elif "anomaly" in query or "alert" in query:
            yield ("thinking", "Scanning for anomalies...")
            self.state.add_card("anomaly-feed", "Live Anomalies", width=1)
            response = "I've activated the Live Anomaly Feed."

        elif "reset" in query or "clear" in query:
            yield ("thinking", "Clearing layout...")
            self.state.cards = []
            response = "Dashboard cleared."

        else:
            response = (
                "I can modify the dashboard. Try asking for 'EC2 costs' or 'Anomalies'."
            )

        # 3. Final Response
        yield ("thinking_complete", "Done")

        words = response.split()
        for i, word in enumerate(words):
            yield ("response", word + " ")
            time.sleep(0.02)
