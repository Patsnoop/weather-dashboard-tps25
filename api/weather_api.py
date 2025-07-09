import requests

API_KEY = "1986865e3e61ccff86286f9f80c06713"

def get_weather_data(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        return {
            "city": city,
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"]
        }
    except Exception as e:
        print(f"API Error: {e}")
        return None