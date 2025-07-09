from tkinter import *
from tkinter import messagebox
from api.weather_api import get_weather_data
from features.statistics import WeatherStatistics
from features.alerts import WeatherAlert
from features.theme import ThemeManager
from features.graph import TemperatureGraph
from utils.image_utils import load_icon
import tkinter as tk


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("1000x1300")

        theme_manager = ThemeManager(root)
        self.stats = WeatherStatistics()
        self.alert_system = WeatherAlert(threshold=85)

        # Input Frame
        top_frame = Frame(root)
        top_frame.pack(pady=10)

        self.city_entry = Entry(top_frame, width=25)
        self.city_entry.pack(side=LEFT, padx=5)

        self.get_weather_btn = Button(top_frame, text="Get Weather", command=self.fetch_weather)
        self.get_weather_btn.pack(side=LEFT, padx=5)

        # Weather Info Frame
        self.weather_frame = Frame(root)
        self.weather_frame.pack(pady=10)

        self.icon_label = Label(self.weather_frame)
        self.icon_label.pack()

        self.weather_label = Label(self.weather_frame, text="", font=("Helvetica", 12))
        self.weather_label.pack()

        # Graph Frame
        self.graph_frame = Frame(root)
        self.graph_frame.pack(pady=20)

        self.graph = TemperatureGraph(self.graph_frame)

        # Control Buttons
        control_frame = Frame(root)
        control_frame.pack(pady=10)

        label = tk.Label(root, text="Select a theme:")
        label.pack(pady=10)

        # Theme dropdown
        theme_var = tk.StringVar(value="Light")
        theme_menu = tk.OptionMenu(root, theme_var, *theme_manager.themes.keys(), command=theme_manager.apply_theme)
        theme_menu.pack(pady=10)

        # Apply default theme
        theme_manager.apply_theme("Light")

        self.stats_btn = Button(control_frame, text="Show Stats", command=self.show_stats)
        self.stats_btn.grid(row=0, column=1, padx=5)

        self.refresh_btn = Button(control_frame, text="Refresh Graph", command=self.graph.plot_graph)
        self.refresh_btn.grid(row=0, column=2, padx=5)

        # Load initial empty graph
        self.graph.plot_graph()

        self.last_data = None

    def fetch_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        data = get_weather_data(city)
        if not data:
            messagebox.showerror("API Error", "Failed to retrieve data.")
            return

        self.last_data = data
        self.stats.save_weather(data)
        self.display_weather(data)

        alert_message = self.alert_system.check_alert(data['temp'])
        if alert_message:
            messagebox.showinfo("Weather Alert", alert_message)

        self.graph.plot_graph()

    def display_weather(self, data):
        icon = load_icon(data['icon'])
        self.icon_label.configure(image=icon)
        self.icon_label.image = icon

        info = (
            f"{data['city']}\n"
            f"Temp: {data['temp']}\u00b0F (Feels like {data['feels_like']}\u00b0F)\n"
            f"Humidity: {data['humidity']}%\n"
            f"Wind Speed: {data['wind_speed']} mph\n"
            f"{data['description'].capitalize()}"
        )
        self.weather_label.config(text=info)

    def show_stats(self):
        stats_text = self.stats.get_statistics()
        messagebox.showinfo("Weather Statistics", stats_text)


if __name__ == "__main__":
    root = Tk()
    app = WeatherApp(root)
    root.mainloop()




    # label = tk.Label(root, text="Select a theme:")
    #     label.pack(pady=10)

    #     # Theme dropdown
    #     theme_var = tk.StringVar(value="Light")
    #     theme_menu = tk.OptionMenu(root, theme_var, *theme_manager.themes.keys(), command=theme_manager.apply_theme)
    #     theme_menu.pack(pady=10)

    #     # Apply default theme
    #     theme_manager.apply_theme("Light")