from flask import Flask, render_template, request


from weather import get_current_weather, get_location, get_forecast as get_weather_forecast

from waitress import serve


app = Flask(__name__)



@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/weather")
def get_weather():
    city = request.args.get("city")

    if not bool(city.strip()):
        city = get_location(request.remote_addr)

    weather_data = get_current_weather(city)

    # City not found
    if not weather_data["cod"] == 200:
        return render_template("city404.html")

    # Get the weather icon code
    icon_code = weather_data["weather"][0]["icon"]
    icon_url = "http://openweathermap.org/img/w/" + icon_code + ".png"

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        icon_code=icon_url,
    )

@app.route("/forecast")
def get_forecast():
    city = request.args.get("city")

    if not bool(city.strip()):
        city = "San Jose"

    forecast_data = get_weather_forecast(city)

    # City not found
    if not forecast_data["cod"] == "200":
        return render_template("city404.html")

    return render_template(
        "forecast.html",
        title=forecast_data["city"]["name"],
        forecast=forecast_data["list"],
    )


@app.route("/alerts")
def get_alerts():
    city = request.args.get("city")

    if not bool(city.strip()):
        city = "San Jose"

    alert_data = get_alerts(city)

    # City not found
    if not alert_data["cod"] == "200":
        return render_template("city404.html")

    return render_template(
        "alerts.html",
        title=alert_data["city"]["name"],
        alerts=alert_data["alerts"],
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
