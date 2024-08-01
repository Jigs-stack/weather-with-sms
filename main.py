from dotenv import load_dotenv
import os
from datetime import datetime
import requests, urllib.parse

load_dotenv()


weather_params = {
    "lat": os.getenv("LAT"),
    "lon": os.getenv("LONG"),
    "API key": os.getenv("WEATHER_API_KEY"),
}


weather_api_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={weather_params['lat']}&lon={weather_params['lon']}&appid={weather_params['API key']}"


today = datetime.now().date()


def check_rain(forecast_data):
    for forecast in forecast_data["list"]:
        forecast_today = datetime.fromtimestamp(forecast["dt"])
        if forecast_today.date() == today:
            if (
                "rain" in forecast
                and "3h" in forecast["rain"]
                and forecast["rain"]["3h"] > 1.5
            ):
                return True
            else:
                print("It wont rain today")


message = "It might rain later today! Please don't forget to bring a coat or umbrella"
# numbers = put your phone numbers in here


def send_message(message, number):
    params = (
        ("apikey", os.getenv("SMS_API_KEY")),
        ("message", message),
        ("number", ",".join(number)),
    )
    try:
        path = "https://semaphore.co/api/v4/messages?" + urllib.parse.urlencode(params)
        requests.post(path)
    except KeyError as err:
        print("Check your API Key", err)
    except requests.exceptions.HTTPError as err:
        print(err)
    except err:
        print("something went wrong", err)
    else:
        print(path)  # get the output link
        print("SMS sent!")


try:
    response = requests.get(weather_api_url)
    forecast_data = response.json()
    check_rain(forecast_data)
except KeyError as err:
    print(f"Check your API Key {err}")
except requests.exceptions.HTTPError as err:
    print(err.response.status_code)
except requests.exceptions.JSONDecodeError as err:
    print(err.response.json)
else:
    if check_rain:
        send_message(message=message, number=numbers)
