import os
import requests
from datetime import datetime
from requests_oauthlib import OAuth1

# ===== 環境変数を最初に取得 =====
OPENWEATHER_KEY = os.environ["OPENWEATHER_KEY"]

X_API_KEY = os.environ["X_API_KEY"]
X_API_SECRET = os.environ["X_API_SECRET"]
X_ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
X_ACCESS_TOKEN_SECRET = os.environ["X_ACCESS_TOKEN_SECRET"]

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


def post_to_x(text: str):
    url = "https://api.x.com/2/tweets"

    oauth = OAuth1(
        X_API_KEY,
        X_API_SECRET,
        X_ACCESS_TOKEN,
        X_ACCESS_TOKEN_SECRET
    )

    response = requests.post(
        url,
        json={"text": text},
        auth=oauth,
        timeout=20
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code not in (200, 201):
        raise Exception(f"X API error: {response.status_code} {response.text}")


def main():
    temp, desc = get_weather()
    today = datetime.now().strftime("%Y年%m月%d日")

    tweet_text = f"""{today} 札幌の天気 ☀️
{desc}
気温 {temp:.1f}℃"""

    print("Tweeting...")
    print(tweet_text)

    post_to_x(tweet_text)


if __name__ == "__main__":
    main()