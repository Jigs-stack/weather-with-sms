from dotenv import load_dotenv
import os
from datetime import datetime
from message import SendMessage
import requests

load_dotenv()


weather_params = {
    "lat": os.getenv("LAT"),
    "lon": os.getenv("LONG"),
    "API key": os.getenv("WEATHER_API_KEY"),
}


weather_api_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={weather_params['lat']}&lon={weather_params['lon']}&appid={weather_params['API key']}"

rain_message1 = "There's an 80% possibility that it might rain today, please dont forget to bring an umbrella or a coat."
rain_message2 = "There's a 45% possibility that it might rain today, please dont forget to bring an umbrella or a coat."


today = datetime.now().date()


def check_rain(forecast_data):
    for forecast in forecast_data["list"]:
        forecast_today = datetime.fromtimestamp(forecast["dt"])
        if forecast_today.date() == today:
            if (
                "rain" in forecast
                and "3h" in forecast["rain"]
                and forecast["rain"]["3h"] > 3.5 < 7.5
            ):
                SendMessage(rain_message1, numbers)
            if (
                "rain" in forecast
                and "3h" in forecast["rain"]
                and forecast["rain"]["3h"] >= 2.2 < 3.5
            ):
                SendMessage(rain_message2, numbers)
            else:
                print(forecast_today.now().date().hour % 3 == 0)


try:
    response = requests.get(weather_api_url)
    forecast_data = response.json()
except KeyError as err:
    print(f"Check your API Key {err}")
except requests.exceptions.HTTPError as err:
    print(err.response.status_code)
except requests.exceptions.JSONDecodeError as err:
    print(err.response.json)
else:
    check_rain(forecast_data)
