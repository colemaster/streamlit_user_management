import time
import random

class FinOpsEngine:
    def __init__(self):
        self.knowledge_base = {
            "cost": "Your current month-to-date cost is **$12,450**, which is 15% higher than last month.",
            "ec2": "You have 45 running EC2 instances. 12 of them are idle and can be stopped to save **$450/month**.",
            "savings": "I recommend purchasing a Compute Savings Plan for 1 year. This could save you approximately **25%** on compute costs.",
            "budget": "You have exceeded your 'Dev-Team' budget by **$200** this week due to increased S3 usage."
        }

    def generate_response(self, user_query):
        """
        Generates a streaming response with a 'thinking' process.
        Yields: (status_type, content)
        status_type: 'thinking' | 'response'
        """
        user_query = user_query.lower()
        
        # 1. Simulate Thinking
        thoughts = [
            "Analyzing user intent...",
            "Querying Cost Explorer API...",
            "Aggregating resource usage metrics...",
            "Checking anomaly detection models...",
            "Formulating recommendations..."
        ]
        
        for thought in thoughts:
            time.sleep(random.uniform(0.05, 0.1))
            yield ("thinking", thought)
            
        # 2. Determine Response
        response_text = "I'm not sure about that specific FinOps detail yet. Try asking about costs, EC2, savings, or budgets."
        
        for key, value in self.knowledge_base.items():
            if key in user_query:
                response_text = value
                break
        
        # 3. Stream Response
        yield ("thinking_complete", "Analysis Complete")
        
        words = response_text.split()
        for i, word in enumerate(words):
            chunk = word + " "
            time.sleep(random.uniform(0.005, 0.01))
            yield ("response", chunk)
