import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime, timedelta
import json
import os
import schedule
import time
import threading
from plyer import notification
import requests
from dateutil import parser
import config

class SmartTaskScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Scheduler")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.resizable(True, True)
        
        # Set modern color scheme
        self.colors = {
            'bg_primary': '#2C3E50',      # Dark blue-gray
            'bg_secondary': '#34495E',    # Lighter blue-gray
            'bg_accent': '#3498DB',       # Bright blue
            'text_primary': '#ECF0F1',    # Light gray-white
            'text_secondary': '#BDC3C7',  # Medium gray
            'success': '#27AE60',         # Green
            'warning': '#E74C3C',         # Red
            'highlight': '#9B59B6',       # Purple
            'input_bg': '#ECF0F1',        # Light input background
            'input_text': '#2C3E50'       # Dark input text
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Set fonts
        self.fonts = {
            'title': font.Font(family='Segoe UI', size=16, weight='bold'),
            'header': font.Font(family='Segoe UI', size=12, weight='bold'),
            'normal': font.Font(family='Segoe UI', size=10),
            'button': font.Font(family='Segoe UI', size=10, weight='bold')
        }
        
        # Configure styles
        self.setup_styles()
        
        # Weather API configuration
        self.weather_api_key = config.WEATHER_API_KEY
        self.weather_base_url = config.WEATHER_BASE_URL
        
        # Tasks storage
        self.tasks_file = config.TASKS_FILE
        self.tasks = []
        
        # Create GUI
        self.create_widgets()
        
        # Load existing tasks
        self.load_tasks()
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        # Schedule periodic GUI updates
        self.update_gui()
    
    def setup_styles(self):
        """Setup modern styling for widgets"""
        style = ttk.Style()
        
        # Configure button styles
        style.configure('Modern.TButton',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=self.fonts['button'],
                       relief='flat')
        
        style.map('Modern.TButton',
                 background=[('active', '#2980B9')],
                 foreground=[('active', self.colors['text_primary'])])
        
        # Configure entry styles
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=1,
                       insertcolor=self.colors['input_text'])
        
        # Configure combobox styles
        style.configure('Modern.TCombobox',
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=1,
                       background=self.colors['input_bg'])
        
        # Configure treeview styles
        style.configure('Modern.Treeview',
                       background=self.colors['input_bg'],
                       foreground=self.colors['input_text'],
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=1)
        
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_primary'],
                       font=self.fonts['header'])
    
    def create_widgets(self):
        # Main container with gradient-like background
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title section
        title_frame = tk.Frame(main_container, bg=self.colors['bg_primary'], height=80)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        title_frame.pack_propagate(False)
        
        # App title with icon
        title_label = tk.Label(title_frame, 
                             text="📅 Smart Task Scheduler",
                             font=self.fonts['title'],
                             fg=self.colors['text_primary'],
                             bg=self.colors['bg_primary'])
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Status indicator
        self.status_label = tk.Label(title_frame,
                                    text="● Ready",
                                    font=self.fonts['normal'],
                                    fg=self.colors['success'],
                                    bg=self.colors['bg_primary'])
        self.status_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Main content area
        content_frame = tk.Frame(main_container, bg=self.colors['bg_secondary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Task input
        left_panel = tk.Frame(content_frame, bg=self.colors['bg_secondary'], width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(20, 10), pady=20)
        left_panel.pack_propagate(False)
        
        # Right panel - Task list
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_secondary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=20)
        
        # Create input section
        self.create_input_section(left_panel)
        
        # Create task list section
        self.create_task_list_section(right_panel)
    
    def create_input_section(self, parent):
        """Create the left panel input section"""
        # Section header
        header_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        header_label = tk.Label(header_frame, 
                               text="📝 Add New Task",
                               font=self.fonts['header'],
                               fg=self.colors['text_primary'],
                               bg=self.colors['bg_secondary'])
        header_label.pack(side=tk.LEFT)
        
        # Task Description
        desc_label = tk.Label(parent, 
                             text="Task Description:",
                             font=self.fonts['normal'],
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg_secondary'])
        desc_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.description_entry = ttk.Entry(parent, style='Modern.TEntry', width=35)
        self.description_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Task Type
        type_label = tk.Label(parent, 
                            text="Task Type:",
                            font=self.fonts['normal'],
                            fg=self.colors['text_secondary'],
                            bg=self.colors['bg_secondary'])
        type_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.task_type_var = tk.StringVar(value="General")
        self.task_type_combo = ttk.Combobox(parent, 
                                           textvariable=self.task_type_var,
                                           values=["General", "Meeting", "Outdoor Activity"],
                                           state="readonly",
                                           style='Modern.TCombobox',
                                           width=33)
        self.task_type_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Date and Time selection
        datetime_label = tk.Label(parent, 
                                 text="Schedule:",
                                 font=self.fonts['normal'],
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_secondary'])
        datetime_label.pack(anchor=tk.W, pady=(10, 5))
        
        datetime_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        datetime_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = ttk.Entry(datetime_frame, 
                                   textvariable=self.date_var,
                                   style='Modern.TEntry',
                                   width=15)
        self.date_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        date_label = tk.Label(datetime_frame, 
                             text="Date",
                             font=self.fonts['normal'],
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg_secondary'])
        date_label.pack(side=tk.LEFT, padx=(0, 15))
        
        self.time_var = tk.StringVar(value=datetime.now().strftime("%H:%M"))
        self.time_entry = ttk.Entry(datetime_frame, 
                                   textvariable=self.time_var,
                                   style='Modern.TEntry',
                                   width=10)
        self.time_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        time_label = tk.Label(datetime_frame, 
                             text="Time",
                             font=self.fonts['normal'],
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg_secondary'])
        time_label.pack(side=tk.LEFT)
        
        # Location (for weather)
        location_label = tk.Label(parent, 
                                  text="Location (for weather):",
                                  font=self.fonts['normal'],
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg_secondary'])
        location_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.location_entry = ttk.Entry(parent, style='Modern.TEntry', width=35)
        self.location_entry.pack(fill=tk.X, pady=(0, 15))
        self.location_entry.insert(0, config.DEFAULT_LOCATION)
        
        # Weather info display
        self.weather_info_label = tk.Label(parent, 
                                         text="",
                                         font=self.fonts['normal'],
                                         fg=self.colors['highlight'],
                                         bg=self.colors['bg_secondary'],
                                         wraplength=300)
        self.weather_info_label.pack(fill=tk.X, pady=(0, 15))
        
        # Add Task button
        self.add_button = tk.Button(parent, 
                                   text="➕ Add Task",
                                   bg=self.colors['bg_accent'],
                                   fg=self.colors['text_primary'],
                                   font=('Segoe UI', 10, 'bold'),
                                   relief='raised',
                                   bd=2,
                                   activebackground='#2980B9',
                                   activeforeground=self.colors['text_primary'],
                                   command=self.add_task)
        self.add_button.pack(fill=tk.X, pady=10, ipady=5)
        
        # Quick stats
        stats_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        stats_frame.pack(fill=tk.X, pady=20)
        
        self.stats_label = tk.Label(stats_frame, 
                                   text="📊 Total Tasks: 0",
                                   font=self.fonts['normal'],
                                   fg=self.colors['text_secondary'],
                                   bg=self.colors['bg_secondary'])
        self.stats_label.pack()
    
    def create_task_list_section(self, parent):
        """Create the right panel task list section"""
        # Section header
        header_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        header_label = tk.Label(header_frame, 
                               text="📋 Scheduled Tasks",
                               font=self.fonts['header'],
                               fg=self.colors['text_primary'],
                               bg=self.colors['bg_secondary'])
        header_label.pack(side=tk.LEFT)
        
        # Delete button
        self.delete_button = tk.Button(header_frame, 
                                      text="🗑️ Delete",
                                      bg=self.colors['warning'],
                                      fg=self.colors['text_primary'],
                                      font=('Segoe UI', 10, 'bold'),
                                      relief='raised',
                                      bd=2,
                                      activebackground='#C0392B',
                                      activeforeground=self.colors['text_primary'],
                                      command=self.delete_task)
        self.delete_button.pack(side=tk.RIGHT, padx=5, ipady=2)
        
        # Create Treeview for tasks
        tree_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Description", "Type", "Date", "Time", "Status")
        self.tasks_tree = ttk.Treeview(tree_frame, 
                                      columns=columns, 
                                      show="headings", 
                                      style='Modern.Treeview',
                                      height=15)
        
        # Define headings with emojis
        self.tasks_tree.heading("Description", text="📝 Description")
        self.tasks_tree.heading("Type", text="🏷️ Type")
        self.tasks_tree.heading("Date", text="📅 Date")
        self.tasks_tree.heading("Time", text="⏰ Time")
        self.tasks_tree.heading("Status", text="✅ Status")
        
        # Configure column widths
        self.tasks_tree.column("Description", width=200)
        self.tasks_tree.column("Type", width=100)
        self.tasks_tree.column("Date", width=100)
        self.tasks_tree.column("Time", width=80)
        self.tasks_tree.column("Status", width=100)
        
        self.tasks_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tasks_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure row colors
        self.tasks_tree.tag_configure('scheduled', background='#E8F5E8')
        self.tasks_tree.tag_configure('completed', background='#FFF3E0')
    
    def update_status(self, message, color=None):
        """Update the status indicator"""
        if color is None:
            color = self.colors['success']
        self.status_label.config(text=f"● {message}", fg=color)
        self.root.after(3000, lambda: self.status_label.config(text="● Ready", fg=self.colors['success']))
    
    def update_stats(self):
        """Update the task statistics"""
        total_tasks = len(self.tasks)
        scheduled_tasks = len([t for t in self.tasks if t['status'] == 'Scheduled'])
        completed_tasks = len([t for t in self.tasks if t['status'] == 'Completed'])
        
        stats_text = f"📊 Total: {total_tasks} | 📅 Scheduled: {scheduled_tasks} | ✅ Completed: {completed_tasks}"
        self.stats_label.config(text=stats_text)
    
    def get_weather_info(self, location):
        """Get weather information for the specified location"""
        # First try real API
        if self.weather_api_key and self.weather_api_key != "5a081e357069900f70cdb55c8a39af86":
            try:
                params = {
                    'q': location,
                    'appid': self.weather_api_key,
                    'units': 'metric'
                }
                response = requests.get(self.weather_base_url, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()
                
                temp = data['main']['temp']
                description = data['weather'][0]['description'].title()
                return f"{temp}°C, {description}"
            except Exception as e:
                print(f"Real weather API failed: {e}")
        
        # Fallback to mock weather data for demo/portfolio
        return self.get_mock_weather(location)
    
    def get_mock_weather(self, location):
        """Get mock weather data for demo purposes"""
        mock_weather = {
            'New York': {'temp': 18, 'desc': 'Partly Cloudy'},
            'London': {'temp': 12, 'desc': 'Light Rain'},
            'Paris': {'temp': 15, 'desc': 'Clear Sky'},
            'Tokyo': {'temp': 22, 'desc': 'Sunny'},
            'Sydney': {'temp': 20, 'desc': 'Overcast'},
            'Berlin': {'temp': 14, 'desc': 'Cloudy'},
            'Moscow': {'temp': 8, 'desc': 'Snow'},
            'Dubai': {'temp': 35, 'desc': 'Hot and Sunny'},
            'Singapore': {'temp': 28, 'desc': 'Thunderstorm'},
            'Los Angeles': {'temp': 24, 'desc': 'Clear'},
            'Chicago': {'temp': 16, 'desc': 'Windy'},
            'Toronto': {'temp': 11, 'desc': 'Foggy'},
            'Mumbai': {'temp': 30, 'desc': 'Humid'},
            'Beijing': {'temp': 19, 'desc': 'Hazy'},
            'Rio': {'temp': 26, 'desc': 'Warm'}
        }
        
        # Find matching city (case-insensitive)
        for city, weather in mock_weather.items():
            if city.lower() in location.lower() or location.lower() in city.lower():
                return f"{weather['temp']}°C, {weather['desc']}"
        
        # Default weather if no match
        return f"{20}°C, Pleasant"
    
    def add_task(self):
        """Add a new task"""
        description = self.description_entry.get().strip()
        task_type = self.task_type_var.get()
        date_str = self.date_var.get().strip()
        time_str = self.time_var.get().strip()
        location = self.location_entry.get().strip()
        
        if not description:
            self.update_status("Please enter a task description", self.colors['warning'])
            messagebox.showerror("Error", "Please enter a task description")
            return
        
        try:
            # Parse date and time
            datetime_str = f"{date_str} {time_str}"
            task_datetime = parser.parse(datetime_str)
            
            # Check if the time is in the past
            if task_datetime <= datetime.now():
                self.update_status("Cannot schedule tasks in the past", self.colors['warning'])
                messagebox.showerror("Error", "Cannot schedule tasks in the past")
                return
            
        except ValueError:
            self.update_status("Invalid date/time format", self.colors['warning'])
            messagebox.showerror("Error", "Invalid date/time format. Use YYYY-MM-DD and HH:MM")
            return
        
        # Get weather info for outdoor activities
        weather_info = None
        if task_type == "Outdoor Activity":
            self.update_status("Fetching weather data...", self.colors['highlight'])
            weather_info = self.get_weather_info(location)
            if weather_info:
                description += f" (Weather: {weather_info})"
                self.weather_info_label.config(text=f"🌤️ {weather_info}")
            else:
                self.weather_info_label.config(text="⚠️ Weather data unavailable")
        
        # Create task dictionary
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'type': task_type,
            'datetime': task_datetime.isoformat(),
            'location': location,
            'status': 'Scheduled',
            'weather_info': weather_info
        }
        
        # Add to tasks list
        self.tasks.append(task)
        
        # Schedule the task
        self.schedule_task(task)
        
        # Save tasks
        self.save_tasks()
        
        # Update GUI
        self.update_tasks_display()
        self.update_stats()
        
        # Clear input fields
        self.description_entry.delete(0, tk.END)
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.time_var.set(datetime.now().strftime("%H:%M"))
        
        # Success feedback
        self.update_status("Task added successfully!", self.colors['success'])
        
        # Show success message with task details
        task_time = task_datetime.strftime("%Y-%m-%d %H:%M")
        messagebox.showinfo("Success", f"Task scheduled for {task_time}")
    
    def schedule_task(self, task):
        """Schedule a task for notification"""
        task_datetime = parser.parse(task['datetime'])
        
        # Calculate the time difference
        now = datetime.now()
        time_diff = task_datetime - now
        
        if time_diff.total_seconds() > 0:
            # Schedule the notification
            schedule.every().day.at(task_datetime.strftime("%H:%M")).do(
                self.show_notification, 
                task['description'],
                task['id']
            ).tag(str(task['id']))
    
    def show_notification(self, description, task_id):
        """Show desktop notification for a task"""
        try:
            notification.notify(
                title=config.NOTIFICATION_TITLE,
                message=description,
                timeout=config.NOTIFICATION_TIMEOUT
            )
            
            # Update task status
            for task in self.tasks:
                if task['id'] == task_id:
                    task['status'] = 'Completed'
                    break
            
            # Save updated tasks
            self.save_tasks()
            
            # Update GUI
            self.update_tasks_display()
            
        except Exception as e:
            print(f"Notification error: {e}")
    
    def delete_task(self):
        """Delete selected task"""
        selected = self.tasks_tree.selection()
        if not selected:
            self.update_status("Please select a task to delete", self.colors['warning'])
            messagebox.showwarning("Warning", "Please select a task to delete")
            return
        
        # Get the task ID from the treeview
        item = self.tasks_tree.item(selected[0])
        task_description = item['values'][0]
        
        # Find and remove the task
        task_to_delete = None
        for task in self.tasks:
            if task['description'] == task_description:
                task_to_delete = task
                break
        
        if task_to_delete:
            # Remove from tasks list
            self.tasks.remove(task_to_delete)
            
            # Cancel the scheduled job
            schedule.clear(str(task_to_delete['id']))
            
            # Save and update
            self.save_tasks()
            self.update_tasks_display()
            self.update_stats()
            
            self.update_status("Task deleted successfully!", self.colors['success'])
            messagebox.showinfo("Success", "Task deleted successfully!")
        else:
            self.update_status("Task not found", self.colors['warning'])
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r') as f:
                    self.tasks = json.load(f)
                
                # Reschedule all tasks
                for task in self.tasks:
                    if task['status'] == 'Scheduled':
                        self.schedule_task(task)
                
                self.update_tasks_display()
                self.update_stats()
                self.update_status(f"Loaded {len(self.tasks)} tasks")
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
    
    def update_tasks_display(self):
        """Update the tasks display in the treeview"""
        # Clear existing items
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        # Add tasks to treeview
        for task in self.tasks:
            task_datetime = parser.parse(task['datetime'])
            date_str = task_datetime.strftime("%Y-%m-%d")
            time_str = task_datetime.strftime("%H:%M")
            
            # Determine tag based on status
            tag = task['status'].lower()
            
            # Add type emoji
            type_emoji = {
                'General': '📝',
                'Meeting': '🤝',
                'Outdoor Activity': '🏃'
            }.get(task['type'], '📝')
            
            # Status emoji
            status_emoji = '📅' if task['status'] == 'Scheduled' else '✅'
            
            self.tasks_tree.insert("", tk.END, values=(
                task['description'],
                f"{type_emoji} {task['type']}",
                date_str,
                time_str,
                f"{status_emoji} {task['status']}"
            ), tags=(tag,))
    
    def run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def update_gui(self):
        """Periodically update the GUI"""
        self.update_tasks_display()
        self.update_stats()
        self.root.after(config.UPDATE_INTERVAL, self.update_gui)  # Update every minute

def main():
    root = tk.Tk()
    app = SmartTaskScheduler(root)
    root.mainloop()

if __name__ == "__main__":
    main()
