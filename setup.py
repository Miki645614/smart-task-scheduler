#!/usr/bin/env python3
"""
Setup script for Smart Task Scheduler
This script helps users get the application running quickly
"""

import os
import sys
import subprocess
import webbrowser

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def check_api_key():
    """Check if API key is configured"""
    try:
        import config
        if config.WEATHER_API_KEY == "YOUR_API_KEY_HERE":
            print("\n⚠️  Weather API key not configured")
            print("To enable weather features:")
            print("1. Visit https://openweathermap.org/api")
            print("2. Sign up for a free account")
            print("3. Get your API key")
            print("4. Edit config.py and replace YOUR_API_KEY_HERE")
            print("\nYou can still use the app without weather features.")
            return False
        else:
            print("✓ Weather API key is configured")
            return True
    except ImportError:
        print("✗ config.py file not found")
        return False

def run_application():
    """Run the main application"""
    print("\nStarting Smart Task Scheduler...")
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\nApplication closed by user")
    except Exception as e:
        print(f"Error running application: {e}")

def main():
    """Main setup process"""
    print("=== Smart Task Scheduler Setup ===\n")
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup failed. Please install dependencies manually:")
        print("pip install -r requirements.txt")
        return
    
    # Check API key
    api_configured = check_api_key()
    
    print("\n=== Setup Complete ===")
    print("✓ Python version compatible")
    print("✓ Dependencies installed")
    if api_configured:
        print("✓ Weather API configured")
    else:
        print("⚠️  Weather API not configured (optional)")
    
    print("\nWould you like to:")
    print("1. Run the application now")
    print("2. Get API key instructions")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            run_application()
            break
        elif choice == "2":
            print("\n=== Getting Weather API Key ===")
            print("1. Go to https://openweathermap.org/api")
            print("2. Click 'Get API key' and sign up")
            print("3. Verify your email if required")
            print("4. Copy your API key")
            print("5. Edit config.py")
            print("6. Replace 'YOUR_API_KEY_HERE' with your actual key")
            print("\nAfter configuring, run: python main.py")
            
            # Open the website
            try:
                webbrowser.open("https://openweathermap.org/api")
                print("\nOpening OpenWeatherMap in your browser...")
            except:
                pass
            break
        elif choice == "3":
            print("\nSetup complete! Run 'python main.py' to start the application.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
