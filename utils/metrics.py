"""
Metrics calculation utilities for the Streaming Platform ETL System
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from collections import defaultdict, Counter
import config

logger = logging.getLogger(__name__)

class MetricsCalculator:
    """Calculates various metrics from streaming platform logs"""
    
    def __init__(self):
        self.metrics_cache = {}
        self.cache_ttl = 60  # seconds
    
    def calculate_plays_per_minute(self, logs_df: pd.DataFrame, 
                                 window_minutes: int = 5) -> Dict[str, Any]:
        """Calculate plays per minute over a time window"""
        try:
            if logs_df.empty:
                return {"plays_per_minute": 0, "total_plays": 0, "time_window": window_minutes}
            
            # Filter for play events
            play_logs = logs_df[logs_df['log_type'] == 'play'].copy()
            
            if play_logs.empty:
                return {"plays_per_minute": 0, "total_plays": 0, "time_window": window_minutes}
            
            # Convert timestamp to datetime if it's not already
            play_logs['timestamp'] = pd.to_datetime(play_logs['timestamp'])
            
            # Get the time range
            end_time = play_logs['timestamp'].max()
            start_time = end_time - timedelta(minutes=window_minutes)
            
            # Filter logs within the time window
            recent_plays = play_logs[play_logs['timestamp'] >= start_time]
            
            total_plays = len(recent_plays)
            plays_per_minute = total_plays / window_minutes
            
            return {
                "plays_per_minute": round(plays_per_minute, 2),
                "total_plays": total_plays,
                "time_window": window_minutes,
                "start_time": start_time,
                "end_time": end_time
            }
            
        except Exception as e:
            logger.error(f"Error calculating plays per minute: {e}")
            return {"plays_per_minute": 0, "total_plays": 0, "time_window": window_minutes}
    
    def calculate_error_rates(self, logs_df: pd.DataFrame, 
                            window_minutes: int = 5) -> Dict[str, Any]:
        """Calculate error rates and types"""
        try:
            if logs_df.empty:
                return {"error_rate": 0, "total_errors": 0, "error_types": {}}
            
            # Filter for error events
            error_logs = logs_df[logs_df['log_type'] == 'error'].copy()
            
            if error_logs.empty:
                return {"error_rate": 0, "total_errors": 0, "error_types": {}}
            
            # Convert timestamp to datetime
            error_logs['timestamp'] = pd.to_datetime(error_logs['timestamp'])
            
            # Get the time range
            end_time = error_logs['timestamp'].max()
            start_time = end_time - timedelta(minutes=window_minutes)
            
            # Filter logs within the time window
            recent_errors = error_logs[error_logs['timestamp'] >= start_time]
            
            # Calculate total events in the same time window
            all_logs = logs_df.copy()
            all_logs['timestamp'] = pd.to_datetime(all_logs['timestamp'])
            recent_all = all_logs[all_logs['timestamp'] >= start_time]
            
            total_errors = len(recent_errors)
            total_events = len(recent_all)
            error_rate = (total_errors / total_events * 100) if total_events > 0 else 0
            
            # Count error types
            error_types = recent_errors['error_type'].value_counts().to_dict()
            
            return {
                "error_rate": round(error_rate, 2),
                "total_errors": total_errors,
                "total_events": total_events,
                "error_types": error_types,
                "time_window": window_minutes
            }
            
        except Exception as e:
            logger.error(f"Error calculating error rates: {e}")
            return {"error_rate": 0, "total_errors": 0, "error_types": {}}
    
    def get_top_titles(self, logs_df: pd.DataFrame, 
                      limit: int = 10) -> List[Dict[str, Any]]:
        """Get top streaming titles by play count"""
        try:
            if logs_df.empty:
                return []
            
            # Filter for play events
            play_logs = logs_df[logs_df['log_type'] == 'play'].copy()
            
            if play_logs.empty:
                return []
            
            # Count plays by content title
            title_counts = play_logs['content_title'].value_counts().head(limit)
            
            top_titles = []
            for title, count in title_counts.items():
                if pd.notna(title):  # Skip null titles
                    top_titles.append({
                        "title": title,
                        "play_count": int(count),
                        "percentage": round((count / len(play_logs)) * 100, 2)
                    })
            
            return top_titles
            
        except Exception as e:
            logger.error(f"Error getting top titles: {e}")
            return []
    
    def calculate_user_engagement(self, logs_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate user engagement metrics"""
        try:
            if logs_df.empty:
                return {"active_users": 0, "avg_session_duration": 0, "engagement_score": 0}
            
            # Get unique users
            unique_users = logs_df['user_id'].nunique()
            
            # Calculate average session duration
            session_durations = []
            for user_id in logs_df['user_id'].unique():
                if pd.notna(user_id):
                    user_logs = logs_df[logs_df['user_id'] == user_id].copy()
                    user_logs['timestamp'] = pd.to_datetime(user_logs['timestamp'])
                    
                    if len(user_logs) > 1:
                        duration = (user_logs['timestamp'].max() - user_logs['timestamp'].min()).total_seconds()
                        session_durations.append(duration)
            
            avg_session_duration = np.mean(session_durations) if session_durations else 0
            
            # Calculate engagement score (plays per user)
            total_plays = len(logs_df[logs_df['log_type'] == 'play'])
            engagement_score = total_plays / unique_users if unique_users > 0 else 0
            
            return {
                "active_users": int(unique_users),
                "avg_session_duration": round(avg_session_duration, 2),
                "engagement_score": round(engagement_score, 2),
                "total_plays": total_plays
            }
            
        except Exception as e:
            logger.error(f"Error calculating user engagement: {e}")
            return {"active_users": 0, "avg_session_duration": 0, "engagement_score": 0}
    
    def calculate_geographic_distribution(self, logs_df: pd.DataFrame) -> Dict[str, int]:
        """Calculate geographic distribution of users"""
        try:
            if logs_df.empty:
                return {}
            
            # Count logs by country
            country_counts = logs_df['country'].value_counts().to_dict()
            
            # Remove null values
            country_counts = {k: v for k, v in country_counts.items() if pd.notna(k)}
            
            return country_counts
            
        except Exception as e:
            logger.error(f"Error calculating geographic distribution: {e}")
            return {}
    
    def calculate_device_platform_stats(self, logs_df: pd.DataFrame) -> Dict[str, Dict[str, int]]:
        """Calculate device and platform statistics"""
        try:
            if logs_df.empty:
                return {"devices": {}, "platforms": {}}
            
            # Device type distribution
            device_counts = logs_df['device_type'].value_counts().to_dict()
            device_counts = {k: v for k, v in device_counts.items() if pd.notna(k)}
            
            # Platform distribution
            platform_counts = logs_df['platform'].value_counts().to_dict()
            platform_counts = {k: v for k, v in platform_counts.items() if pd.notna(k)}
            
            return {
                "devices": device_counts,
                "platforms": platform_counts
            }
            
        except Exception as e:
            logger.error(f"Error calculating device/platform stats: {e}")
            return {"devices": {}, "platforms": {}}
    
    def calculate_performance_metrics(self, logs_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate performance-related metrics"""
        try:
            if logs_df.empty:
                return {"avg_response_time": 0, "buffer_underrun_rate": 0}
            
            # Average response time
            response_times = logs_df['response_time'].dropna()
            avg_response_time = response_times.mean() if not response_times.empty else 0
            
            # Buffer underrun rate (simulated)
            total_play_events = len(logs_df[logs_df['log_type'] == 'play'])
            buffer_underruns = int(total_play_events * config.BUFFER_UNDERRUN_RATE)
            buffer_underrun_rate = (buffer_underruns / total_play_events * 100) if total_play_events > 0 else 0
            
            return {
                "avg_response_time": round(avg_response_time, 2),
                "buffer_underrun_rate": round(buffer_underrun_rate, 2),
                "total_play_events": total_play_events,
                "buffer_underruns": buffer_underruns
            }
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {"avg_response_time": 0, "buffer_underrun_rate": 0}
    
    def calculate_time_series_metrics(self, logs_df: pd.DataFrame, 
                                    interval_minutes: int = 5) -> pd.DataFrame:
        """Calculate time series metrics"""
        try:
            if logs_df.empty:
                return pd.DataFrame()
            
            # Convert timestamp to datetime
            logs_df = logs_df.copy()
            logs_df['timestamp'] = pd.to_datetime(logs_df['timestamp'])
            
            # Create time bins
            logs_df['time_bin'] = logs_df['timestamp'].dt.floor(f'{interval_minutes}T')
            
            # Group by time bin and calculate metrics
            time_series = logs_df.groupby('time_bin').agg({
                'log_type': lambda x: (x == 'play').sum(),  # Play count
                'user_id': 'nunique',  # Unique users
                'log_type': lambda x: (x == 'error').sum()  # Error count
            }).rename(columns={
                'log_type': 'plays',
                'user_id': 'unique_users',
                'log_type': 'errors'
            })
            
            # Calculate error rate
            time_series['error_rate'] = (time_series['errors'] / 
                                       (time_series['plays'] + time_series['errors']) * 100)
            
            return time_series.reset_index()
            
        except Exception as e:
            logger.error(f"Error calculating time series metrics: {e}")
            return pd.DataFrame()
    
    def get_all_metrics(self, logs_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate all metrics for the dashboard"""
        try:
            metrics = {}
            
            # Basic metrics
            metrics['plays_per_minute'] = self.calculate_plays_per_minute(logs_df)
            metrics['error_rates'] = self.calculate_error_rates(logs_df)
            metrics['top_titles'] = self.get_top_titles(logs_df)
            metrics['user_engagement'] = self.calculate_user_engagement(logs_df)
            metrics['geographic_distribution'] = self.calculate_geographic_distribution(logs_df)
            metrics['device_platform_stats'] = self.calculate_device_platform_stats(logs_df)
            metrics['performance_metrics'] = self.calculate_performance_metrics(logs_df)
            metrics['time_series'] = self.calculate_time_series_metrics(logs_df)
            
            # Add timestamp
            metrics['calculated_at'] = datetime.now().isoformat()
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating all metrics: {e}")
            return {}

# Global metrics calculator instance
metrics_calculator = MetricsCalculator() 