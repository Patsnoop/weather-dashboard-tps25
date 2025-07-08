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
            for i, row in enumerate(reader):
                dates.append(f"Day {i + 1}")
                temps.append(float(row['temp']))

        if not temps:
            return

        # Create a figure
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot(dates, temps, marker='o', linestyle='-', color='blue')
        ax.set_title("Temperature Over Time")
        ax.set_xlabel("Entry")
        ax.set_ylabel("Temp (°F)")
        ax.grid(True)

        # Embed the figure into the Tkinter frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()