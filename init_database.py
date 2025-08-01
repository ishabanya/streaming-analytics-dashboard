#!/usr/bin/env python3
"""
Database initialization script for the Streaming Platform ETL System
"""

import os
import sys
import logging
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import DatabaseManager
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Initialize the database and create all necessary tables"""
    try:
        logger.info("Starting database initialization...")
        
        # Create data directory if it doesn't exist
        os.makedirs(config.DATA_DIR, exist_ok=True)
        logger.info(f"Data directory created/verified: {config.DATA_DIR}")
        
        # Initialize database manager
        db_manager = DatabaseManager()
        logger.info("Database manager initialized successfully")
        
        # Get database statistics
        stats = db_manager.get_database_stats()
        logger.info("Database statistics:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
        
        logger.info("Database initialization completed successfully!")
        
        # Print database path
        logger.info(f"Database location: {os.path.abspath(config.DATABASE_PATH)}")
        
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 