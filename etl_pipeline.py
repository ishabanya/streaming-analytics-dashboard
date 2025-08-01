#!/usr/bin/env python3
"""
ETL Pipeline for the Streaming Platform ETL System
Processes raw logs and transforms them into analytics data
"""

import time
import logging
import sys
import os
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import threading

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import DatabaseManager
from utils.log_parser import LogParser
from utils.metrics import MetricsCalculator
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ETLPipeline:
    """Main ETL pipeline for processing streaming platform logs"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.log_parser = LogParser()
        self.metrics_calculator = MetricsCalculator()
        self.running = False
        self.processed_count = 0
        self.error_count = 0
        
    def process_raw_logs(self, limit: int = None) -> List[Dict[str, Any]]:
        """Process raw logs and transform them into analytics data"""
        try:
            # Get unprocessed raw logs
            end_time = datetime.now()
            start_time = end_time - timedelta(minutes=config.ETL_PROCESSING_INTERVAL)
            
            raw_logs_df = self.db_manager.get_logs_by_timeframe(
                start_time, end_time, table="raw_logs", limit=limit or config.BATCH_SIZE
            )
            
            if raw_logs_df.empty:
                return []
            
            processed_logs = []
            
            for _, row in raw_logs_df.iterrows():
                try:
                    # Convert row to dict
                    log_data = row.to_dict()
                    
                    # Extract event type
                    event_type = self.log_parser.extract_event_type(log_data)
                    
                    # Calculate duration if applicable
                    duration = self.log_parser.calculate_duration(log_data)
                    
                    # Parse error details if it's an error log
                    error_details = self.log_parser.parse_error_details(log_data)
                    
                    # Validate response time
                    response_time = self.log_parser.validate_response_time(log_data.get('response_time'))
                    
                    # Create processed log entry
                    processed_log = {
                        "raw_log_id": log_data.get('id'),
                        "timestamp": log_data.get('timestamp'),
                        "event_type": event_type,
                        "user_id": log_data.get('user_id'),
                        "content_id": log_data.get('content_id'),
                        "content_title": log_data.get('content_title'),
                        "device_type": log_data.get('device_type'),
                        "platform": log_data.get('platform'),
                        "country": log_data.get('country'),
                        "duration": duration,
                        "quality": log_data.get('quality'),
                        "error_type": error_details.get('error_type'),
                        "response_time": response_time
                    }
                    
                    # Insert processed log
                    processed_log_id = self.db_manager.insert_processed_log(processed_log)
                    processed_logs.append(processed_log)
                    
                    self.processed_count += 1
                    
                except Exception as e:
                    logger.error(f"Error processing log {log_data.get('id')}: {e}")
                    self.error_count += 1
                    continue
            
            return processed_logs
            
        except Exception as e:
            logger.error(f"Error in process_raw_logs: {e}")
            return []
    
    def calculate_and_store_metrics(self, logs_df: pd.DataFrame):
        """Calculate metrics and store them in the database"""
        try:
            if logs_df.empty:
                return
            
            # Calculate all metrics
            metrics = self.metrics_calculator.get_all_metrics(logs_df)
            
            # Store metrics in database
            for metric_name, metric_data in metrics.items():
                if metric_name == 'calculated_at' or metric_name == 'time_series':
                    continue
                
                if isinstance(metric_data, dict) and 'plays_per_minute' in metric_data:
                    # Store plays per minute metric
                    self.db_manager.insert_metric({
                        "metric_name": "plays_per_minute",
                        "metric_value": metric_data['plays_per_minute'],
                        "metric_unit": "plays/min",
                        "timestamp": datetime.now(),
                        "time_window": f"{metric_data['time_window']}m"
                    })
                
                elif isinstance(metric_data, dict) and 'error_rate' in metric_data:
                    # Store error rate metric
                    self.db_manager.insert_metric({
                        "metric_name": "error_rate",
                        "metric_value": metric_data['error_rate'],
                        "metric_unit": "%",
                        "timestamp": datetime.now(),
                        "time_window": f"{metric_data['time_window']}m"
                    })
                
                elif isinstance(metric_data, dict) and 'active_users' in metric_data:
                    # Store user engagement metrics
                    self.db_manager.insert_metric({
                        "metric_name": "active_users",
                        "metric_value": metric_data['active_users'],
                        "metric_unit": "users",
                        "timestamp": datetime.now(),
                        "time_window": "5m"
                    })
                    
                    self.db_manager.insert_metric({
                        "metric_name": "avg_session_duration",
                        "metric_value": metric_data['avg_session_duration'],
                        "metric_unit": "seconds",
                        "timestamp": datetime.now(),
                        "time_window": "5m"
                    })
                
                elif isinstance(metric_data, dict) and 'avg_response_time' in metric_data:
                    # Store performance metrics
                    self.db_manager.insert_metric({
                        "metric_name": "avg_response_time",
                        "metric_value": metric_data['avg_response_time'],
                        "metric_unit": "ms",
                        "timestamp": datetime.now(),
                        "time_window": "5m"
                    })
            
            logger.info(f"Calculated and stored {len(metrics)} metric categories")
            
        except Exception as e:
            logger.error(f"Error calculating and storing metrics: {e}")
    
    def cleanup_old_data(self):
        """Clean up old data based on retention policy"""
        try:
            self.db_manager.cleanup_old_data()
            logger.info("Data cleanup completed")
        except Exception as e:
            logger.error(f"Error during data cleanup: {e}")
    
    def run_etl_cycle(self):
        """Run one ETL processing cycle"""
        try:
            # Process raw logs
            processed_logs = self.process_raw_logs()
            
            if processed_logs:
                logger.info(f"Processed {len(processed_logs)} logs in this cycle")
                
                # Get recent logs for metrics calculation
                end_time = datetime.now()
                start_time = end_time - timedelta(minutes=30)  # Last 30 minutes
                
                recent_logs_df = self.db_manager.get_logs_by_timeframe(
                    start_time, end_time, table="processed_logs"
                )
                
                # Calculate and store metrics
                self.calculate_and_store_metrics(recent_logs_df)
            
            # Periodic cleanup (every 10 cycles)
            if self.processed_count % (config.BATCH_SIZE * 10) == 0:
                self.cleanup_old_data()
                
        except Exception as e:
            logger.error(f"Error in ETL cycle: {e}")
    
    def start_pipeline(self):
        """Start the ETL pipeline"""
        self.running = True
        logger.info("Starting ETL pipeline...")
        
        try:
            while self.running:
                start_time = time.time()
                
                # Run ETL cycle
                self.run_etl_cycle()
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                # Log statistics
                if self.processed_count % 100 == 0:
                    logger.info(f"ETL Statistics - Processed: {self.processed_count}, "
                              f"Errors: {self.error_count}, "
                              f"Cycle time: {processing_time:.2f}s")
                
                # Sleep until next cycle
                sleep_time = max(0, config.ETL_PROCESSING_INTERVAL - processing_time)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            logger.info("ETL pipeline interrupted by user")
        except Exception as e:
            logger.error(f"ETL pipeline error: {e}")
        finally:
            self.running = False
            logger.info("ETL pipeline stopped")
    
    def stop_pipeline(self):
        """Stop the ETL pipeline"""
        self.running = False
        logger.info("Stopping ETL pipeline...")
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        return {
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "success_rate": ((self.processed_count - self.error_count) / self.processed_count * 100) 
                           if self.processed_count > 0 else 0,
            "running": self.running,
            "last_update": datetime.now().isoformat()
        }

def main():
    """Main function to run the ETL pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Streaming Platform ETL Pipeline")
    parser.add_argument("--continuous", action="store_true", default=True,
                       help="Run pipeline continuously (default: True)")
    parser.add_argument("--cycles", type=int, default=1,
                       help="Number of ETL cycles to run (default: 1)")
    
    args = parser.parse_args()
    
    pipeline = ETLPipeline()
    
    if args.continuous:
        # Run continuously
        pipeline.start_pipeline()
    else:
        # Run specified number of cycles
        for i in range(args.cycles):
            logger.info(f"Running ETL cycle {i + 1}/{args.cycles}")
            pipeline.run_etl_cycle()
            time.sleep(config.ETL_PROCESSING_INTERVAL)
        
        # Print final statistics
        stats = pipeline.get_pipeline_stats()
        logger.info("Final ETL Statistics:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")

if __name__ == "__main__":
    main() 