#!/usr/bin/env python3
"""
Demo script for Smart Task Scheduler
Shows the key features and functionality
"""

import sys
import os
import json
from datetime import datetime, timedelta
import time

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_task_creation():
    """Demonstrate task creation without GUI"""
    print("=== Smart Task Scheduler Demo ===\n")
    
    # Sample tasks for demonstration
    demo_tasks = [
        {
            'id': 1,
            'description': 'Team meeting with project stakeholders',
            'type': 'Meeting',
            'datetime': (datetime.now() + timedelta(hours=2)).isoformat(),
            'location': 'New York',
            'status': 'Scheduled',
            'weather_info': None
        },
        {
            'id': 2,
            'description': 'Morning run in the park (Weather: 18°C, Partly Cloudy)',
            'type': 'Outdoor Activity',
            'datetime': (datetime.now() + timedelta(hours=4)).isoformat(),
            'location': 'New York',
            'status': 'Scheduled',
            'weather_info': '18°C, Partly Cloudy'
        },
        {
            'id': 3,
            'description': 'Complete project documentation',
            'type': 'General',
            'datetime': (datetime.now() + timedelta(days=1)).isoformat(),
            'location': 'New York',
            'status': 'Scheduled',
            'weather_info': None
        }
    ]
    
    print("Sample Tasks Created:")
    print("-" * 50)
    
    for task in demo_tasks:
        task_datetime = datetime.fromisoformat(task['datetime'])
        print(f"Task: {task['description']}")
        print(f"Type: {task['type']}")
        print(f"Due: {task_datetime.strftime('%Y-%m-%d %H:%M')}")
        print(f"Status: {task['status']}")
        if task['weather_info']:
            print(f"Weather Info: {task['weather_info']}")
        print("-" * 50)
    
    # Save demo tasks
    with open('tasks.json', 'w') as f:
        json.dump(demo_tasks, f, indent=2)
    
    print(f"\n✓ {len(demo_tasks)} demo tasks saved to tasks.json")
    
    return demo_tasks

def demo_api_integration():
    """Demonstrate API integration capabilities"""
    print("\n=== API Integration Demo ===\n")
    
    try:
        import config
        import requests
        from dateutil import parser
        
        if config.WEATHER_API_KEY == "YOUR_API_KEY_HERE":
            print("⚠️  Weather API key not configured")
            print("To see weather integration:")
            print("1. Get API key from https://openweathermap.org/api")
            print("2. Edit config.py and replace YOUR_API_KEY_HERE")
            print("3. Run the application again")
        else:
            print("✓ Weather API key is configured")
            print("✓ Ready to fetch weather data for outdoor activities")
            
            # Test API connection
            try:
                params = {
                    'q': config.DEFAULT_LOCATION,
                    'appid': config.WEATHER_API_KEY,
                    'units': 'metric'
                }
                response = requests.get(config.WEATHER_BASE_URL, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    temp = data['main']['temp']
                    description = data['weather'][0]['description'].title()
                    print(f"✓ API test successful: {temp}°C, {description}")
                else:
                    print("⚠️  API test failed - check your API key")
            except Exception as e:
                print(f"⚠️  API test failed: {e}")
    
    except ImportError:
        print("✗ Missing dependencies - run: pip install -r requirements.txt")

def demo_notification_system():
    """Demonstrate notification system"""
    print("\n=== Notification System Demo ===\n")
    
    try:
        from plyer import notification
        
        print("✓ Notification library available")
        print("✓ Desktop notifications will appear when tasks are due")
        print("✓ Notifications include task description and timing")
        
        # Test notification (optional)
        print("\nWould you like to test a notification now? (y/n): ", end="")
        try:
            choice = input().lower().strip()
            if choice == 'y':
                notification.notify(
                    title="Test Notification",
                    message="This is a test notification from Smart Task Scheduler!",
                    timeout=5
                )
                print("✓ Test notification sent!")
            else:
                print("Skipping notification test")
        except KeyboardInterrupt:
            print("\nSkipping notification test")
    
    except ImportError:
        print("⚠️  Notification library not available")
        print("Install with: pip install plyer")

def demo_scheduling_system():
    """Demonstrate scheduling capabilities"""
    print("\n=== Scheduling System Demo ===\n")
    
    try:
        import schedule
        
        print("✓ Schedule library available")
        print("✓ Tasks are automatically scheduled in background")
        print("✓ Multi-threaded design prevents GUI blocking")
        print("✓ Persistent scheduling across application restarts")
        
        # Show scheduling logic
        print("\nScheduling Features:")
        print("- Tasks scheduled for specific date/time")
        print("- Background thread runs scheduler continuously")
        print("- Automatic status updates when notifications sent")
        print("- JSON persistence for task storage")
    
    except ImportError:
        print("⚠️  Schedule library not available")
        print("Install with: pip install schedule")

def show_portfolio_highlights():
    """Show key portfolio features"""
    print("\n=== Portfolio Highlights ===\n")
    
    features = [
        "✅ API Integration - OpenWeatherMap API for weather data",
        "✅ GUI Development - Clean Tkinter interface with modern design",
        "✅ Background Processing - Multi-threaded scheduling system",
        "✅ Data Persistence - JSON-based task storage",
        "✅ Cross-platform Notifications - Native system alerts",
        "✅ Error Handling - Robust exception management",
        "✅ Configuration Management - Separate config file",
        "✅ User Experience - Intuitive workflow and feedback",
        "✅ Code Quality - Clean, modular architecture",
        "✅ Documentation - Comprehensive README and inline comments"
    ]
    
    for feature in features:
        print(feature)
    
    print(f"\n📊 Project Statistics:")
    print(f"- Lines of Code: ~300+")
    print(f"- Dependencies: 4 core libraries")
    print(f"- Files: 5 main project files")
    print(f"- Features: 10+ key capabilities")

def main():
    """Run the complete demo"""
    print("🚀 Smart Task Scheduler - Portfolio Demo")
    print("=" * 50)
    
    # Run all demo sections
    demo_task_creation()
    demo_api_integration()
    demo_notification_system()
    demo_scheduling_system()
    show_portfolio_highlights()
    
    print("\n" + "=" * 50)
    print("🎯 Demo Complete!")
    print("\nNext Steps:")
    print("1. Run 'python main.py' to start the GUI application")
    print("2. Configure your OpenWeatherMap API key for weather features")
    print("3. Add your own tasks and test the notification system")
    print("4. Take screenshots for your portfolio")
    print("\nPerfect for showcasing Python development skills on Upwork! 🌟")

if __name__ == "__main__":
    main()
