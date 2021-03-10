import csv
from itertools import chain

import requests
from django.shortcuts import render
from pydash import join, chunk
from rest_framework import viewsets

from django.http import HttpResponse
from weather.models import ReportStation, ListNameStation, PmData, WeatherData, WeatherHistory
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
            apikey = "155078.nzsdK4hEn2R2n13o"
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
            apikey = "155078.nzsdK4hEn2R2n13o"
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

    def export(self):
        # Create the HttpResponse object with the appropriate CSV header.
        with open('test.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name','temp', 'temp_avg', 'temp_max', 'temp_min',
                            'pressure', 'pressure_avg', 'pressure_max','pressure_min',
                            'humidity', 'humidity_avg', 'humidity_max',
                            'humidity_min','pm1', 'pm1_avg', 'pm1_max', 'pm1_min',
                            'pm2_5', 'pm2_5_avg', 'pm2_5_max', 'pm2_5_min',
                            'pm10', 'pm10_avg', 'pm10_max', 'pm10_min', ])
            for history in WeatherHistory.objects.all().values_list('id', 'name',
                                                                  'temp', 'temp_avg', 'temp_max', 'temp_min',
                                                                  'pressure', 'pressure_avg', 'pressure_max',
                                                                  'pressure_min',
                                                                  'humidity', 'humidity_avg', 'humidity_max',
                                                                  'humidity_min',
                                                                  'pm1', 'pm1_avg', 'pm1_max', 'pm1_min',
                                                                  'pm2_5', 'pm2_5_avg', 'pm2_5_max', 'pm2_5_min',
                                                                  'pm10', 'pm10_avg', 'pm10_max', 'pm10_min', ):
                writer.writerow(history)

    def call_schedu(self):
        self.save_reportstation()
        self.save_weatherdata()
        self.export()
