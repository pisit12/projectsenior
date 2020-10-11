
from rest_framework import serializers
from .models import ReportStation, WeatherData


class ReportStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportStation
        fields = ['name', 'type', 'time', 'lasttime', 'lat', 'lat', 'lng',]
        read_only_fields = ['name', 'type', 'time', 'lasttime', 'lat', 'lat', 'lng',]

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['name', 'temp', 'time', 'pressure', 'humidity', 'wind_direction'
            , 'wind_speed', 'wind_gust', 'rain_1h'
            , 'rain_24h', 'rain_mn', 'luminosity']
        read_only_fields = ['name', 'temp', 'time', 'pressure', 'humidity', 'wind_direction'
            , 'wind_speed', 'wind_gust', 'rain_1h'
            , 'rain_24h', 'rain_mn', 'luminosity']


