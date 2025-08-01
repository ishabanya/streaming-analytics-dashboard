#!/usr/bin/env python3
"""
Main Streamlit App for Streaming Platform ETL + Dashboard
Deployable to Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime, timedelta
import random

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

# Demo data generator for Streamlit Cloud
class DemoDataGenerator:
    """Generates realistic demo data for the streaming platform"""
    
    def __init__(self):
        self.content_titles = [
            "The Matrix", "Breaking Bad", "Planet Earth", "Live Sports Event",
            "Friends", "Game of Thrones", "The Office", "Stranger Things",
            "Black Mirror", "The Crown", "Narcos", "Money Heist",
            "The Witcher", "Bridgerton", "Wednesday", "Wednesday Addams"
        ]
        self.device_types = ["mobile", "desktop", "tablet", "smart_tv", "gaming_console"]
        self.platforms = ["web", "ios", "android", "roku", "fire_tv", "apple_tv"]
        self.countries = ["US", "UK", "CA", "AU", "DE", "FR", "JP", "BR", "IN", "MX"]
        self.qualities = ["240p", "360p", "480p", "720p", "1080p", "4K"]
        self.error_types = ["network_error", "playback_error", "authentication_error", "content_not_found"]
        
    def generate_demo_data(self, hours_back=2):
        """Generate demo data for the specified time range"""
        logs = []
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_back)
        
        # Generate more realistic data distribution
        total_events = random.randint(800, 1200)
        
        for i in range(total_events):
            timestamp = start_time + timedelta(
                seconds=random.randint(0, int((end_time - start_time).total_seconds()))
            )
            
            # Weighted event types (more plays, fewer errors)
            event_weights = [0.6, 0.2, 0.05, 0.1, 0.03, 0.02]  # play, pause, stop, error, seek, quality_change
            event_type = random.choices(
                ['play_started', 'playback_paused', 'playback_stopped', 'playback_error', 'playback_seek', 'quality_changed'],
                weights=event_weights
            )[0]
            
            # Generate error type only for error events
            error_type = None
            if event_type == 'playback_error':
                error_type = random.choice(self.error_types)
            
            log = {
                'timestamp': timestamp,
                'event_type': event_type,
                'user_id': f"user_{random.randint(1000, 9999)}",
                'content_title': random.choice(self.content_titles),
                'device_type': random.choice(self.device_types),
                'platform': random.choice(self.platforms),
                'country': random.choice(self.countries),
                'duration': random.randint(1, 3600),
                'quality': random.choice(self.qualities),
                'error_type': error_type,
                'response_time': random.randint(100, 5000)
            }
            logs.append(log)
        
        return pd.DataFrame(logs)

# Initialize demo data generator
@st.cache_resource
def get_demo_data_generator():
    return DemoDataGenerator()

demo_generator = get_demo_data_generator()

# Metrics calculator
class MetricsCalculator:
    """Calculates various metrics from streaming platform logs"""
    
    def get_all_metrics(self, logs_df):
        """Calculate all metrics for the dashboard"""
        if logs_df.empty:
            return {}
        
        # Calculate basic metrics
        play_logs = logs_df[logs_df['event_type'] == 'play_started']
        error_logs = logs_df[logs_df['event_type'] == 'playback_error']
        
        # Calculate plays per minute (assuming 5-minute window)
        time_window_minutes = 5
        plays_per_minute = len(play_logs) / time_window_minutes if time_window_minutes > 0 else 0
        
        # Calculate error rate
        error_rate = (len(error_logs) / len(logs_df) * 100) if len(logs_df) > 0 else 0
        
        # Calculate user engagement
        active_users = logs_df['user_id'].nunique()
        avg_session_duration = logs_df['duration'].mean() if not logs_df.empty else 0
        engagement_score = len(play_logs) / active_users if active_users > 0 else 0
        
        # Calculate performance metrics
        avg_response_time = logs_df['response_time'].mean() if not logs_df.empty else 0
        total_play_events = len(play_logs)
        buffer_underruns = int(total_play_events * 0.012)  # 1.2% buffer underrun rate
        buffer_underrun_rate = (buffer_underruns / total_play_events * 100) if total_play_events > 0 else 0
        
        metrics = {
            'plays_per_minute': {
                'plays_per_minute': plays_per_minute,
                'total_plays': len(play_logs),
                'time_window': time_window_minutes
            },
            'error_rates': {
                'error_rate': error_rate,
                'total_errors': len(error_logs),
                'error_types': error_logs['error_type'].value_counts().to_dict() if not error_logs.empty else {}
            },
            'top_titles': [
                {'title': title, 'play_count': count, 'percentage': (count / len(play_logs) * 100) if len(play_logs) > 0 else 0}
                for title, count in play_logs['content_title'].value_counts().head(10).items()
            ],
            'user_engagement': {
                'active_users': active_users,
                'avg_session_duration': avg_session_duration,
                'engagement_score': engagement_score
            },
            'geographic_distribution': logs_df['country'].value_counts().to_dict(),
            'device_platform_stats': {
                'devices': logs_df['device_type'].value_counts().to_dict(),
                'platforms': logs_df['platform'].value_counts().to_dict()
            },
            'performance_metrics': {
                'avg_response_time': avg_response_time,
                'buffer_underrun_rate': buffer_underrun_rate,
                'total_play_events': total_play_events,
                'buffer_underruns': buffer_underruns
            }
        }
        
        return metrics

@st.cache_resource
def get_metrics_calculator():
    return MetricsCalculator()

metrics_calculator = get_metrics_calculator()

def get_recent_data(minutes: int = 30):
    """Get recent data from demo generator"""
    hours_back = minutes / 60
    logs_df = demo_generator.generate_demo_data(hours_back=max(1, hours_back))
    
    # Filter for the specified time range
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=minutes)
    
    logs_df['timestamp'] = pd.to_datetime(logs_df['timestamp'])
    mask = (logs_df['timestamp'] >= start_time) & (logs_df['timestamp'] <= end_time)
    return logs_df[mask]

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