import os
import requests
from PIL import Image, ImageTk

ICON_FOLDER = "assets/icons/"

def download_icon(icon_code):
    os.makedirs(ICON_FOLDER, exist_ok=True)
    icon_path = os.path.join(ICON_FOLDER, f"{icon_code}.png")
    if not os.path.exists(icon_path):
        url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        response = requests.get(url)
        with open(icon_path, "wb") as f:
            f.write(response.content)
    return icon_path

def load_icon(icon_code):
    path = download_icon(icon_code)
    img = Image.open(path).resize((50, 50))
    return ImageTk.PhotoImage(img)