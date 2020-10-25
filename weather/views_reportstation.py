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
    # ReportStation.push()
    URL = "https://api.aprs.fi/api/get?&what=loc&apikey=149072.z1vz5VxaYwb5VkAm&format=json"

    # location given here
    name = "OH7RDA"
    # lat = "63.06717"
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'name': name}
    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)
    # extracting data in json format
    # extracting latitude, longitude and formatted address
    # of the first matching location
    # latitude = data['entries']['lat']
    # longitude = data['entries']['lng']
    # # printing the output
    # print("Latitude:%s\nLongitude:%s"% (latitude, longitude))
    data=r
    ReportStation.push(r.json())
    