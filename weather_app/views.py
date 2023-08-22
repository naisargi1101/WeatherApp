from datetime import datetime
import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    API_KEY = open("D:\WeatherApp\weather_app\API_KEY", "r").read()
    #print(API_KEY)
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"
    #forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        city1 = request.POST["city1"]
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecast1 = fetch_weather_and_forecast(city1,current_weather_url,forecast_url,API_KEY)
        if city2:
            weather_data2, daily_forecast2 = fetch_weather_and_forecast(city2,current_weather_url,forecast_url,API_KEY)
        else:
            weather_data2, daily_forecast2 = None, None
        context = {
            "weather_data1": weather_data1,
            "daily_forecast1": daily_forecast1,
            "weather_data2": weather_data2,
            "daily_forecast2": daily_forecast2,
        }
        return render(request, "weather_app/index.html", context)
    
    else:
        return render(request, "weather_app/index.html")

# Get current weather data
def fetch_weather_and_forecast(city,current_weather_url,forecast_url,api_key):

    current_weather = requests.get(current_weather_url.format(city,api_key)).json()
    # #print(current_weather)
    lat,lon = current_weather['coord']['lat'], current_weather['coord']['lon']
    forecast = requests.get(forecast_url.format(lat,lon,api_key)).json()
    #print(forecast)
    weathe_data = {
        'city': city,
        'temperature': round(current_weather['main']['temp']- 273.15,2),
        'description': current_weather['weather'][0]['description'],
        'icon': current_weather['weather'][0]['icon']
    }

    daily_forecast = []
    for i in range(5):
        daily_forecast.append({
            'day': datetime.fromtimestamp(forecast['list'][i]['dt']).strftime("%A"),
            'time': datetime.fromtimestamp(forecast['list'][i]['dt']).strftime("%I%p"),
            'min_temp': round(forecast['list'][i]['main']['temp_min'] - 273.15, 2),
            'max_temp': round(forecast['list'][i]['main']['temp_max'] - 273.15, 2),
            'description': forecast['list'][i]['weather'][0]['description'],
            'icon': forecast['list'][i]['weather'][0]['icon']
        })

    return weathe_data, daily_forecast
