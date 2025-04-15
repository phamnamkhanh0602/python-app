import requests
api_key = "5634849698f284eba828945eec5edfee"

def get_weather_by_name(name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={api_key}&units=metric"
    x = requests.get(url)
    return x.json()

# 5 day weather forecast
def get_weather_forecast_by_name(name):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={name}&appid={api_key}&units=metric"
    x = requests.get(url)
    return x.json()

