#!/usr/bin/env python3
"""
Deployment script for ResQConnect
This script helps set up and run the application with proper configuration
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_prerequisites():
    """Check if required tools are available"""
    print("Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    
    # Check if pip is available
    try:
        import pip
    except ImportError:
        print("❌ pip is required")
        return False
    
    print("✅ Prerequisites check passed")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_config():
    """Create a sample config.json file if it doesn't exist"""
    config_path = Path("config.json")
    
    if config_path.exists():
        print("✅ config.json already exists")
        return True
    
    print("Creating sample config.json file...")
    
    sample_config = {
        "params": {
            "mongo_uri": "mongodb://localhost:27017/emergencyDB"
        }
    }
    
    try:
        with open(config_path, 'w') as f:
            json.dump(sample_config, f, indent=2)
        print("✅ Sample config.json created. Please update it with your actual configuration.")
        return True
    except Exception as e:
        print(f"❌ Failed to create config.json: {e}")
        return False

def run_application():
    """Run the Flask application"""
    print("Starting ResQConnect application...")
    try:
        subprocess.check_call([sys.executable, "main.py"])
    except subprocess.CalledProcessError:
        print("❌ Failed to start application")
        return False
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        return True

def main():
    """Main deployment function"""
    print("🚀 ResQConnect Deployment Script")
    print("=" * 40)
    
    if not check_prerequisites():
        return False
    
    if not install_dependencies():
        return False
    
    if not create_config():
        return False
    
    print("\n✅ Setup completed successfully!")
    print("💡 To run the application manually, use: python main.py")
    print("💡 For production, use: gunicorn -w 4 -b 0.0.0.0:5000 main:app")
    
    response = input("\nWould you like to start the application now? (y/n): ")
    if response.lower() in ['y', 'yes']:
        run_application()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)