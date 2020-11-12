from django.shortcuts import render
from rest_framework import viewsets, mixins
# Create your views here.
from rest_framework.response import Response

from weather.models import ReportStation , ListNameStation
from weather.serializers import ReportStationSerializer
from pydash import chunk, join
import requests


class ReportStationViewSet(mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = ReportStation.objects.all()
    serializer_class = ReportStationSerializer

    URL = "https://api.aprs.fi/api/get?"

    queryset_list_name=ListNameStation.objects.all()

    station_names=queryset_list_name.values_list('name_stations')
    list_names=list(station_names)
    str_names=""
    for j in list_names:
        str_names += join(j,",")+","
    names = str_names.split(",")
    chunked_names = chunk(names, 20)

    for j in chunked_names:
        name = join(j, ",")
        what = "loc"
        apikey = "149072.z1vz5VxaYwb5VkAm"
        format = "json"
        PARAMS = {'name': name, 'what': what, 'apikey': apikey, 'format': format}
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        a = data['entries']
        for i in a:
            obj, is_created = ReportStation.objects.get_or_create(name=i["name"])
            for j in i:
                setattr(obj, j, i[j])
            obj.save()
