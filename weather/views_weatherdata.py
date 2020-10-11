from django.shortcuts import render
from rest_framework import viewsets, mixins
# Create your views here.

from weather.models import WeatherData
from weather.serializers import WeatherDataSerializer


class WeatherDataViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer