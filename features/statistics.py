import csv
from pathlib import Path

DATA_FILE = Path("data/weather_history.csv")

class WeatherStatistics:
    def __init__(self):
        self.ensure_data_file()

    def ensure_data_file(self):
        if not DATA_FILE.exists():
            DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(DATA_FILE, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['city', 'temp', 'description'])

    def save_weather(self, city, temp, description):
        with open(DATA_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([city, temp, description])

    def get_statistics(self):
        temps = []
        weather_types = {}
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                temps.append(float(row['temp']))
                desc = row['description']
                weather_types[desc] = weather_types.get(desc, 0) + 1

        if not temps:
            return "No data available."

        return (
            f"Min Temp: {min(temps):.1f}°F\n"
            f"Max Temp: {max(temps):.1f}°F\n"
            f"Weather Types: {weather_types}"
        )