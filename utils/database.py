"""
Database utilities for the Streaming Platform ETL System
"""

import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any, Optional
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database operations for the streaming platform ETL system"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.DATABASE_PATH
        self.engine = create_engine(config.DATABASE_URL)
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with self.engine.connect() as conn:
                # Create raw_logs table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS raw_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        log_type VARCHAR(50) NOT NULL,
                        log_level VARCHAR(20) NOT NULL,
                        user_id VARCHAR(100),
                        session_id VARCHAR(100),
                        content_id VARCHAR(100),
                        content_title VARCHAR(255),
                        content_type VARCHAR(50),
                        device_type VARCHAR(50),
                        platform VARCHAR(50),
                        country VARCHAR(10),
                        ip_address VARCHAR(45),
                        user_agent TEXT,
                        duration INTEGER,
                        position INTEGER,
                        quality VARCHAR(20),
                        error_type VARCHAR(100),
                        error_message TEXT,
                        response_time INTEGER,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create processed_logs table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS processed_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        raw_log_id INTEGER,
                        timestamp DATETIME NOT NULL,
                        event_type VARCHAR(50) NOT NULL,
                        user_id VARCHAR(100),
                        content_id VARCHAR(100),
                        content_title VARCHAR(255),
                        device_type VARCHAR(50),
                        platform VARCHAR(50),
                        country VARCHAR(10),
                        duration INTEGER,
                        quality VARCHAR(20),
                        error_type VARCHAR(100),
                        response_time INTEGER,
                        processed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (raw_log_id) REFERENCES raw_logs (id)
                    )
                """))
                
                # Create metrics table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        metric_name VARCHAR(100) NOT NULL,
                        metric_value REAL NOT NULL,
                        metric_unit VARCHAR(20),
                        timestamp DATETIME NOT NULL,
                        time_window VARCHAR(20),
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create indexes for better performance
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_raw_logs_timestamp ON raw_logs(timestamp)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_raw_logs_log_type ON raw_logs(log_type)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_raw_logs_content_title ON raw_logs(content_title)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_processed_logs_timestamp ON processed_logs(timestamp)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)"))
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def insert_raw_log(self, log_data: Dict[str, Any]) -> int:
        """Insert a raw log entry"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    INSERT INTO raw_logs (
                        timestamp, log_type, log_level, user_id, session_id,
                        content_id, content_title, content_type, device_type,
                        platform, country, ip_address, user_agent, duration,
                        position, quality, error_type, error_message, response_time
                    ) VALUES (
                        :timestamp, :log_type, :log_level, :user_id, :session_id,
                        :content_id, :content_title, :content_type, :device_type,
                        :platform, :country, :ip_address, :user_agent, :duration,
                        :position, :quality, :error_type, :error_message, :response_time
                    )
                """), log_data)
                conn.commit()
                return result.lastrowid
        except Exception as e:
            logger.error(f"Error inserting raw log: {e}")
            raise
    
    def insert_processed_log(self, log_data: Dict[str, Any]) -> int:
        """Insert a processed log entry"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    INSERT INTO processed_logs (
                        raw_log_id, timestamp, event_type, user_id, content_id,
                        content_title, device_type, platform, country, duration,
                        quality, error_type, response_time
                    ) VALUES (
                        :raw_log_id, :timestamp, :event_type, :user_id, :content_id,
                        :content_title, :device_type, :platform, :country, :duration,
                        :quality, :error_type, :response_time
                    )
                """), log_data)
                conn.commit()
                return result.lastrowid
        except Exception as e:
            logger.error(f"Error inserting processed log: {e}")
            raise
    
    def insert_metric(self, metric_data: Dict[str, Any]) -> int:
        """Insert a metric entry"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    INSERT INTO metrics (
                        metric_name, metric_value, metric_unit, timestamp, time_window
                    ) VALUES (
                        :metric_name, :metric_value, :metric_unit, :timestamp, :time_window
                    )
                """), metric_data)
                conn.commit()
                return result.lastrowid
        except Exception as e:
            logger.error(f"Error inserting metric: {e}")
            raise
    
    def get_logs_by_timeframe(self, start_time: datetime, end_time: datetime, 
                            table: str = "raw_logs", limit: int = 1000) -> pd.DataFrame:
        """Get logs within a specific timeframe"""
        try:
            query = f"""
                SELECT * FROM {table}
                WHERE timestamp BETWEEN :start_time AND :end_time
                ORDER BY timestamp DESC
                LIMIT :limit
            """
            with self.engine.connect() as conn:
                df = pd.read_sql_query(
                    text(query),
                    conn,
                    params={"start_time": start_time, "end_time": end_time, "limit": limit}
                )
            return df
        except Exception as e:
            logger.error(f"Error getting logs by timeframe: {e}")
            return pd.DataFrame()
    
    def get_metrics_by_timeframe(self, start_time: datetime, end_time: datetime,
                               metric_name: str = None) -> pd.DataFrame:
        """Get metrics within a specific timeframe"""
        try:
            query = """
                SELECT * FROM metrics
                WHERE timestamp BETWEEN :start_time AND :end_time
            """
            params = {"start_time": start_time, "end_time": end_time}
            
            if metric_name:
                query += " AND metric_name = :metric_name"
                params["metric_name"] = metric_name
            
            query += " ORDER BY timestamp DESC"
            
            with self.engine.connect() as conn:
                df = pd.read_sql_query(text(query), conn, params=params)
            return df
        except Exception as e:
            logger.error(f"Error getting metrics by timeframe: {e}")
            return pd.DataFrame()
    
    def cleanup_old_data(self, days: int = None):
        """Clean up old data based on retention policy"""
        days = days or config.RETENTION_DAYS
        cutoff_date = datetime.now() - timedelta(days=days)
        
        try:
            with self.engine.connect() as conn:
                # Delete old raw logs
                conn.execute(text("DELETE FROM raw_logs WHERE timestamp < :cutoff_date"), 
                           {"cutoff_date": cutoff_date})
                
                # Delete old processed logs
                conn.execute(text("DELETE FROM processed_logs WHERE timestamp < :cutoff_date"), 
                           {"cutoff_date": cutoff_date})
                
                # Delete old metrics
                conn.execute(text("DELETE FROM metrics WHERE timestamp < :cutoff_date"), 
                           {"cutoff_date": cutoff_date})
                
                conn.commit()
                logger.info(f"Cleaned up data older than {days} days")
                
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            raise
    
    def get_database_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        try:
            with self.engine.connect() as conn:
                stats = {}
                
                # Count records in each table
                for table in ["raw_logs", "processed_logs", "metrics"]:
                    result = conn.execute(text(f"SELECT COUNT(*) as count FROM {table}"))
                    stats[f"{table}_count"] = result.fetchone()[0]
                
                # Get latest timestamp
                for table in ["raw_logs", "processed_logs", "metrics"]:
                    result = conn.execute(text(f"SELECT MAX(timestamp) as latest FROM {table}"))
                    latest = result.fetchone()[0]
                    stats[f"{table}_latest"] = latest
                
                return stats
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}

# Global database manager instance
db_manager = DatabaseManager() 