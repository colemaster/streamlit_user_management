import time
import random


class FinOpsEngine:
    """
    Simulates an intelligent FinOps AI engine.

    In a production environment, this would:
    1. Use an LLM (e.g., GPT-4, Claude) to understand natural language.
    2. Query real cloud APIs (AWS Cost Explorer, Azure Cost Management).
    3. Use RAG (Retrieval Augmented Generation) to fetch documentation.

    Currently, it mocks this behavior for demonstration purposes.
    """

    def __init__(self):
        # Knowledge base mimics a vector database search result
        self.knowledge_base = {
            "cost": "Your current month-to-date cost is **$12,450**, which is 15% higher than last month.",
            "ec2": "You have 45 running EC2 instances. 12 of them are idle and can be stopped to save **$450/month**.",
            "savings": "I recommend purchasing a Compute Savings Plan for 1 year. This could save you approximately **25%** on compute costs.",
            "budget": "You have exceeded your 'Dev-Team' budget by **$200** this week due to increased S3 usage.",
        }

    def generate_response(self, user_query):
        """
        Generates a streaming response with a 'thinking' process.

        This simulates the latency and steps of a real AI agent.

        Yields: (status_type, content)
        status_type: 'thinking' | 'response'
        """
        user_query = user_query.lower()

        start_time = time.time()

        # 1. Simulate Thinking (AI Reasoning Steps)
        thoughts = [
            "Analyzing user intent...",
            "Querying Cost Explorer API...",
            "Aggregating resource usage metrics...",
            "Checking anomaly detection models...",
            "Formulating recommendations...",
        ]

        for thought in thoughts:
            # Simulate network/processing latency
            time.sleep(random.uniform(0.05, 0.1))
            yield ("thinking", thought)

        # 2. Determine Response (Simple Keyword Matching)
        response_text = "I'm not sure about that specific FinOps detail yet. Try asking about costs, EC2, savings, or budgets."

        for key, value in self.knowledge_base.items():
            if key in user_query:
                response_text = value
                break

        # 3. Stream Response (Token-by-token simulation)
        yield ("thinking_complete", "Analysis Complete")

        words = response_text.split()
        for i, word in enumerate(words):
            chunk = word + " "
            # Simulate token generation speed
            time.sleep(random.uniform(0.005, 0.01))
            yield ("response", chunk)

        # 4. Yield Metrics
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        input_tokens = len(user_query.split()) * 1.3  # Approx estimation
        output_tokens = len(words) * 1.3  # Approx estimation

        yield (
            "metrics",
            {
                "latency_ms": round(latency_ms, 2),
                "input_tokens": int(input_tokens),
                "output_tokens": int(output_tokens),
                "total_tokens": int(input_tokens + output_tokens),
            },
        )
