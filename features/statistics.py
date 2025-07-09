import csv
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("data/weather_history.csv")

class WeatherStatistics:
    def __init__(self):
        self.ensure_data_file()

    def ensure_data_file(self):
        if not DATA_FILE.exists():
            DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(DATA_FILE, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['date','city', 'temp', 'feels_like', 'humidity', 'wind_speed', 'description'])

    def save_weather(self, data):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(DATA_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                now,
                data['city'],
                data['temp'],
                data['feels_like'],
                data['humidity'],
                data['wind_speed'],
                data['description']
            ])

    def get_statistics(self):
        temps = []
        humidity = []
        wind = []
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            if 'temp' not in reader.fieldnames:
                return "Error: CSV headers are incorrect."

            for row in reader:
                try:
                    temps.append(float(row['temp']))
                    humidity.append(int(row['humidity']))
                    wind.append(float(row['wind_speed']))
                except (ValueError, KeyError):
                    # Skip bad rows
                    continue

        if not temps:
            return "No data available."

        return (
            f"Temp: Min {min(temps):.1f}°F, Max {max(temps):.1f}°F\n"
            f"Humidity: Avg {sum(humidity)/len(humidity):.1f}%\n"
            f"Wind Speed: Avg {sum(wind)/len(wind):.1f} mph"
        )