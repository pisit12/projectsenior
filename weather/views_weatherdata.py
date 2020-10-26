import requests
from django.shortcuts import render
from rest_framework import viewsets, mixins
# Create your views here.

from weather.models import WeatherData
from weather.serializers import WeatherDataSerializer


class WeatherDataViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer

    URL = "https://api.aprs.fi/api/get?what=wx&apikey=149072.z1vz5VxaYwb5VkAm&format=json"
    name = "FW6985"
    PARAMS = {'name': name}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    a = data['entries'][0]
    for i in a:
        if i == 'name':
            name = a[i]
            # WeatherData.objects.create(name=name)
        if i == 'time':
            time = a[i]
            # WeatherData.objects.create(time=time)
        if i == 'temp':
            temp = a[i]
            # WeatherData.objects.create(temp=temp)
        if i == 'pressure':
            pressure = a[i]
            # WeatherData.objects.create(pressure=pressure)
        if i == 'humidity':
            humidity = a[i]
            # WeatherData.objects.create(humidity=humidity)
        if i == 'wind_direction':
            wind_direction = a[i]
            # WeatherData.objects.create(wind_direction=wind_direction)
        if i == 'wind_speed':
            wind_speed = a[i]
            # WeatherData.objects.create(wind_speed=wind_speed)
        if i == 'wind_gust':
            wind_gust = a[i]
            # WeatherData.objects.create(wind_gust=wind_gust)
        if i == 'rain_1h':
            rain_1h = a[i]
            # WeatherData.objects.create(rain_1h=rain_1h)
        if i == 'rain_24h':
            rain_24h = a[i]
            # WeatherData.objects.create(rain_24h=rain_24h)
        if i == 'rain_mn':
            rain_mn = a[i]
            # WeatherData.objects.create(rain_mn=rain_mn)
        if i == 'luminosity':
            luminosity = a[i]
            # WeatherData.objects.create(luminosity=luminosity)
    WeatherData.objects.create(name=name, time=time, temp=temp,
                               pressure=pressure, humidity=humidity,
                               wind_direction=wind_direction, wind_speed=wind_speed,
                               wind_gust=wind_gust, rain_1h=rain_1h, rain_24h=rain_24h,
                               rain_mn=rain_mn, luminosity=luminosity).save()
    #     วนรับเอา