import os
import requests

# Create a folder to save icons
ICON_FOLDER = "weather_icons"
os.makedirs(ICON_FOLDER, exist_ok=True)

# List of all OpenWeather icon codes (day & night)
icon_codes = [
    "01d", "01n", "02d", "02n", "03d", "03n", "04d", "04n",
    "09d", "09n", "10d", "10n", "11d", "11n", "13d", "13n",
    "50d", "50n"
]

# Base URL for OpenWeather icons
BASE_URL = "https://openweathermap.org/img/wn/"

# Function to download icons
def download_icons():
    for code in icon_codes:
        icon_url = f"{BASE_URL}{code}@2x.png"  # Using 2x size
        icon_path = os.path.join(ICON_FOLDER, f"{code}.png")

        response = requests.get(icon_url)
        if response.status_code == 200:
            with open(icon_path, "wb") as file:
                file.write(response.content)
            print(f"✅ Downloaded: {icon_path}")
        else:
            print(f"❌ Failed to download: {icon_url}")

# Run the script
download_icons()
print("🎉 All icons downloaded successfully!")
