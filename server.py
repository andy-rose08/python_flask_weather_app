from math import ceil
from flask import Flask, render_template, request
from weather import get_current_weather, get_location, get_forecast as get_weather_forecast
from flask_frozen import Freezer
from waitress import serve
import sys
import os
import traceback

app = Flask(__name__)
freezer = Freezer(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", API_KEY=os.getenv("API_KEY"))


@app.route("/weather", methods=["GET", "POST"])
def get_weather():
    try:
        if request.method == "POST":
            city = request.form.get("city")
        else:
            city = request.args.get("city")  # Get city from URL parameters

        if city is None:  # If city is still None, proceed with the default behavior
            city_data = get_location(request.remote_addr)
            if isinstance(city_data, dict):
                city = city_data.get("city")
            else:
                city = city_data

        if city is None:
            city = "San Jose"
        elif not isinstance(city, str) or not bool(city.strip()):
            return "Invalid city name", 400

        weather_data = get_current_weather(city)
        if weather_data is None or weather_data.get("cod") != 200:
            return render_template("city404.html", API_KEY=os.getenv("API_KEY"))

        icon_code = weather_data["weather"][0]["icon"]
        icon_url = "https://openweathermap.org/img/w/" + icon_code + ".png"

        return render_template(
            "weather.html",
            title=weather_data["name"],
            status=weather_data["weather"][0]["description"].capitalize(),
            temp=f"{weather_data['main']['temp']:.1f}",
            feels_like=f"{weather_data['main']['feels_like']:.1f}",
            icon_code=icon_url,
            API_KEY=os.getenv("API_KEY"),
            city=city,  # Pass the city to the template
        )
    except Exception as e:
        traceback.print_exc()
        return "An error occurred: " + str(e), 500


@app.route("/forecast")
def get_forecast():
    city = request.args.get("city")
    if city is None or not bool(city.strip()):
        city = "San Jose"
    forecast_data = get_weather_forecast(city)
    if forecast_data is None or forecast_data.get("cod") != "200":
        return render_template("city404.html", API_KEY=os.getenv("API_KEY"))

    # Divide the forecast into pages of 5 items each
    forecast = forecast_data["list"]
    forecasts_per_page = 5
    pages = [forecast[i : i + forecasts_per_page] for i in range(0, len(forecast), forecasts_per_page)]
    total_pages = ceil(len(forecast) / forecasts_per_page)

    page = request.args.get("page", 1, type=int)
    if page > total_pages:
        page = total_pages
    elif page < 1:
        page = 1

    return render_template(
        "forecast.html",
        title=forecast_data["city"]["name"],
        forecast=pages[page - 1],
        total_pages=total_pages,
        current_page=page,
        current_city=city,
    )


@app.route("/city404")
def all_routes():
    return render_template("city404.html", API_KEY=os.getenv("API_KEY"))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()  # Build the static files
    else:
        serve(app, host="0.0.0.0", port=8000)  # Run the application
