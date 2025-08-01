#!/usr/bin/env python3
"""
Log Producer for the Streaming Platform ETL System
Generates realistic streaming platform logs for testing and demonstration
"""

import time
import random
import json
import logging
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import DatabaseManager
from utils.log_parser import LogParser
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StreamingLogProducer:
    """Produces realistic streaming platform logs"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.log_parser = LogParser()
        self.user_sessions = {}  # Track active user sessions
        self.content_sessions = {}  # Track content playback sessions
        
    def generate_user_id(self) -> str:
        """Generate a realistic user ID"""
        return f"user_{random.randint(10000, 99999)}"
    
    def generate_session_id(self, user_id: str) -> str:
        """Generate a session ID for a user"""
        return f"{user_id}_{int(time.time())}"
    
    def generate_content_id(self) -> str:
        """Generate a content ID"""
        return f"content_{random.randint(1000, 9999)}"
    
    def generate_ip_address(self) -> str:
        """Generate a realistic IP address"""
        return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    def generate_user_agent(self, platform: str) -> str:
        """Generate a realistic user agent string"""
        user_agents = {
            "web": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ],
            "ios": [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPad; CPU OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1"
            ],
            "android": [
                "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
            ]
        }
        return random.choice(user_agents.get(platform, user_agents["web"]))
    
    def generate_play_log(self) -> Dict[str, Any]:
        """Generate a play event log"""
        user_id = self.generate_user_id()
        session_id = self.generate_session_id(user_id)
        content_title = random.choice(config.CONTENT_TITLES)
        content_type = random.choice(config.CONTENT_TYPES)
        device_type = random.choice(config.DEVICE_TYPES)
        platform = random.choice(config.PLATFORMS)
        country = random.choice(config.USER_COUNTRIES)
        
        # Track user session
        self.user_sessions[user_id] = {
            "session_id": session_id,
            "start_time": datetime.now(),
            "device_type": device_type,
            "platform": platform,
            "country": country
        }
        
        log_data = {
            "timestamp": datetime.now(),
            "log_type": "play",
            "log_level": "INFO",
            "user_id": user_id,
            "session_id": session_id,
            "content_id": self.generate_content_id(),
            "content_title": content_title,
            "content_type": content_type,
            "device_type": device_type,
            "platform": platform,
            "country": country,
            "ip_address": self.generate_ip_address(),
            "user_agent": self.generate_user_agent(platform),
            "duration": random.randint(1, 3600),  # 1 second to 1 hour
            "position": random.randint(0, 7200),  # 0 to 2 hours
            "quality": random.choice(["240p", "360p", "480p", "720p", "1080p", "4K"]),
            "response_time": random.randint(config.RESPONSE_TIME_RANGE[0], config.RESPONSE_TIME_RANGE[1])
        }
        
        return log_data
    
    def generate_pause_log(self, user_id: str = None) -> Dict[str, Any]:
        """Generate a pause event log"""
        if user_id is None:
            user_id = random.choice(list(self.user_sessions.keys())) if self.user_sessions else self.generate_user_id()
        
        session_data = self.user_sessions.get(user_id, {})
        session_id = session_data.get("session_id", self.generate_session_id(user_id))
        
        log_data = {
            "timestamp": datetime.now(),
            "log_type": "pause",
            "log_level": "INFO",
            "user_id": user_id,
            "session_id": session_id,
            "content_id": self.generate_content_id(),
            "content_title": random.choice(config.CONTENT_TITLES),
            "content_type": random.choice(config.CONTENT_TYPES),
            "device_type": session_data.get("device_type", random.choice(config.DEVICE_TYPES)),
            "platform": session_data.get("platform", random.choice(config.PLATFORMS)),
            "country": session_data.get("country", random.choice(config.USER_COUNTRIES)),
            "ip_address": self.generate_ip_address(),
            "user_agent": self.generate_user_agent(session_data.get("platform", "web")),
            "duration": random.randint(1, 3600),
            "position": random.randint(0, 7200),
            "quality": random.choice(["240p", "360p", "480p", "720p", "1080p", "4K"]),
            "response_time": random.randint(config.RESPONSE_TIME_RANGE[0], config.RESPONSE_TIME_RANGE[1])
        }
        
        return log_data
    
    def generate_error_log(self) -> Dict[str, Any]:
        """Generate an error event log"""
        user_id = self.generate_user_id()
        session_id = self.generate_session_id(user_id)
        device_type = random.choice(config.DEVICE_TYPES)
        platform = random.choice(config.PLATFORMS)
        country = random.choice(config.USER_COUNTRIES)
        
        # Select error type based on configured rates
        error_type = random.choices(
            list(config.ERROR_RATES.keys()),
            weights=list(config.ERROR_RATES.values())
        )[0]
        
        error_messages = {
            "network_error": [
                "Network connection timeout",
                "Failed to establish connection",
                "Connection lost during playback"
            ],
            "playback_error": [
                "Media playback failed",
                "Video codec not supported",
                "Audio stream error"
            ],
            "authentication_error": [
                "Invalid authentication token",
                "Session expired",
                "Access denied"
            ],
            "content_not_found": [
                "Content not available",
                "Video not found",
                "Stream unavailable"
            ]
        }
        
        log_data = {
            "timestamp": datetime.now(),
            "log_type": "error",
            "log_level": "ERROR",
            "user_id": user_id,
            "session_id": session_id,
            "content_id": self.generate_content_id(),
            "content_title": random.choice(config.CONTENT_TITLES),
            "content_type": random.choice(config.CONTENT_TYPES),
            "device_type": device_type,
            "platform": platform,
            "country": country,
            "ip_address": self.generate_ip_address(),
            "user_agent": self.generate_user_agent(platform),
            "error_type": error_type,
            "error_message": random.choice(error_messages.get(error_type, ["Unknown error"])),
            "response_time": random.randint(config.RESPONSE_TIME_RANGE[0], config.RESPONSE_TIME_RANGE[1])
        }
        
        return log_data
    
    def generate_seek_log(self, user_id: str = None) -> Dict[str, Any]:
        """Generate a seek event log"""
        if user_id is None:
            user_id = random.choice(list(self.user_sessions.keys())) if self.user_sessions else self.generate_user_id()
        
        session_data = self.user_sessions.get(user_id, {})
        session_id = session_data.get("session_id", self.generate_session_id(user_id))
        
        log_data = {
            "timestamp": datetime.now(),
            "log_type": "seek",
            "log_level": "INFO",
            "user_id": user_id,
            "session_id": session_id,
            "content_id": self.generate_content_id(),
            "content_title": random.choice(config.CONTENT_TITLES),
            "content_type": random.choice(config.CONTENT_TYPES),
            "device_type": session_data.get("device_type", random.choice(config.DEVICE_TYPES)),
            "platform": session_data.get("platform", random.choice(config.PLATFORMS)),
            "country": session_data.get("country", random.choice(config.USER_COUNTRIES)),
            "ip_address": self.generate_ip_address(),
            "user_agent": self.generate_user_agent(session_data.get("platform", "web")),
            "position": random.randint(0, 7200),
            "response_time": random.randint(config.RESPONSE_TIME_RANGE[0], config.RESPONSE_TIME_RANGE[1])
        }
        
        return log_data
    
    def generate_quality_change_log(self, user_id: str = None) -> Dict[str, Any]:
        """Generate a quality change event log"""
        if user_id is None:
            user_id = random.choice(list(self.user_sessions.keys())) if self.user_sessions else self.generate_user_id()
        
        session_data = self.user_sessions.get(user_id, {})
        session_id = session_data.get("session_id", self.generate_session_id(user_id))
        
        qualities = ["240p", "360p", "480p", "720p", "1080p", "4K"]
        from_quality = random.choice(qualities)
        to_quality = random.choice([q for q in qualities if q != from_quality])
        
        log_data = {
            "timestamp": datetime.now(),
            "log_type": "quality_change",
            "log_level": "INFO",
            "user_id": user_id,
            "session_id": session_id,
            "content_id": self.generate_content_id(),
            "content_title": random.choice(config.CONTENT_TITLES),
            "content_type": random.choice(config.CONTENT_TYPES),
            "device_type": session_data.get("device_type", random.choice(config.DEVICE_TYPES)),
            "platform": session_data.get("platform", random.choice(config.PLATFORMS)),
            "country": session_data.get("country", random.choice(config.USER_COUNTRIES)),
            "ip_address": self.generate_ip_address(),
            "user_agent": self.generate_user_agent(session_data.get("platform", "web")),
            "quality": to_quality,
            "response_time": random.randint(config.RESPONSE_TIME_RANGE[0], config.RESPONSE_TIME_RANGE[1])
        }
        
        return log_data
    
    def generate_log_batch(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        """Generate a batch of logs with realistic distribution"""
        logs = []
        
        for _ in range(batch_size):
            # Weighted selection of log types
            log_type = random.choices(
                config.LOG_TYPES,
                weights=[0.6, 0.2, 0.05, 0.1, 0.03, 0.02]  # play, pause, stop, error, seek, quality_change
            )[0]
            
            if log_type == "play":
                logs.append(self.generate_play_log())
            elif log_type == "pause":
                logs.append(self.generate_pause_log())
            elif log_type == "stop":
                # Similar to pause but with stop type
                log_data = self.generate_pause_log()
                log_data["log_type"] = "stop"
                logs.append(log_data)
            elif log_type == "error":
                logs.append(self.generate_error_log())
            elif log_type == "seek":
                logs.append(self.generate_seek_log())
            elif log_type == "quality_change":
                logs.append(self.generate_quality_change_log())
        
        return logs
    
    def produce_logs(self, duration_minutes: int = 60, rate_per_second: int = None):
        """Produce logs continuously for the specified duration"""
        rate_per_second = rate_per_second or config.LOG_GENERATION_RATE
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        
        logger.info(f"Starting log production for {duration_minutes} minutes at {rate_per_second} logs/second")
        logger.info(f"End time: {end_time}")
        
        total_logs = 0
        
        try:
            while datetime.now() < end_time:
                # Generate batch of logs
                batch = self.generate_log_batch(rate_per_second)
                
                # Insert logs into database
                for log_data in batch:
                    try:
                        # Parse and validate log
                        parsed_log = self.log_parser.parse_log_entry(log_data)
                        
                        # Insert into database
                        log_id = self.db_manager.insert_raw_log(parsed_log)
                        total_logs += 1
                        
                        if total_logs % 100 == 0:
                            logger.info(f"Produced {total_logs} logs so far...")
                            
                    except Exception as e:
                        logger.error(f"Error processing log: {e}")
                        continue
                
                # Sleep for 1 second
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Log production interrupted by user")
        
        logger.info(f"Log production completed. Total logs produced: {total_logs}")

def main():
    """Main function to run the log producer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Streaming Platform Log Producer")
    parser.add_argument("--duration", type=int, default=60, 
                       help="Duration in minutes to produce logs (default: 60)")
    parser.add_argument("--rate", type=int, default=config.LOG_GENERATION_RATE,
                       help=f"Logs per second (default: {config.LOG_GENERATION_RATE})")
    
    args = parser.parse_args()
    
    producer = StreamingLogProducer()
    producer.produce_logs(duration_minutes=args.duration, rate_per_second=args.rate)

if __name__ == "__main__":
    main() 