import csv
from itertools import chain

import requests
from django.shortcuts import render
from pydash import join, chunk
from rest_framework import viewsets

from django.http import HttpResponse
from weather.models import ReportStation, ListNameStation, PmData, WeatherData
from weather.serializers import ReportStationSerializer, WeatherDataSerializer



class WeatherViewset(viewsets.ModelViewSet):
    serializer_class = ReportStationSerializer
    serializer_class = WeatherDataSerializer
    search_fields = ['name']

    def get_queryset(self):
        data_report = ReportStation.objects.all()
        data_weather = WeatherData.objects.all()
        # print(data)
        list_data = list(chain(data_report, data_weather))
        return list_data

    def save_reportstation(self):
        list_name = ListNameStation.objects.all()
        list_names = list(list_name.values_list('name'))
        # print("list_names")
        str_names = ""
        for j in list_names:
            str_names += join(j, ",") + ","
        names = str_names.split(",")
        chunked_names = chunk(names, 20)
        URL = "https://api.aprs.fi/api/get?"
        for j in chunked_names:
            name = join(j, ",")
            what = "loc"
            apikey = "149072.z1vz5VxaYwb5VkAm"
            format = "json"
            PARAMS = {'name':  name, 'what': what, 'apikey': apikey, 'format': format}
            api_request = requests.get(url=URL, params=PARAMS)
            print("call api 1")
            api_request.raise_for_status()
            data_weathers = api_request.json()
            for i in data_weathers['entries']:
                obj, is_created = ReportStation.objects.update_or_create(name=i["name"])
                # print(obj)
                for j in i:
                    setattr(obj, j, i[j])
                    # print(obj)
                    # print(j)
                obj.save()

    def save_weatherdata(self):
        queryset_pm = PmData.objects.all()
        queryset_names = ListNameStation.objects.all()

        list_names = list(queryset_names.values_list('name'))
        list_pm = list(queryset_pm.values('name', 'pm1', 'pm2_5', 'pm10'))
        # print("list_names")
        str_names = ""
        for j in list_names:
            str_names += join(j, ",") + ","
        names = str_names.split(",")
        chunked_names = chunk(names, 20)
        URL = "https://api.aprs.fi/api/get?"
        for j in chunked_names:
            name = join(j, ",")
            what = "wx"
            apikey = "149072.z1vz5VxaYwb5VkAm"
            format = "json"
            PARAMS = {'name': name, 'what': what, 'apikey': apikey, 'format': format}
            response = requests.get(url=URL, params=PARAMS)
            print("call api 2")
            response.raise_for_status()
            datas_weather = response.json()
            aprs_datas = datas_weather['entries']
            dict_data = {}
            for i in aprs_datas:
                for pm in list_pm:
                    if pm['name'] == i['name']:
                        i.update(pm)
                    pass
                # for i in aprs_datas:
                obj, is_created = WeatherData.objects.update_or_create(name=i["name"])
                # print(obj)
                for j in i:
                    setattr(obj, j, i[j])
                obj.save()


    # name = models.CharField(max_length=60, default='')
    # type_choices = [
    #     ('a', 'AIS'),
    #     ('l', 'APRS station'),
    #     ('i', 'APRS item'),
    #     ('o', 'APRS object'),
    #     ('w', 'weather station'),
    # ]
    # type = models.CharField(
    #     max_length=16,
    #     choices=type_choices,
    #     default='',
    # )
    # time = models.IntegerField(default=0)
    # lasttime = models.IntegerField(default=0)
    # lat = models.FloatField(default=0.00000)
    # lng = models.FloatField(default=0.00000)
    # comment = models.CharField(max_length=200, default='')