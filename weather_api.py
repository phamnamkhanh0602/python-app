import requests
api_key = "5634849698f284eba828945eec5edfee"


city = "Ha Noi"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
print(url)
x = requests.get(url)
print(x.json())