"""
Log parsing utilities for the Streaming Platform ETL System
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging
import config

logger = logging.getLogger(__name__)

class LogParser:
    """Parser for streaming platform log data"""
    
    def __init__(self):
        self.log_patterns = {
            'play': r'play.*content_id=(\w+).*position=(\d+)',
            'pause': r'pause.*content_id=(\w+).*position=(\d+)',
            'stop': r'stop.*content_id=(\w+).*duration=(\d+)',
            'error': r'error.*type=(\w+).*message=(.+)',
            'seek': r'seek.*content_id=(\w+).*from=(\d+).*to=(\d+)',
            'quality_change': r'quality_change.*content_id=(\w+).*from=(\w+).*to=(\w+)'
        }
    
    def parse_log_entry(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and validate a log entry"""
        try:
            # Validate required fields
            required_fields = ['timestamp', 'log_type', 'log_level']
            for field in required_fields:
                if field not in log_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Parse timestamp
            if isinstance(log_data['timestamp'], str):
                log_data['timestamp'] = datetime.fromisoformat(log_data['timestamp'].replace('Z', '+00:00'))
            
            # Validate log type
            if log_data['log_type'] not in config.LOG_TYPES:
                raise ValueError(f"Invalid log type: {log_data['log_type']}")
            
            # Validate log level
            if log_data['log_level'] not in config.LOG_LEVELS:
                raise ValueError(f"Invalid log level: {log_data['log_level']}")
            
            # Enrich log data with additional fields
            enriched_data = self._enrich_log_data(log_data)
            
            # Validate content-specific fields
            self._validate_content_fields(enriched_data)
            
            return enriched_data
            
        except Exception as e:
            logger.error(f"Error parsing log entry: {e}")
            raise
    
    def _enrich_log_data(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich log data with additional fields"""
        enriched = log_data.copy()
        
        # Add default values for optional fields
        enriched.setdefault('user_id', None)
        enriched.setdefault('session_id', None)
        enriched.setdefault('content_id', None)
        enriched.setdefault('content_title', None)
        enriched.setdefault('content_type', None)
        enriched.setdefault('device_type', None)
        enriched.setdefault('platform', None)
        enriched.setdefault('country', None)
        enriched.setdefault('ip_address', None)
        enriched.setdefault('user_agent', None)
        enriched.setdefault('duration', None)
        enriched.setdefault('position', None)
        enriched.setdefault('quality', None)
        enriched.setdefault('error_type', None)
        enriched.setdefault('error_message', None)
        enriched.setdefault('response_time', None)
        
        # Generate session ID if not provided
        if not enriched.get('session_id') and enriched.get('user_id'):
            enriched['session_id'] = f"{enriched['user_id']}_{int(enriched['timestamp'].timestamp())}"
        
        return enriched
    
    def _validate_content_fields(self, log_data: Dict[str, Any]):
        """Validate content-specific fields"""
        # Validate content title if provided
        if log_data.get('content_title') and log_data['content_title'] not in config.CONTENT_TITLES:
            logger.warning(f"Unknown content title: {log_data['content_title']}")
        
        # Validate content type if provided
        if log_data.get('content_type') and log_data['content_type'] not in config.CONTENT_TYPES:
            logger.warning(f"Unknown content type: {log_data['content_type']}")
        
        # Validate device type if provided
        if log_data.get('device_type') and log_data['device_type'] not in config.DEVICE_TYPES:
            logger.warning(f"Unknown device type: {log_data['device_type']}")
        
        # Validate platform if provided
        if log_data.get('platform') and log_data['platform'] not in config.PLATFORMS:
            logger.warning(f"Unknown platform: {log_data['platform']}")
        
        # Validate country if provided
        if log_data.get('country') and log_data['country'] not in config.USER_COUNTRIES:
            logger.warning(f"Unknown country: {log_data['country']}")
    
    def extract_event_type(self, log_data: Dict[str, Any]) -> str:
        """Extract event type from log data"""
        log_type = log_data.get('log_type', '')
        
        # Map log types to event types
        event_mapping = {
            'play': 'play_started',
            'pause': 'playback_paused',
            'stop': 'playback_stopped',
            'error': 'playback_error',
            'seek': 'playback_seek',
            'quality_change': 'quality_changed'
        }
        
        return event_mapping.get(log_type, 'unknown_event')
    
    def calculate_duration(self, log_data: Dict[str, Any]) -> Optional[int]:
        """Calculate duration for playback events"""
        if log_data.get('log_type') in ['play', 'pause', 'stop']:
            # For demo purposes, generate a random duration
            import random
            return random.randint(1, 3600)  # 1 second to 1 hour
        return None
    
    def parse_error_details(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse error details from log data"""
        error_details = {
            'error_type': log_data.get('error_type'),
            'error_message': log_data.get('error_message')
        }
        
        # Extract error type from message if not explicitly provided
        if not error_details['error_type'] and error_details['error_message']:
            error_message = error_details['error_message'].lower()
            
            if 'network' in error_message or 'connection' in error_message:
                error_details['error_type'] = 'network_error'
            elif 'playback' in error_message or 'media' in error_message:
                error_details['error_type'] = 'playback_error'
            elif 'auth' in error_message or 'login' in error_message:
                error_details['error_type'] = 'authentication_error'
            elif 'not found' in error_message or '404' in error_message:
                error_details['error_type'] = 'content_not_found'
            else:
                error_details['error_type'] = 'unknown_error'
        
        return error_details
    
    def validate_response_time(self, response_time: Optional[int]) -> Optional[int]:
        """Validate and normalize response time"""
        if response_time is None:
            return None
        
        min_time, max_time = config.RESPONSE_TIME_RANGE
        
        if response_time < min_time:
            logger.warning(f"Response time too low: {response_time}ms, setting to {min_time}ms")
            return min_time
        elif response_time > max_time:
            logger.warning(f"Response time too high: {response_time}ms, setting to {max_time}ms")
            return max_time
        
        return response_time
    
    def parse_log_batch(self, log_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse a batch of log entries"""
        parsed_logs = []
        
        for log_entry in log_batch:
            try:
                parsed_log = self.parse_log_entry(log_entry)
                parsed_logs.append(parsed_log)
            except Exception as e:
                logger.error(f"Failed to parse log entry: {e}")
                # Continue processing other logs
                continue
        
        return parsed_logs

# Global log parser instance
log_parser = LogParser() 