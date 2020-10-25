from django.shortcuts import render
from rest_framework import viewsets, mixins
# Create your views here.

from weather.models import ReportStation, WeatherData
from weather.serializers import ReportStationSerializer

import requests

class ReportStationViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = ReportStation.objects.all()
    serializer_class = ReportStationSerializer
    # def get_queryset(self):
    #     user = self.request.user
    #     # return ReportStation.objects.all()

    r = requests.get('https://api.aprs.fi/api/get?name=OH7RDA&what=loc&apikey=APIKEY&format=json')
    
    print(r.json())
