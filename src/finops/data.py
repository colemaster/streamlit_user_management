import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data(days=30):
    """Generates mock AWS cost data."""
    dates = [datetime.today() - timedelta(days=x) for x in range(days)]
    services = ['Amazon EC2', 'Amazon S3', 'Amazon RDS', 'AWS Lambda', 'Amazon CloudFront']
    regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-2']
    usage_types = ['Compute', 'Storage', 'Data Transfer', 'API Requests']
    
    data = []
    
    for date in dates:
        for service in services:
            for region in regions:
                # Randomize cost and usage
                cost = np.random.uniform(10, 500)
                if service == 'Amazon EC2':
                    cost *= 2.5 # EC2 is expensive
                elif service == 'AWS Lambda':
                    cost *= 0.1 # Lambda is cheap
                
                usage = cost * np.random.uniform(0.8, 1.2)
                
                # Add some anomalies
                if np.random.random() > 0.95:
                    cost *= 3
                
                data.append({
                    'Date': date,
                    'Service': service,
                    'Region': region,
                    'Usage Type': np.random.choice(usage_types),
                    'Unblended Cost': round(cost, 2),
                    'Usage Quantity': round(usage, 2)
                })
                
    return pd.DataFrame(data)
