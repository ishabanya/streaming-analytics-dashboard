"""
Configuration settings for the Streaming Platform ETL System
"""

import os
from datetime import datetime

# Database Configuration
DATABASE_PATH = "data/streaming.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Log Producer Configuration
LOG_GENERATION_RATE = 10  # logs per second
LOG_TYPES = ["play", "pause", "stop", "error", "seek", "quality_change"]
LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]

# Streaming Content Configuration
CONTENT_TYPES = ["movie", "tv_show", "documentary", "live_stream"]
CONTENT_TITLES = [
    "The Matrix", "Breaking Bad", "Planet Earth", "Live Sports Event",
    "Friends", "Game of Thrones", "The Office", "Stranger Things",
    "Black Mirror", "The Crown", "Narcos", "Money Heist",
    "The Witcher", "Bridgerton", "Wednesday", "Wednesday Addams",
    "Wednesday TV Show", "Wednesday Netflix", "Wednesday Series"
]

# User Configuration
USER_COUNTRIES = ["US", "UK", "CA", "AU", "DE", "FR", "JP", "BR", "IN", "MX"]
DEVICE_TYPES = ["mobile", "desktop", "tablet", "smart_tv", "gaming_console"]
PLATFORMS = ["web", "ios", "android", "roku", "fire_tv", "apple_tv"]

# ETL Configuration
ETL_PROCESSING_INTERVAL = 5  # seconds
BATCH_SIZE = 100
RETENTION_DAYS = 30

# Dashboard Configuration
DASHBOARD_REFRESH_RATE = 5  # seconds
CHART_UPDATE_INTERVAL = 10  # seconds

# Error Configuration
ERROR_RATES = {
    "network_error": 0.02,  # 2%
    "playback_error": 0.01,  # 1%
    "authentication_error": 0.005,  # 0.5%
    "content_not_found": 0.003,  # 0.3%
}

# Performance Configuration
RESPONSE_TIME_RANGE = (100, 5000)  # milliseconds
BUFFER_UNDERRUN_RATE = 0.01  # 1%

# Time Configuration
TIMEZONE = "UTC"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# File Paths
DATA_DIR = "data"
LOGS_DIR = "logs"
EXPORT_DIR = "exports"

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, EXPORT_DIR]:
    os.makedirs(directory, exist_ok=True) 