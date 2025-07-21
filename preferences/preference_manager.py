PREFERENCE_SCHEMA = {
    "general": {
        "temperature_unit": {
            "type": "choice",
            "options": ["celsius", "fahrenheit", "kelvin"],
            "default": "fahrenheit",
            "label": "Temperature Unit",
            "description": "Display temperature in preferred unit"
        },
        "wind_speed_unit": {
            "type": "choice",
            "options": ["mph", "kph", "m/s", "knots"],
            "default": "mph",
            "label": "Wind Speed Unit",
            "description": "Display wind speed in preferred unit"
        },
        "pressure_unit": {
            "type": "choice",
            "options": ["mb", "inHg", "hPa"],
            "default": "inHg",
            "label": "Pressure Unit",
            "description": "Display pressure in preferred unit"
        },
        "time_format": {
            "type": "choice",
            "options": ["12h", "24h"],
            "default": "12h",
            "label": "Time Format",
            "description": "12-hour or 24-hour time display"
        }
    },
    "location": {
        "default_location": {
            "type": "string",
            "default": "",
            "label": "Default Location",
            "description": "City or ZIP code to load on startup"
        },
        "save_recent_locations": {
            "type": "boolean",
            "default": True,
            "label": "Save Recent Locations",
            "description": "Remember recently searched locations"
        },
        "max_recent_locations": {
            "type": "integer",
            "default": 10,
            "min": 1,
            "max": 50,
            "label": "Recent Locations Count",
            "description": "Number of recent locations to remember"
        }
    },
    "display": {
        "theme": {
            "type": "choice",
            "options": ["light", "dark", "auto"],
            "default": "light",
            "label": "Application Theme",
            "description": "Visual theme for the application"
        },
        "show_feels_like": {
            "type": "boolean",
            "default": True,
            "label": "Show 'Feels Like' Temperature",
            "description": "Display feels-like temperature"
        },
        "show_humidity": {
            "type": "boolean",
            "default": True,
            "label": "Show Humidity",
            "description": "Display humidity percentage"
        },
        "show_uv_index": {
            "type": "boolean",
            "default": True,
            "label": "Show UV Index",
            "description": "Display UV index when available"
        },
        "chart_style": {
            "type": "choice",
            "options": ["line", "bar", "area"],
            "default": "line",
            "label": "Default Chart Style",
            "description": "Preferred visualization style"
        }
    },
    "data": {
        "update_interval": {
            "type": "integer",
            "default": 30,
            "min": 5,
            "max": 120,
            "label": "Update Interval (minutes)",
            "description": "How often to refresh weather data"
        },
        "cache_duration": {
            "type": "integer",
            "default": 7,
            "min": 1,
            "max": 30,
            "label": "Cache Duration (days)",
            "description": "How long to keep historical data"
        },
        "enable_notifications": {
            "type": "boolean",
            "default": False,
            "label": "Enable Weather Alerts",
            "description": "Show notifications for severe weather"
        }
    },
    "advanced": {
        "api_timeout": {
            "type": "integer",
            "default": 10,
            "min": 5,
            "max": 30,
            "label": "API Timeout (seconds)",
            "description": "Maximum time to wait for API responses"
        },
        "debug_mode": {
            "type": "boolean",
            "default": False,
            "label": "Debug Mode",
            "description": "Show detailed error messages"
        },
        "log_api_calls": {
            "type": "boolean",
            "default": False,
            "label": "Log API Calls",
            "description": "Save API request/response logs"
        }
    }
}




from typing import Any, Dict, List, Callable
import json
import os
from datetime import datetime

class PreferenceManager:
    def __init__(self, storage_path="preferences.json", schema=PREFERENCE_SCHEMA):
        self.storage_path = storage_path
        self.schema = schema
        self.preferences = self._load_preferences()
        self._change_listeners = []
        self._ensure_defaults()
    
    def _load_preferences(self) -> Dict:
        """Load preferences from storage or return defaults."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print(f"Error loading preferences, using defaults")
        return {}
    
    def _ensure_defaults(self):
        """Ensure all preferences have values, using defaults if needed."""
        for category, prefs in self.schema.items():
            if category not in self.preferences:
                self.preferences[category] = {}
            for key, spec in prefs.items():
                if key not in self.preferences[category]:
                    self.preferences[category][key] = spec['default']
    
    def get(self, category: str, key: str, default=None) -> Any:
        """Get a preference value."""
        try:
            return self.preferences[category][key]
        except KeyError:
            return default
    
    def set(self, category: str, key: str, value: Any) -> bool:
        """Set a preference value with validation."""
        # Validate the preference exists in schema
        if category not in self.schema or key not in self.schema[category]:
            raise ValueError(f"Unknown preference: {category}.{key}")
        
        spec = self.schema[category][key]
        
        # Validate the value
        if not self._validate_value(value, spec):
            raise ValueError(f"Invalid value for {category}.{key}: {value}")
        
        # Store old value for change notification
        old_value = self.preferences.get(category, {}).get(key)
        
        # Set the new value
        if category not in self.preferences:
            self.preferences[category] = {}
        self.preferences[category][key] = value
        
        # Save to storage
        self._save_preferences()
        
        # Notify listeners
        if old_value != value:
            self._notify_change(category, key, old_value, value)
        
        return True
    
    def _validate_value(self, value: Any, spec: Dict) -> bool:
        """Validate a value against its specification."""
        pref_type = spec['type']
        
        if pref_type == 'boolean':
            return isinstance(value, bool)
        elif pref_type == 'integer':
            if not isinstance(value, int):
                return False
            if 'min' in spec and value < spec['min']:
                return False
            if 'max' in spec and value > spec['max']:
                return False
            return True
        elif pref_type == 'string':
            return isinstance(value, str)
        elif pref_type == 'choice':
            return value in spec['options']
        
        return False
    
    def _save_preferences(self):
        """Save preferences to storage."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.preferences, f, indent=2)
        except IOError as e:
            print(f"Error saving preferences: {e}")
    
    def add_change_listener(self, callback: Callable):
        """Add a listener for preference changes."""
        self._change_listeners.append(callback)
    
    def remove_change_listener(self, callback: Callable):
        """Remove a change listener."""
        if callback in self._change_listeners:
            self._change_listeners.remove(callback)
    
    def _notify_change(self, category: str, key: str, old_value: Any, new_value: Any):
        """Notify all listeners of a preference change."""
        for listener in self._change_listeners:
            try:
                listener(category, key, old_value, new_value)
            except Exception as e:
                print(f"Error in preference change listener: {e}")
    
    def reset_to_defaults(self, category: str = None):
        """Reset preferences to defaults."""
        if category:
            # Reset specific category
            if category in self.schema:
                for key, spec in self.schema[category].items():
                    old_value = self.preferences.get(category, {}).get(key)
                    self.preferences[category][key] = spec['default']
                    if old_value != spec['default']:
                        self._notify_change(category, key, old_value, spec['default'])
        else:
            # Reset all preferences
            old_preferences = self.preferences.copy()
            self.preferences = {}
            self._ensure_defaults()
            
            # Notify changes
            for category in self.schema:
                for key in self.schema[category]:
                    old_value = old_preferences.get(category, {}).get(key)
                    new_value = self.preferences[category][key]
                    if old_value != new_value:
                        self._notify_change(category, key, old_value, new_value)
        
        self._save_preferences()
    
    def export_preferences(self, filepath: str):
        """Export preferences to a file."""
        with open(filepath, 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def import_preferences(self, filepath: str):
        """Import preferences from a file."""
        try:
            with open(filepath, 'r') as f:
                imported = json.load(f)
            
            # Validate imported preferences
            for category, prefs in imported.items():
                if category in self.schema:
                    for key, value in prefs.items():
                        if key in self.schema[category]:
                            self.set(category, key, value)
            
            return True
        except Exception as e:
            print(f"Error importing preferences: {e}")
            return False
