"""
Caching Showcase Component - Demonstrates Enhanced Session-Scoped Caching.

This component showcases the session-scoped caching capabilities with
performance monitoring and cache management features.
"""

import streamlit as st
import time
import pandas as pd
from datetime import datetime
from src.ui.enhanced_caching import (
    SessionCacheManager,
    session_cached_data,
    session_cached_resource,
    load_financial_data,
    load_performance_metrics,
    process_analytics_data,
    load_ml_models,
    show_cache_dashboard,
    monitor_cache_performance
)


def render_caching_showcase():
    """Render the caching showcase component."""
    st.markdown("## 🗄️ Enhanced Session-Scoped Caching Showcase")
    st.markdown("Test the new Streamlit nightly session-scoped caching features for improved performance.")
    
    # Cache Dashboard
    st.markdown("### Cache Management Dashboard")
    show_cache_dashboard()
    
    st.divider()
    
    # Performance Monitoring
    st.markdown("### Cache Performance Monitoring")
    monitor_cache_performance()
    
    st.divider()
    
    # Data Loading Examples
    st.markdown("### Session-Scoped Data Loading")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Load Financial Data", use_container_width=True):
            start_time = time.time()
            data = load_financial_data(days=30)
            load_time = time.time() - start_time
            
            st.success(f"Loaded {len(data)} records in {load_time:.3f}s")
            st.dataframe(data.head(), use_container_width=True)
    
    with col2:
        if st.button("⚡ Load Performance Metrics", use_container_width=True):
            start_time = time.time()
            metrics = load_performance_metrics()
            load_time = time.time() - start_time
            
            st.success(f"Loaded metrics for {len(metrics)} services in {load_time:.3f}s")
            st.json(metrics)
    
    # Analytics Processing
    st.markdown("### Analytics Data Processing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        aggregation = st.selectbox("Aggregation", ["daily", "weekly", "monthly"])
    
    with col2:
        min_users = st.number_input("Min Users Filter", min_value=0, value=500)
    
    with col3:
        if st.button("🔄 Process Analytics", use_container_width=True):
            filters = {"min_users": min_users} if min_users > 0 else None
            
            start_time = time.time()
            analytics_data = process_analytics_data(
                data_source="web_analytics",
                aggregation=aggregation,
                filters=filters
            )
            load_time = time.time() - start_time
            
            st.success(f"Processed {len(analytics_data)} records in {load_time:.3f}s")
            st.dataframe(analytics_data, use_container_width=True)
    
    st.divider()
    
    # Resource Caching Examples
    st.markdown("### Session-Scoped Resource Caching")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🤖 Load ML Models", use_container_width=True):
            start_time = time.time()
            models = load_ml_models()
            load_time = time.time() - start_time
            
            st.success(f"Loaded {len(models)} ML models in {load_time:.3f}s")
            
            for model_name, model_info in models.items():
                with st.expander(f"🔬 {model_name.replace('_', ' ').title()}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**Type:** {model_info['type']}")
                        st.write(f"**Accuracy:** {model_info['accuracy']:.1%}")
                    with col_b:
                        st.write(f"**Status:** {model_info['status']}")
                        st.write(f"**Last Trained:** {model_info['last_trained'].strftime('%Y-%m-%d')}")
    
    with col2:
        if st.button("🔄 Refresh All Resources", use_container_width=True):
            # Clear resource caches
            load_ml_models.clear()
            
            st.success("Resource caches cleared!")
            st.info("Next load will fetch fresh resources")
    
    st.divider()
    
    # Custom Caching Examples
    st.markdown("### Custom Session-Scoped Caching")
    
    # Example with custom cached function
    @session_cached_data(ttl=300, show_spinner=True)
    def expensive_computation(complexity: int) -> dict:
        """Simulate an expensive computation."""
        time.sleep(complexity * 0.5)  # Simulate processing time
        
        result = {
            "computation_id": f"comp_{complexity}_{int(time.time())}",
            "complexity": complexity,
            "result": sum(range(complexity * 1000)),
            "timestamp": datetime.now().isoformat(),
            "processing_time": complexity * 0.5
        }
        
        return result
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        complexity = st.slider("Computation Complexity", 1, 5, 2)
    
    with col2:
        if st.button("🧮 Run Computation", use_container_width=True):
            start_time = time.time()
            result = expensive_computation(complexity)
            actual_time = time.time() - start_time
            
            st.success(f"Completed in {actual_time:.3f}s (expected: {result['processing_time']:.1f}s)")
            st.json(result)
    
    with col3:
        if st.button("🗑️ Clear Computation Cache", use_container_width=True):
            expensive_computation.clear()
            st.success("Computation cache cleared!")
    
    st.divider()
    
    # Cache Statistics and Analysis
    st.markdown("### Cache Statistics & Analysis")
    
    stats = SessionCacheManager.get_cache_stats()
    
    if stats['total_cached_items'] > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Cached Items", stats['total_cached_items'])
        
        with col2:
            size_mb = stats['estimated_total_size'] / (1024 * 1024)
            st.metric("Cache Size", f"{size_mb:.2f} MB")
        
        with col3:
            if st.button("📊 Analyze Cache Usage", use_container_width=True):
                st.session_state["show_cache_analysis"] = True
        
        # Cache Analysis
        if st.session_state.get("show_cache_analysis", False):
            st.markdown("#### Detailed Cache Analysis")
            
            # Create cache usage chart
            cache_data = []
            for key, info in stats['cache_details'].items():
                if 'size_estimate' in info:
                    cache_data.append({
                        'Cache Key': key.replace('_cache_', '').replace('_', ' ').title(),
                        'Size (bytes)': info['size_estimate'],
                        'Type': info['type']
                    })
            
            if cache_data:
                df = pd.DataFrame(cache_data)
                
                # Size distribution chart
                st.bar_chart(df.set_index('Cache Key')['Size (bytes)'])
                
                # Detailed table
                st.dataframe(df, use_container_width=True)
            
            if st.button("❌ Close Analysis"):
                st.session_state["show_cache_analysis"] = False
                st.rerun()
    else:
        st.info("No cached data available. Try loading some data first!")
    
    st.divider()
    
    # Cache Management Tools
    st.markdown("### Cache Management Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh All Data Caches", use_container_width=True):
            # Clear all data caches
            load_financial_data.clear()
            load_performance_metrics.clear()
            process_analytics_data.clear()
            
            st.success("All data caches refreshed!")
    
    with col2:
        if st.button("🗑️ Clear Pattern Cache", use_container_width=True):
            pattern = st.text_input("Cache pattern to clear:", value="financial")
            if pattern:
                cleared = SessionCacheManager.clear_session_cache(pattern)
                st.success(f"Cleared {cleared} cache items matching '{pattern}'")
    
    with col3:
        if st.button("⚠️ Clear All Caches", use_container_width=True):
            cleared = SessionCacheManager.clear_session_cache()
            st.warning(f"Cleared all {cleared} cached items!")
    
    # Performance Tips
    st.markdown("### 💡 Performance Tips")
    
    with st.expander("Session-Scoped Caching Best Practices"):
        st.markdown("""
        **Session-Scoped Caching Benefits:**
        - ✅ Data persists for the entire user session
        - ✅ Improved performance for repeated operations
        - ✅ Reduced server load and API calls
        - ✅ Better user experience with faster loading
        
        **Best Practices:**
        - Use `scope="session"` for user-specific data
        - Set appropriate TTL values for data freshness
        - Monitor cache size to avoid memory issues
        - Clear caches when data becomes stale
        - Use `show_spinner` for better UX during loading
        
        **When to Use Session-Scoped Caching:**
        - User preferences and settings
        - Authentication tokens and user data
        - Expensive computations with stable inputs
        - External API responses with low change frequency
        - ML model predictions and analysis results
        """)


def add_caching_examples_to_dashboard():
    """Add caching examples to existing dashboard components."""
    
    st.markdown("### 🚀 Performance-Enhanced Components")
    
    # Example of cached dashboard data
    @session_cached_data(ttl=1800, show_spinner=True)
    def get_dashboard_summary():
        """Get dashboard summary with session caching."""
        # Simulate data aggregation
        time.sleep(0.5)  # Simulate processing time
        
        return {
            "total_users": 12543,
            "active_sessions": 892,
            "revenue_today": 45230.50,
            "conversion_rate": 3.2,
            "avg_response_time": 0.12,
            "error_rate": 0.05,
            "last_updated": datetime.now()
        }
    
    # Load cached summary
    summary = get_dashboard_summary()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", f"{summary['total_users']:,}")
        st.metric("Active Sessions", f"{summary['active_sessions']:,}")
    
    with col2:
        st.metric("Revenue Today", f"${summary['revenue_today']:,.2f}")
        st.metric("Conversion Rate", f"{summary['conversion_rate']:.1f}%")
    
    with col3:
        st.metric("Response Time", f"{summary['avg_response_time']:.3f}s")
        st.metric("Error Rate", f"{summary['error_rate']:.2f}%")
    
    st.caption(f"Last updated: {summary['last_updated'].strftime('%H:%M:%S')}")
    
    if st.button("🔄 Refresh Dashboard Data"):
        get_dashboard_summary.clear()
        st.rerun()