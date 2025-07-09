import requests
from PIL import Image, ImageTk
import os

MAP_FOLDER = "assets/maps/"

def download_map(lat, lon, zoom=10):
    os.makedirs(MAP_FOLDER, exist_ok=True)
    file_path = os.path.join(MAP_FOLDER, f"{lat}_{lon}.png")

    if not os.path.exists(file_path):
        url = (
            f"https://staticmap.openstreetmap.de/staticmap.php?"
            f"center={lat},{lon}&zoom={zoom}&size=400x300&markers={lat},{lon},red-pushpin"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error if request fails
        with open(file_path, 'wb') as f:
            f.write(response.content)

    return file_path

def load_map_image(lat, lon):
    map_path = download_map(lat, lon)
    img = Image.open(map_path)
    return ImageTk.PhotoImage(img)