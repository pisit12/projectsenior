
from rest_framework import serializers
from .models import ReportStation, WeatherData, WeatherHistory


class ReportStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportStation
        fields = ['name', 'type', 'time', 'lasttime', 'lat', 'lat', 'lng',]
        read_only_fields = ['name', 'type', 'time', 'lasttime', 'lat', 'lat', 'lng',]

class WeatherDataSerializer(serializers.ModelSerializer):
    # station = ReportStationSerializer(source=station_id)
    class Meta:
        model = WeatherData
        fields = ['name', 'temp', 'time', 'pressure', 'humidity', 'wind_direction'
            , 'wind_speed', 'wind_gust', 'rain_1h'
            , 'rain_24h', 'rain_mn', 'luminosity']
        read_only_fields = [ 'name', 'temp', 'time', 'pressure', 'humidity', 'wind_direction'
            , 'wind_speed', 'wind_gust', 'rain_1h'
            , 'rain_24h', 'rain_mn', 'luminosity']

# class WeatherHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         Model = WeatherHistory
#         fields = ['temp_avg', 'temp_max', 'temp_min']
#         read_only_fields = ['temp_avg', 'temp_max', 'temp_min']
#

