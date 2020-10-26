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
    name = "FW6985"
    PARAMS = {'name': name}
    r = requests.get(url=URL, params=PARAMS)
    data=r.json()
    a=data['entries'][0]
    for i in a:
        if i == 'name':
            name=a[i]
            # ReportStation.objects.create(name=name)
        if i == 'type':
            type=a[i]
            # ReportStation.objects.create(type=type)
        if i == 'time':
            time=a[i]
            # ReportStation.objects.create(time=time)
        if i == 'lasttime':
            lasttime=a[i]
            # ReportStation.objects.create(lasttime=lasttime)
        if i == 'lat':
            lat=a[i]
            # ReportStation.objects.create(lat=lat)
        if i == 'lng':
            lng=a[i]
            # ReportStation.objects.create(lng=lng)
    ReportStation.objects.create(name=name, type=type, time=time,
                                 lasttime=lasttime, lat=lat, lng=lng).save()
    #     วนรับเอา

