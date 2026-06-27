import requests
from django.shortcuts import render
from .forms import CityForm

API_KEY = "6037fb2af16db2406ee628127f598fee"

def index(request):

    weather_data = None

    if request.method == "POST":

        form = CityForm(request.POST)

        if form.is_valid():

            city = form.cleaned_data["city"]

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

            response = requests.get(url)

            print(response.status_code)
            print(response.text)

            if response.status_code == 200:

                data = response.json()

                weather_data = {
                    "city": city.title(),
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind": data["wind"]["speed"],
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"],
                }

    else:
        form = CityForm()

    return render(
        request,
        "weather/index.html",
        {
            "form": form,
            "weather": weather_data
        }
    )

# Create your views here.
