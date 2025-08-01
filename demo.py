#!/usr/bin/env python3
"""
Demo script for the Streaming Platform ETL System
Demonstrates the system capabilities with sample data
"""

import time
import threading
import subprocess
import sys
import os
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from log_producer import StreamingLogProducer
from etl_pipeline import ETLPipeline
import config

class SystemDemo:
    """Demo class for the streaming platform ETL system"""
    
    def __init__(self):
        self.producer = StreamingLogProducer()
        self.pipeline = ETLPipeline()
        self.running = False
        
    def generate_demo_data(self, duration_minutes: int = 5, rate_per_second: int = 5):
        """Generate demo data for a specified duration"""
        print(f"🎬 Generating demo data for {duration_minutes} minutes at {rate_per_second} logs/second...")
        
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        total_logs = 0
        
        try:
            while datetime.now() < end_time:
                # Generate batch of logs
                batch = self.producer.generate_log_batch(rate_per_second)
                
                # Insert logs into database
                for log_data in batch:
                    try:
                        # Parse and validate log
                        parsed_log = self.producer.log_parser.parse_log_entry(log_data)
                        
                        # Insert into database
                        log_id = self.producer.db_manager.insert_raw_log(parsed_log)
                        total_logs += 1
                        
                        if total_logs % 50 == 0:
                            print(f"📊 Generated {total_logs} logs...")
                            
                    except Exception as e:
                        print(f"❌ Error processing log: {e}")
                        continue
                
                # Sleep for 1 second
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("⏹️  Demo data generation interrupted")
        
        print(f"✅ Demo data generation completed. Total logs: {total_logs}")
        return total_logs
    
    def run_etl_demo(self, cycles: int = 10):
        """Run ETL pipeline demo"""
        print(f"🔄 Running ETL pipeline for {cycles} cycles...")
        
        for i in range(cycles):
            print(f"🔄 ETL Cycle {i + 1}/{cycles}")
            self.pipeline.run_etl_cycle()
            time.sleep(config.ETL_PROCESSING_INTERVAL)
        
        # Print final statistics
        stats = self.pipeline.get_pipeline_stats()
        print("📊 Final ETL Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    def show_system_stats(self):
        """Show system statistics"""
        print("\n📊 System Statistics:")
        
        # Database stats
        db_stats = self.producer.db_manager.get_database_stats()
        print("🗄️  Database Statistics:")
        for key, value in db_stats.items():
            print(f"  {key}: {value}")
        
        # Pipeline stats
        pipeline_stats = self.pipeline.get_pipeline_stats()
        print("\n🔄 Pipeline Statistics:")
        for key, value in pipeline_stats.items():
            print(f"  {key}: {value}")
    
    def run_full_demo(self, data_duration: int = 3, etl_cycles: int = 6):
        """Run a complete demo of the system"""
        print("🎬 Starting Streaming Platform ETL System Demo")
        print("=" * 60)
        
        # Step 1: Generate demo data
        print("\n📝 Step 1: Generating demo data...")
        total_logs = self.generate_demo_data(duration_minutes=data_duration, rate_per_second=3)
        
        # Step 2: Run ETL processing
        print("\n🔄 Step 2: Running ETL processing...")
        self.run_etl_demo(cycles=etl_cycles)
        
        # Step 3: Show statistics
        print("\n📊 Step 3: System Statistics")
        self.show_system_stats()
        
        print("\n✅ Demo completed successfully!")
        print("\n🚀 To view the dashboard, run:")
        print("   streamlit run dashboard.py")
        print("\n📊 Dashboard will be available at: http://localhost:8501")

def main():
    """Main demo function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Streaming Platform ETL System Demo")
    parser.add_argument("--data-duration", type=int, default=3,
                       help="Duration for data generation in minutes (default: 3)")
    parser.add_argument("--etl-cycles", type=int, default=6,
                       help="Number of ETL cycles to run (default: 6)")
    parser.add_argument("--log-rate", type=int, default=3,
                       help="Log generation rate per second (default: 3)")
    
    args = parser.parse_args()
    
    # Initialize demo
    demo = SystemDemo()
    
    # Run demo
    demo.run_full_demo(
        data_duration=args.data_duration,
        etl_cycles=args.etl_cycles
    )

if __name__ == "__main__":
    main() 