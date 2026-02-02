import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import streamlit as st


@st.cache_data(scope="session", ttl=3600, show_spinner="Generating mock data...")
def generate_mock_data(days=30):
    """
    Generates mock AWS cost data with session-scoped caching.
    
    Uses Streamlit nightly 2026 session-scoped caching for improved performance.
    Data is cached per session and automatically expires after 1 hour.
    """
    dates = [datetime.today() - timedelta(days=x) for x in range(days)]
    services = [
        "Amazon EC2",
        "Amazon S3",
        "Amazon RDS",
        "AWS Lambda",
        "Amazon CloudFront",
    ]
    regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-2"]
    usage_types = ["Compute", "Storage", "Data Transfer", "API Requests"]

    data = []

    for date in dates:
        for service in services:
            for region in regions:
                # Randomize cost and usage
                cost = np.random.uniform(10, 500)
                if service == "Amazon EC2":
                    cost *= 2.5  # EC2 is expensive
                elif service == "AWS Lambda":
                    cost *= 0.1  # Lambda is cheap

                usage = cost * np.random.uniform(0.8, 1.2)

                # Add some anomalies
                if np.random.random() > 0.95:
                    cost *= 3

                data.append(
                    {
                        "Date": date,
                        "Service": service,
                        "Region": region,
                        "Usage Type": np.random.choice(usage_types),
                        "Unblended Cost": round(cost, 2),
                        "Usage Quantity": round(usage, 2),
                    }
                )

    return pd.DataFrame(data)


@st.cache_data(scope="session", ttl=1800, show_spinner="Loading cost trends...")
def get_cost_trends(service_filter: str = "All", days: int = 30) -> pd.DataFrame:
    """
    Get cost trends data with session-scoped caching.
    
    Args:
        service_filter: Filter by service name
        days: Number of days to include
        
    Returns:
        DataFrame with cost trend data
    """
    # Generate trend data based on the base mock data
    base_data = generate_mock_data(days)
    
    if service_filter != "All":
        base_data = base_data[base_data["Service"] == service_filter]
    
    # Aggregate by date
    daily_costs = base_data.groupby("Date")["Unblended Cost"].sum().reset_index()
    daily_costs = daily_costs.sort_values("Date")
    
    # Add trend indicators
    daily_costs["7_day_avg"] = daily_costs["Unblended Cost"].rolling(window=7, min_periods=1).mean()
    daily_costs["trend"] = daily_costs["Unblended Cost"].pct_change()
    
    return daily_costs


@st.cache_data(scope="session", ttl=2400, show_spinner="Analyzing anomalies...")
def detect_cost_anomalies(threshold: float = 2.0) -> pd.DataFrame:
    """
    Detect cost anomalies with session-scoped caching.
    
    Args:
        threshold: Standard deviation threshold for anomaly detection
        
    Returns:
        DataFrame with detected anomalies
    """
    data = generate_mock_data()
    
    # Calculate anomalies by service and region
    anomalies = []
    
    for service in data["Service"].unique():
        for region in data["Region"].unique():
            service_data = data[
                (data["Service"] == service) & (data["Region"] == region)
            ]
            
            if len(service_data) > 5:  # Need enough data points
                mean_cost = service_data["Unblended Cost"].mean()
                std_cost = service_data["Unblended Cost"].std()
                
                # Find anomalies
                anomaly_mask = (
                    service_data["Unblended Cost"] > mean_cost + threshold * std_cost
                )
                
                service_anomalies = service_data[anomaly_mask]
                
                for _, row in service_anomalies.iterrows():
                    anomalies.append({
                        "Date": row["Date"],
                        "Service": row["Service"],
                        "Region": row["Region"],
                        "Cost": row["Unblended Cost"],
                        "Expected_Cost": mean_cost,
                        "Deviation": (row["Unblended Cost"] - mean_cost) / std_cost,
                        "Severity": "High" if (row["Unblended Cost"] - mean_cost) / std_cost > 3 else "Medium"
                    })
    
    return pd.DataFrame(anomalies)


@st.cache_data(scope="session", ttl=3600, show_spinner="Loading service breakdown...")
def get_service_breakdown(days: int = 30) -> pd.DataFrame:
    """
    Get service cost breakdown with session-scoped caching.
    
    Args:
        days: Number of days to analyze
        
    Returns:
        DataFrame with service breakdown
    """
    data = generate_mock_data(days)
    
    # Aggregate by service
    service_breakdown = data.groupby("Service").agg({
        "Unblended Cost": ["sum", "mean", "count"],
        "Usage Quantity": "sum"
    }).round(2)
    
    # Flatten column names
    service_breakdown.columns = [
        "Total_Cost", "Avg_Daily_Cost", "Usage_Days", "Total_Usage"
    ]
    
    # Calculate percentages
    total_cost = service_breakdown["Total_Cost"].sum()
    service_breakdown["Cost_Percentage"] = (
        service_breakdown["Total_Cost"] / total_cost * 100
    ).round(1)
    
    return service_breakdown.reset_index()


# Cache management functions
def clear_data_cache():
    """Clear all data-related caches."""
    functions_to_clear = [
        generate_mock_data,
        get_cost_trends,
        detect_cost_anomalies,
        get_service_breakdown
    ]
    
    for func in functions_to_clear:
        func.clear()


def refresh_all_data():
    """Refresh all cached data."""
    clear_data_cache()
    
    # Pre-load fresh data
    generate_mock_data()
    get_cost_trends()
    detect_cost_anomalies()
    get_service_breakdown()
