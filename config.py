# Configuration file for Smart Task Scheduler
# Copy this file and replace with your actual API key

# OpenWeatherMap API Key
# Get your free API key from: https://openweathermap.org/api
WEATHER_API_KEY = "5a081e357069900f70cdb55c8a39af86"

# Weather API base URL
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Default location for weather (if not specified)
DEFAULT_LOCATION = "New York"

# Notification settings
NOTIFICATION_TIMEOUT = 10  # seconds
NOTIFICATION_TITLE = "Task Reminder"

# GUI settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
UPDATE_INTERVAL = 60000  # milliseconds (1 minute)

# Task storage
TASKS_FILE = "tasks.json"
