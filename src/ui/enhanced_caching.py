"""
Enhanced Caching System for Streamlit Nightly 2026.

Implements session-scoped caching using @st.cache_data(scope="session")
for improved performance and user experience.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Callable
import hashlib
import json
from functools import wraps


class SessionCacheManager:
    """
    Manager for session-scoped caching with advanced features.
    
    Provides utilities for managing cached data with session scope,
    cache invalidation, and performance monitoring.
    """
    
    @staticmethod
    def get_cache_stats() -> Dict[str, Any]:
        """Get statistics about current cache usage."""
        cache_keys = [key for key in st.session_state.keys() if key.startswith('_cache_')]
        
        total_size = 0
        cache_info = {}
        
        for key in cache_keys:
            try:
                data = st.session_state[key]
                # Estimate size (rough approximation)
                size = len(str(data))
                total_size += size
                cache_info[key] = {
                    'size_estimate': size,
                    'type': type(data).__name__,
                    'created': getattr(data, '_cache_created', 'unknown')
                }
            except Exception:
                cache_info[key] = {'error': 'Unable to analyze'}
        
        return {
            'total_cached_items': len(cache_keys),
            'estimated_total_size': total_size,
            'cache_details': cache_info
        }
    
    @staticmethod
    def clear_session_cache(pattern: Optional[str] = None) -> int:
        """
        Clear cached items from session state.
        
        Args:
            pattern: Optional pattern to match cache keys
            
        Returns:
            Number of items cleared
        """
        cache_keys = [key for key in st.session_state.keys() if key.startswith('_cache_')]
        
        if pattern:
            cache_keys = [key for key in cache_keys if pattern in key]
        
        cleared_count = 0
        for key in cache_keys:
            if key in st.session_state:
                del st.session_state[key]
                cleared_count += 1
        
        return cleared_count
    
    @staticmethod
    def cache_key_from_args(*args, **kwargs) -> str:
        """Generate a cache key from function arguments."""
        # Create a deterministic hash from arguments
        key_data = {
            'args': args,
            'kwargs': kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()


# Enhanced caching decorators
def session_cached_data(
    ttl: Optional[int] = None,
    max_entries: Optional[int] = None,
    show_spinner: bool = True,
    persist: str = "disk"
):
    """
    Enhanced session-scoped data caching decorator.
    
    Args:
        ttl: Time to live in seconds (None for session lifetime)
        max_entries: Maximum number of cached entries
        show_spinner: Show loading spinner
        persist: Persistence mode ("disk", "memory")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"_cache_{func.__name__}_{SessionCacheManager.cache_key_from_args(*args, **kwargs)}"
            
            # Check if cached result exists and is valid
            if cache_key in st.session_state:
                cached_data = st.session_state[cache_key]
                
                # Check TTL if specified
                if ttl and 'timestamp' in cached_data:
                    age = (datetime.now() - cached_data['timestamp']).total_seconds()
                    if age > ttl:
                        del st.session_state[cache_key]
                    else:
                        return cached_data['result']
                else:
                    return cached_data['result']
            
            # Execute function with spinner if enabled
            if show_spinner:
                with st.spinner(f"Loading {func.__name__}..."):
                    result = func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Cache the result
            cache_data = {
                'result': result,
                'timestamp': datetime.now(),
                'function': func.__name__
            }
            
            st.session_state[cache_key] = cache_data
            
            return result
        
        return wrapper
    return decorator


def session_cached_resource(
    show_spinner: bool = True,
    validate: Optional[Callable] = None
):
    """
    Enhanced session-scoped resource caching decorator.
    
    Args:
        show_spinner: Show loading spinner
        validate: Optional validation function for cached resource
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"_resource_{func.__name__}_{SessionCacheManager.cache_key_from_args(*args, **kwargs)}"
            
            # Check if cached resource exists and is valid
            if cache_key in st.session_state:
                cached_resource = st.session_state[cache_key]
                
                # Validate resource if validator provided
                if validate and not validate(cached_resource):
                    del st.session_state[cache_key]
                else:
                    return cached_resource
            
            # Create resource with spinner if enabled
            if show_spinner:
                with st.spinner(f"Initializing {func.__name__}..."):
                    resource = func(*args, **kwargs)
            else:
                resource = func(*args, **kwargs)
            
            # Cache the resource
            st.session_state[cache_key] = resource
            
            return resource
        
        return wrapper
    return decorator


# Enhanced data loading functions with session-scoped caching
@st.cache_data(scope="session", ttl=3600, show_spinner="Loading financial data...")
def load_financial_data(days: int = 30, refresh: bool = False) -> pd.DataFrame:
    """
    Load financial data with session-scoped caching.
    
    Args:
        days: Number of days of data to load
        refresh: Force refresh of cached data
        
    Returns:
        DataFrame with financial data
    """
    if refresh:
        # Clear cache for this function
        st.cache_data.clear()
    
    # Generate mock financial data
    dates = pd.date_range(end=datetime.now(), periods=days)
    
    data = []
    for date in dates:
        # Generate realistic financial metrics
        revenue = np.random.normal(100000, 15000)
        costs = np.random.normal(75000, 10000)
        profit = revenue - costs
        
        # Add some seasonal trends
        day_of_year = date.dayofyear
        seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * day_of_year / 365)
        
        data.append({
            'date': date,
            'revenue': revenue * seasonal_factor,
            'costs': costs,
            'profit': profit * seasonal_factor,
            'margin': (profit / revenue) * 100 if revenue > 0 else 0
        })
    
    return pd.DataFrame(data)


@st.cache_data(scope="session", ttl=1800, show_spinner="Loading performance metrics...")
def load_performance_metrics(service: str = "all") -> Dict[str, Any]:
    """
    Load performance metrics with session-scoped caching.
    
    Args:
        service: Service to load metrics for
        
    Returns:
        Dictionary with performance metrics
    """
    # Simulate loading performance data
    services = ["ec2", "s3", "rds", "lambda"] if service == "all" else [service]
    
    metrics = {}
    for svc in services:
        # Generate realistic performance metrics
        response_times = np.random.exponential(0.1, 100)  # Response times in seconds
        throughput = np.random.poisson(1000, 100)  # Requests per second
        error_rate = np.random.beta(1, 99, 100) * 100  # Error percentage
        
        metrics[svc] = {
            'avg_response_time': np.mean(response_times),
            'p95_response_time': np.percentile(response_times, 95),
            'avg_throughput': np.mean(throughput),
            'error_rate': np.mean(error_rate),
            'uptime': np.random.uniform(99.5, 99.99),
            'last_updated': datetime.now()
        }
    
    return metrics


@st.cache_data(scope="session", ttl=7200, show_spinner="Processing analytics...")
def process_analytics_data(
    data_source: str,
    aggregation: str = "daily",
    filters: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    """
    Process analytics data with session-scoped caching.
    
    Args:
        data_source: Source of data to process
        aggregation: Aggregation level (daily, weekly, monthly)
        filters: Optional filters to apply
        
    Returns:
        Processed analytics DataFrame
    """
    # Simulate data processing
    if aggregation == "daily":
        periods = 30
        freq = "D"
    elif aggregation == "weekly":
        periods = 12
        freq = "W"
    else:  # monthly
        periods = 6
        freq = "M"
    
    dates = pd.date_range(end=datetime.now(), periods=periods, freq=freq)
    
    # Generate analytics data
    data = []
    for date in dates:
        # Simulate various metrics
        users = np.random.poisson(1000)
        sessions = np.random.poisson(1500)
        pageviews = np.random.poisson(5000)
        bounce_rate = np.random.beta(2, 8) * 100
        
        # Apply filters if provided
        if filters:
            if filters.get("min_users") and users < filters["min_users"]:
                continue
            if filters.get("max_bounce_rate") and bounce_rate > filters["max_bounce_rate"]:
                bounce_rate = filters["max_bounce_rate"]
        
        data.append({
            'date': date,
            'users': users,
            'sessions': sessions,
            'pageviews': pageviews,
            'bounce_rate': bounce_rate,
            'conversion_rate': np.random.uniform(2, 8)
        })
    
    return pd.DataFrame(data)


@st.cache_resource(scope="session", show_spinner="Initializing ML models...")
def load_ml_models() -> Dict[str, Any]:
    """
    Load ML models with session-scoped resource caching.
    
    Returns:
        Dictionary of initialized ML models
    """
    # Simulate loading ML models
    models = {
        'anomaly_detector': {
            'type': 'isolation_forest',
            'accuracy': 0.95,
            'last_trained': datetime.now() - timedelta(days=7),
            'status': 'ready'
        },
        'cost_predictor': {
            'type': 'random_forest',
            'accuracy': 0.87,
            'last_trained': datetime.now() - timedelta(days=3),
            'status': 'ready'
        },
        'recommendation_engine': {
            'type': 'collaborative_filtering',
            'accuracy': 0.82,
            'last_trained': datetime.now() - timedelta(days=1),
            'status': 'ready'
        }
    }
    
    return models


# Cache management utilities
def show_cache_dashboard():
    """Display a dashboard for cache management."""
    st.markdown("### 🗄️ Session Cache Dashboard")
    
    # Get cache statistics
    stats = SessionCacheManager.get_cache_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Cached Items",
            stats['total_cached_items'],
            help="Number of items currently cached in session"
        )
    
    with col2:
        size_kb = stats['estimated_total_size'] / 1024
        st.metric(
            "Cache Size",
            f"{size_kb:.1f} KB",
            help="Estimated total size of cached data"
        )
    
    with col3:
        if st.button("🗑️ Clear Cache", use_container_width=True):
            cleared = SessionCacheManager.clear_session_cache()
            st.success(f"Cleared {cleared} cached items")
            st.rerun()
    
    # Show cache details
    if stats['cache_details']:
        st.markdown("#### Cache Details")
        
        for key, info in stats['cache_details'].items():
            with st.expander(f"📦 {key.replace('_cache_', '')}"):
                if 'error' in info:
                    st.error(info['error'])
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Type:** {info['type']}")
                        st.write(f"**Size:** {info['size_estimate']} bytes")
                    with col2:
                        if st.button(f"Clear {key}", key=f"clear_{key}"):
                            if key in st.session_state:
                                del st.session_state[key]
                                st.success("Cache cleared!")
                                st.rerun()
    else:
        st.info("No cached items found")


# Performance monitoring
def monitor_cache_performance():
    """Monitor and display cache performance metrics."""
    if 'cache_performance' not in st.session_state:
        st.session_state.cache_performance = {
            'hits': 0,
            'misses': 0,
            'total_load_time': 0,
            'function_stats': {}
        }
    
    perf = st.session_state.cache_performance
    
    if perf['hits'] + perf['misses'] > 0:
        hit_rate = perf['hits'] / (perf['hits'] + perf['misses']) * 100
        avg_load_time = perf['total_load_time'] / (perf['hits'] + perf['misses'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Cache Hit Rate", f"{hit_rate:.1f}%")
        
        with col2:
            st.metric("Avg Load Time", f"{avg_load_time:.3f}s")
        
        with col3:
            st.metric("Total Requests", perf['hits'] + perf['misses'])
    else:
        st.info("No cache performance data available yet")