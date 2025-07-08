import requests

API_KEY = "1986865e3e61ccff86286f9f80c06713"

def get_weather_data(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return None
        return {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    except Exception as e:
        print(f"API Error: {e}")
        return None