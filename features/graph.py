import csv
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_FILE = Path("data/weather_history.csv")

class TemperatureGraph:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

    def plot_graph(self):
        dates = []
        temps = []

        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    dates.append(row['date'])
                    temps.append(float(row['temp']))
                except (ValueError, KeyError):
                    continue  # skip malformed rows

        if not temps:
            return  # No data to plot

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot(dates, temps, marker='o', linestyle='-', color='blue')
        ax.set_title("Temperature Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Temp (°F)")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)

        # Clear old graph
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Embed the figure into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()