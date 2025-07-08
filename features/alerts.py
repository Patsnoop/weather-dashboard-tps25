class WeatherAlert:
    def __init__(self, threshold):
        self.threshold = threshold

    def check_alert(self, temp):
        if temp > self.threshold:
            return f"Alert: Temperature exceeds {self.threshold}°F!"
        return None