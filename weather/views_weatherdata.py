from django.shortcuts import render
from rest_framework import viewsets, mixins
# Create your views here.
from rest_framework.viewsets import GenericViewSet

from weather.models import ReportStation, WeatherData
from weather.serializers import ReportStationSerializer, WeatherDataSerializer


class WeatherDataViewSet(mixins.ListModelMixin,
                   GenericViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer