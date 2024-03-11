from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()


def get_current_weather(city="San Jose"):
    request_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv("API_KEY")}&units=metric'

    weather_data = requests.get(request_url).json()

    return weather_data


def get_forecast(city="San Jose"):
    request_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={os.getenv("API_KEY")}&units=metric'

    forecast_data = requests.get(request_url).json()

    return forecast_data


def get_location(ip_address):
    request_url = f"https://ipinfo.io/{ip_address}/json"

    location_data = requests.get(request_url).json()

    return location_data.get("city", "San Jose")


def get_alerts(city="San Jose"):
    request_url = f'https://api.openweathermap.org/data/2.5/onecall?q={city}&appid={os.getenv("API_KEY")}&units=metric'
    alert_data = requests.get(request_url).json()
    return alert_data



if __name__ == "__main__":
    pprint("\n*** Get Current Weather Conditions ***\n")

    city = input("\n Enter a city name: ")

    # CHECK EMPTY STRINGS OR EMPTY SPACES

    if not bool(city.strip()):
        city = "San Jose"

    weather_data = get_current_weather(city)
    pprint(weather_data)
