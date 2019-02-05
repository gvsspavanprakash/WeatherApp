from django.shortcuts import render
import requests

from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=38a710d9dfee78c2cd586c5523af611f'
    template = 'weather/weather.html'
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'weather/weather.html')

    form = CityForm()
    cities = City.objects.all()

    weather_data = []
    counter = 0
    for city in cities:
        r = requests.get(url.format(city)).json()
        # counter += 1
        # if counter == 4:
        #     print(r, city)
        #     break
        if r['cod'] == 200 :
            city_weather = {
                'city' : city.name  ,
                'temparature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon'        : r['weather'][0]['icon'],
            }

            weather_data.append(city_weather)

    
    
    context  = {
        'weather_data' : weather_data,
        'form'         : form,
    }
    return render(request, template, context)