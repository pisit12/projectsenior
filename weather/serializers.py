
from rest_framework import serializers
from .models import ReportStation, WeatherData


class ReportStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportStation
        fields = ['name', 'location', 'temp', 'humid', 'pressure', 'pm2_5', 'pm10', 'wind']
        read_only_fields = ['name', 'location', 'temp', 'humid', 'pressure', 'pm2_5', 'pm10', 'wind']

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['__all__']
        read_only_fields = ['__all__']


