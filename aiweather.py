import os
import requests
from datetime import datetime

OPENWEATHER_KEY = os.environ["OPENWEATHER_KEY"]
CITY = "Sapporo,jp"

def get_weather():
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={OPENWEATHER_KEY}&units=metric&lang=ja"
    )
    r = requests.get(url, timeout=20)
    data = r.json()

    print("FULL API RESPONSE:")
    print(data)

    if "main" not in data or "weather" not in data:
        raise Exception(f"API did not return weather data: {data}")

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return temp, desc

def main():
    temp, desc = get_weather()
    today = datetime.now().strftime("%Y年%m月%d日")
    print(f"{today} 札幌の天気 ☀️")
    print(desc)
    print(f"気温 {temp:.1f}℃")

if __name__ == "__main__":
    main()
