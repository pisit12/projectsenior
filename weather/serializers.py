
from rest_framework import serializers
from .models import ReportStation, WeatherData, WeatherHistory, ListNameStation, PmData


class ListNameStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListNameStation
        fields = ['id','name',]
        read_only_fields = ['id',]

class ReportStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportStation
        fields = ['id','name', 'type', 'time', 'lasttime', 'lat', 'lat', 'lng','comment']
        read_only_fields = ['id','name', 'reportstation_id', 'type', 'time', 'lasttime', 'lat', 'lat', 'lng','comment'
                        ]

class WeatherDataSerializer(serializers.ModelSerializer):
    # station = ReportStationSerializer(source=station_id)
    # history = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = WeatherData
        fields = ['id', 'name', 'temp', 'time', 'pressure', 'humidity', 'wind_direction',
            'wind_speed', 'wind_gust', 'rain_1h',
            'rain_24h', 'rain_mn', 'luminosity',
            'pm1', 'pm2_5', 'pm10','date_created',]
        read_only_fields = ['id','name','temp', 'time', 'pressure', 'humidity', 'wind_direction',
            'wind_speed', 'wind_gust', 'rain_1h',
            'rain_24h', 'rain_mn', 'luminosity',
            'pm1', 'pm2_5', 'pm10','date_created',]

class WeatherHistorySerializer(serializers.ModelSerializer):
    # history= serializers.PrimaryKeyRelatedField(source='history_id', read_only=True)

    class Meta:
        model = WeatherHistory
        fields = ['id', 'name', 'temp', 'temp_avg', 'temp_max', 'temp_min','pm1','pm1_avg','pm1_max','pm1_min','date_created']
        read_only_fields = ['id', 'name', 'temp', 'temp_avg', 'temp_max', 'temp_min','pm1','pm1_avg','pm1_max','pm1_min','date_created']


class PmDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = PmData
        fields = ['id', 'name', 'pm1', 'pm2_5', 'pm10']
        read_only_field = ['id', 'name', 'pm1', 'pm2_5', 'pm10']
