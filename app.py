from tkinter import *
from tkinter import messagebox
from api.weather_api import get_weather_data
from features.statistics import WeatherStatistics
from features.alerts import WeatherAlert
from features.theme import ThemeManager

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("400x400")
        
        self.theme_manager = ThemeManager(root)
        self.stats = WeatherStatistics()
        self.alert_system = WeatherAlert(threshold=85)  # Fahrenheit threshold for alerts
        
        # Widgets
        self.city_entry = Entry(root)
        self.city_entry.pack(pady=10)
        
        self.get_weather_btn = Button(root, text="Get Weather", command=self.fetch_weather)
        self.get_weather_btn.pack(pady=5)
        
        self.weather_label = Label(root, text="", font=("Helvetica", 12))
        self.weather_label.pack(pady=10)

        self.theme_btn = Button(root, text="Switch Theme", command=self.theme_manager.toggle_theme)
        self.theme_btn.pack(pady=5)

        self.stats_btn = Button(root, text="Show Stats", command=self.show_stats)
        self.stats_btn.pack(pady=5)

    def fetch_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        
        data = get_weather_data(city)
        if not data:
            messagebox.showerror("API Error", "Failed to retrieve data.")
            return
        
        temp = data['temp']
        desc = data['description']
        weather = f"{city}: {temp}°F, {desc}"
        self.weather_label.config(text=weather)

        # Save data to stats
        self.stats.save_weather(city, temp, desc)

        # Check for alerts
        alert_message = self.alert_system.check_alert(temp)
        if alert_message:
            messagebox.showinfo("Weather Alert", alert_message)

    def show_stats(self):
        stats_text = self.stats.get_statistics()
        messagebox.showinfo("Weather Statistics", stats_text)

if __name__ == "__main__":
    root = Tk()
    app = WeatherApp(root)
    root.mainloop()