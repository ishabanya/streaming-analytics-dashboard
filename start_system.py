#!/usr/bin/env python3
"""
Startup script for the Streaming Platform ETL System
Initializes the database and provides startup instructions
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_banner():
    """Print system banner"""
    print("=" * 80)
    print("🎬 STREAMING PLATFORM ETL + DASHBOARD SYSTEM")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'streamlit', 'pandas', 'plotly', 'sqlalchemy', 
        'numpy', 'python-dateutil', 'faker'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def initialize_database():
    """Initialize the database"""
    print("\n🗄️  Initializing database...")
    
    try:
        result = subprocess.run([sys.executable, "init_database.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Database initialized successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Database initialization failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def print_startup_instructions():
    """Print instructions for starting the system"""
    print("\n" + "=" * 80)
    print("🚀 SYSTEM STARTUP INSTRUCTIONS")
    print("=" * 80)
    print("To run the complete system, open 3 terminal windows and run:")
    print()
    print("Terminal 1 - ETL Pipeline:")
    print("  python etl_pipeline.py")
    print()
    print("Terminal 2 - Log Producer:")
    print("  python log_producer.py")
    print()
    print("Terminal 3 - Dashboard:")
    print("  streamlit run dashboard.py")
    print()
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("=" * 80)

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before continuing.")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        print("\n❌ Database initialization failed. Please check the error messages.")
        sys.exit(1)
    
    # Print startup instructions
    print_startup_instructions()
    
    print("\n🎉 System is ready to start!")
    print("Follow the instructions above to launch the complete system.")

if __name__ == "__main__":
    main() 