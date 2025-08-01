#!/usr/bin/env python3
"""
Main Streamlit App for Streaming Platform ETL + Dashboard
Deployable to Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import sys
import os
import sqlite3
import threading
import queue

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
try:
    from utils.database import DatabaseManager
    from utils.metrics import MetricsCalculator
    import config
except ImportError:
    # For Streamlit Cloud deployment, create simplified versions
    st.error("Some modules not available. Running in demo mode.")
    
    # Create a simple demo database manager
    class DatabaseManager:
        def __init__(self):
            self.demo_data = self._generate_demo_data()
        
        def _generate_demo_data(self):
            """Generate demo data for Streamlit Cloud"""
            import random
            from datetime import datetime, timedelta
            
            # Generate demo logs
            logs = []
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=2)
            
            content_titles = [
                "The Matrix", "Breaking Bad", "Planet Earth", "Live Sports Event",
                "Friends", "Game of Thrones", "The Office", "Stranger Things",
                "Black Mirror", "The Crown", "Narcos", "Money Heist"
            ]
            
            device_types = ["mobile", "desktop", "tablet", "smart_tv"]
            platforms = ["web", "ios", "android", "roku"]
            countries = ["US", "UK", "CA", "AU", "DE", "FR", "JP", "BR"]
            
            for i in range(1000):
                timestamp = start_time + timedelta(
                    seconds=random.randint(0, int((end_time - start_time).total_seconds()))
                )
                
                log = {
                    'timestamp': timestamp,
                    'event_type': random.choice(['play_started', 'playback_paused', 'playback_error']),
                    'user_id': f"user_{random.randint(1000, 9999)}",
                    'content_title': random.choice(content_titles),
                    'device_type': random.choice(device_types),
                    'platform': random.choice(platforms),
                    'country': random.choice(countries),
                    'duration': random.randint(1, 3600),
                    'quality': random.choice(['240p', '360p', '480p', '720p', '1080p']),
                    'error_type': random.choice(['network_error', 'playback_error', 'authentication_error']) if random.random() < 0.1 else None,
                    'response_time': random.randint(100, 5000)
                }
                logs.append(log)
            
            return pd.DataFrame(logs)
        
        def get_logs_by_timeframe(self, start_time, end_time, table="processed_logs", limit=1000):
            """Get logs within timeframe (demo version)"""
            df = self.demo_data.copy()
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            mask = (df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)
            return df[mask].head(limit)
    
    # Create a simple metrics calculator
    class MetricsCalculator:
        def get_all_metrics(self, logs_df):
            """Calculate all metrics (demo version)"""
            if logs_df.empty:
                return {}
            
            # Calculate basic metrics
            play_logs = logs_df[logs_df['event_type'] == 'play_started']
            error_logs = logs_df[logs_df['event_type'] == 'playback_error']
            
            metrics = {
                'plays_per_minute': {
                    'plays_per_minute': len(play_logs) / 5,  # Assuming 5-minute window
                    'total_plays': len(play_logs),
                    'time_window': 5
                },
                'error_rates': {
                    'error_rate': (len(error_logs) / len(logs_df) * 100) if len(logs_df) > 0 else 0,
                    'total_errors': len(error_logs),
                    'error_types': error_logs['error_type'].value_counts().to_dict() if not error_logs.empty else {}
                },
                'top_titles': [
                    {'title': title, 'play_count': count, 'percentage': (count / len(play_logs) * 100) if len(play_logs) > 0 else 0}
                    for title, count in play_logs['content_title'].value_counts().head(10).items()
                ],
                'user_engagement': {
                    'active_users': logs_df['user_id'].nunique(),
                    'avg_session_duration': logs_df['duration'].mean() if not logs_df.empty else 0,
                    'engagement_score': len(play_logs) / logs_df['user_id'].nunique() if logs_df['user_id'].nunique() > 0 else 0
                },
                'geographic_distribution': logs_df['country'].value_counts().to_dict(),
                'device_platform_stats': {
                    'devices': logs_df['device_type'].value_counts().to_dict(),
                    'platforms': logs_df['platform'].value_counts().to_dict()
                },
                'performance_metrics': {
                    'avg_response_time': logs_df['response_time'].mean() if not logs_df.empty else 0,
                    'buffer_underrun_rate': 1.2,  # Demo value
                    'total_play_events': len(play_logs),
                    'buffer_underruns': int(len(play_logs) * 0.012)
                }
            }
            
            return metrics

# Initialize components
@st.cache_resource
def init_components():
    """Initialize database and metrics components"""
    return DatabaseManager(), MetricsCalculator()

db_manager, metrics_calculator = init_components()

# Page configuration
st.set_page_config(
    page_title="Streaming Platform Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
    }
    .stApp {
        background-color: #fafafa;
    }
</style>
""", unsafe_allow_html=True)

def get_recent_data(minutes: int = 30):
    """Get recent data from the database"""
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=minutes)
    
    # Get processed logs
    logs_df = db_manager.get_logs_by_timeframe(start_time, end_time, table="processed_logs")
    
    return logs_df

def display_header():
    """Display the main header"""
    st.markdown('<h1 class="main-header">📊 Streaming Platform Analytics</h1>', unsafe_allow_html=True)
    
    # Add timestamp
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def display_key_metrics(logs_df: pd.DataFrame):
    """Display key metrics in cards"""
    st.subheader("🎯 Key Metrics")
    
    # Calculate metrics
    metrics = metrics_calculator.get_all_metrics(logs_df)
    
    # Create metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        plays_per_min = metrics.get('plays_per_minute', {}).get('plays_per_minute', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{plays_per_min:.1f}</div>
            <div class="metric-label">Plays per Minute</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        error_rate = metrics.get('error_rates', {}).get('error_rate', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{error_rate:.1f}%</div>
            <div class="metric-label">Error Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        active_users = metrics.get('user_engagement', {}).get('active_users', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{active_users}</div>
            <div class="metric-label">Active Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_response = metrics.get('performance_metrics', {}).get('avg_response_time', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_response:.0f}ms</div>
            <div class="metric-label">Avg Response Time</div>
        </div>
        """, unsafe_allow_html=True)

def display_plays_chart(logs_df: pd.DataFrame):
    """Display plays over time chart"""
    st.subheader("📈 Plays Over Time")
    
    if not logs_df.empty:
        # Filter for play events
        play_logs = logs_df[logs_df['event_type'] == 'play_started'].copy()
        
        if not play_logs.empty:
            # Convert timestamp to datetime
            play_logs['timestamp'] = pd.to_datetime(play_logs['timestamp'])
            
            # Group by minute
            play_logs['minute'] = play_logs['timestamp'].dt.floor('min')
            plays_by_minute = play_logs.groupby('minute').size().reset_index(name='plays')
            
            # Create chart
            fig = px.line(
                plays_by_minute, 
                x='minute', 
                y='plays',
                title="Plays per Minute",
                labels={'minute': 'Time', 'plays': 'Number of Plays'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No play events found in the selected time range.")
    else:
        st.info("No data available for the selected time range.")

def display_top_titles(logs_df: pd.DataFrame):
    """Display top streaming titles"""
    st.subheader("🏆 Top Streaming Titles")
    
    if not logs_df.empty:
        # Filter for play events
        play_logs = logs_df[logs_df['event_type'] == 'play_started'].copy()
        
        if not play_logs.empty:
            # Count plays by title
            title_counts = play_logs['content_title'].value_counts().head(10)
            
            # Create bar chart
            fig = px.bar(
                x=title_counts.values,
                y=title_counts.index,
                orientation='h',
                title="Top 10 Titles by Play Count",
                labels={'x': 'Play Count', 'y': 'Title'}
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display as table
            st.subheader("📋 Title Rankings")
            title_df = pd.DataFrame({
                'Title': title_counts.index,
                'Play Count': title_counts.values,
                'Percentage': (title_counts.values / len(play_logs) * 100).round(2)
            })
            st.dataframe(title_df, use_container_width=True)
        else:
            st.info("No play events found in the selected time range.")
    else:
        st.info("No data available for the selected time range.")

def display_error_analysis(logs_df: pd.DataFrame):
    """Display error analysis"""
    st.subheader("⚠️ Error Analysis")
    
    if not logs_df.empty:
        # Filter for error events
        error_logs = logs_df[logs_df['event_type'] == 'playback_error'].copy()
        
        if not error_logs.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Error types pie chart
                error_types = error_logs['error_type'].value_counts()
                fig = px.pie(
                    values=error_types.values,
                    names=error_types.index,
                    title="Error Types Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Error rate over time
                error_logs['timestamp'] = pd.to_datetime(error_logs['timestamp'])
                error_logs['minute'] = error_logs['timestamp'].dt.floor('min')
                errors_by_minute = error_logs.groupby('minute').size().reset_index(name='errors')
                
                fig = px.line(
                    errors_by_minute,
                    x='minute',
                    y='errors',
                    title="Errors Over Time"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No error events found in the selected time range.")
    else:
        st.info("No data available for the selected time range.")

def display_geographic_distribution(logs_df: pd.DataFrame):
    """Display geographic distribution"""
    st.subheader("🌍 Geographic Distribution")
    
    if not logs_df.empty:
        # Count by country
        country_counts = logs_df['country'].value_counts()
        
        if not country_counts.empty:
            # Create bar chart
            fig = px.bar(
                x=country_counts.index,
                y=country_counts.values,
                title="Users by Country",
                labels={'x': 'Country', 'y': 'User Count'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No geographic data available.")
    else:
        st.info("No data available for the selected time range.")

def display_device_platform_stats(logs_df: pd.DataFrame):
    """Display device and platform statistics"""
    st.subheader("📱 Device & Platform Statistics")
    
    if not logs_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Device type distribution
            device_counts = logs_df['device_type'].value_counts()
            if not device_counts.empty:
                fig = px.pie(
                    values=device_counts.values,
                    names=device_counts.index,
                    title="Device Type Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Platform distribution
            platform_counts = logs_df['platform'].value_counts()
            if not platform_counts.empty:
                fig = px.pie(
                    values=platform_counts.values,
                    names=platform_counts.index,
                    title="Platform Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected time range.")

def display_performance_metrics(logs_df: pd.DataFrame):
    """Display performance metrics"""
    st.subheader("⚡ Performance Metrics")
    
    if not logs_df.empty:
        # Calculate performance metrics
        metrics = metrics_calculator.get_all_metrics(logs_df)
        perf_metrics = metrics.get('performance_metrics', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Response time distribution
            response_times = logs_df['response_time'].dropna()
            if not response_times.empty:
                fig = px.histogram(
                    response_times,
                    title="Response Time Distribution",
                    labels={'value': 'Response Time (ms)', 'count': 'Frequency'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Performance metrics table
            st.subheader("📊 Performance Summary")
            perf_df = pd.DataFrame([
                ["Average Response Time", f"{perf_metrics.get('avg_response_time', 0):.0f} ms"],
                ["Buffer Underrun Rate", f"{perf_metrics.get('buffer_underrun_rate', 0):.1f}%"],
                ["Total Play Events", perf_metrics.get('total_play_events', 0)],
                ["Buffer Underruns", perf_metrics.get('buffer_underruns', 0)]
            ], columns=["Metric", "Value"])
            st.dataframe(perf_df, use_container_width=True)
    else:
        st.info("No data available for the selected time range.")

def display_recent_logs(logs_df: pd.DataFrame):
    """Display recent logs table"""
    st.subheader("📋 Recent Activity")
    
    if not logs_df.empty:
        # Select relevant columns
        display_df = logs_df[['timestamp', 'event_type', 'user_id', 'content_title', 
                             'device_type', 'platform', 'country']].head(100)
        
        # Format timestamp
        display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No recent activity found.")

def main():
    """Main dashboard function"""
    # Sidebar configuration
    st.sidebar.title("⚙️ Dashboard Settings")
    
    # Time range selector
    time_range = st.sidebar.selectbox(
        "Time Range",
        ["Last 5 minutes", "Last 15 minutes", "Last 30 minutes", "Last 1 hour", "Last 6 hours"],
        index=2
    )
    
    # Convert time range to minutes
    time_mapping = {
        "Last 5 minutes": 5,
        "Last 15 minutes": 15,
        "Last 30 minutes": 30,
        "Last 1 hour": 60,
        "Last 6 hours": 360
    }
    
    minutes = time_mapping[time_range]
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)
    refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)
    
    # Get data
    logs_df = get_recent_data(minutes)
    
    # Display dashboard
    display_header()
    display_key_metrics(logs_df)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Plays", "🏆 Top Titles", "⚠️ Errors", "🌍 Geography", "📱 Devices", "📋 Activity"
    ])
    
    with tab1:
        display_plays_chart(logs_df)
    
    with tab2:
        display_top_titles(logs_df)
    
    with tab3:
        display_error_analysis(logs_df)
    
    with tab4:
        display_geographic_distribution(logs_df)
    
    with tab5:
        display_device_platform_stats(logs_df)
        display_performance_metrics(logs_df)
    
    with tab6:
        display_recent_logs(logs_df)
    
    # Auto-refresh functionality
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main() 