import csv
import re
from datetime import datetime, date

from itertools import chain

import pytz
import requests
from django.shortcuts import render
from pydash import join, chunk
from rest_framework import viewsets

from django.http import HttpResponse
from weather.models import ReportStation, ListNameStation, PmData, WeatherData, WeatherHistory
from weather.serializers import ReportStationSerializer, WeatherDataSerializer, WeatherHistorySerializer


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
            # 149072.5M4NG9sB5ZNWSCx
            # 155078.nzsdK4hEn2R2n13o
            format = "json"
            PARAMS = {'name':  name, 'what': what, 'apikey': apikey, 'format': format}
            api_request = requests.get(url=URL, params=PARAMS)
            # print("call api 1")
            api_request.raise_for_status()
            data_weathers = api_request.json()
            aprs_datas = data_weathers['entries']
            for i in aprs_datas:
                date_data = {}
                timestamp = i['lasttime']
                date_time = datetime.fromtimestamp(int(timestamp))
                timezone = pytz.timezone("Asia/Bangkok")
                i['date_time'] = date_time.astimezone(timezone)
                date_data.update(i)
                i.update(date_data)
                obj, is_created = ReportStation.objects.update_or_create(name=i["name"])
                for j in i:
                    setattr(obj, j, i[j])
                obj.save()

    def save_pm(self):
        queryset_station = ReportStation.objects.all()
        list_pm = list(queryset_station.values('name', 'comment'))
        pm_total = []
        pmdata = []
        for i in list_pm:
            # print(i['comment'])
            name_pm = i['comment'].split("PM")
            # print(name_pm)
            try:
                # print(name_pm[1])
                num_pm = re.findall(r'(?<=\[)(.*?)(?=\])', name_pm[1])  # x
                # print(num_pm)
                list_key = ['pm1', 'pm2_5', 'pm10']  # j
                output = {}
                output.update(i)
                for j, x in enumerate(num_pm):
                    # print(x)
                    output[list_key[j]] = x
                    # print(output)
                pmdata.append(output)
                # print(pmdata)
            except:
                pass

        for i in pmdata:
            try:
                obj, is_created = PmData.objects.update_or_create(
                    name=i['name'], pm1=i['pm1'],
                    pm2_5=i['pm2_5'], pm10=i['pm10'])
                for j in i:
                    setattr(obj, j, i[j])
                    # print(i[j])
                obj.save()
            except:
                # print(i)
                pass

    def save_weatherdata(self):
        queryset_pm = PmData.objects.all()
        queryset_names = ListNameStation.objects.all()

        list_names = list(queryset_names.values_list('name'))
        list_pm = list(queryset_pm.values('name', 'pm1', 'pm2_5', 'pm10'))

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

            response.raise_for_status()
            datas_weather = response.json()
            aprs_datas = datas_weather['entries']
            for i in aprs_datas:
                for pm in list_pm:
                    if pm['name'] == i['name']:
                        i.update(pm)
                    pass
                date_data = {}
                timestamp = i['time']
                date_time = datetime.fromtimestamp(int(timestamp))
                timezone = pytz.timezone("Asia/Bangkok")
                i['date_time'] = date_time.astimezone(timezone)
                date_data.update(i)
                i.update(date_data)
                obj, is_created = WeatherData.objects.update_or_create(name=i["name"])

                for j in i:
                    setattr(obj, j, i[j])
                obj.save()

    def history(self):
        queryset = WeatherHistory.objects.all()
        queryset_datas = WeatherData.objects.all()
        list_history = list(queryset.values_list('name', 'temp', 'temp_avg', 'temp_max', 'temp_min', 'date_time', ))
        list_datas = list(queryset_datas.values('name', 'temp', 'date_time'))
        dict_all = {}
        list_all = []
        if list_history == []:
            print(list_history)
            for j in list_datas:
                try:
                    j['temp_avg'] = j['temp']
                    j['temp_max'] = j['temp']
                    j['temp_min'] = j['temp']
                    dict_all.update(j)
                    dict_all_copy = dict_all.copy()
                    list_all.append(dict_all_copy)
                except:
                    pass
        else:
            try:
                for j in list_datas:
                    count = 0
                    for i in list_history:
                        if i['name'] == j['name']:
                            count += 1
                            if i['temp_min'] >= j['temp']:
                                j['temp_min'] = j['temp']
                            j['temp_min'] = i['temp_min']
                            if i['temp_max'] <= j['temp']:
                                j['temp_max'] = j['temp']
                            j['temp_max'] = i['temp_max']
                    j['temp_avg'] = (i['temp_avg'] * count + j['temp']) / count + 1
                    dict_all.update(j)
                    dict_all_copy = dict_all.copy()
                    list_all.append(dict_all_copy)
            except:
                pass
        for i in list_all:
            try:
                obj = WeatherHistory.objects.create(name=i['name'])
                for j in i:
                    setattr(obj, j, i[j])
                obj.save()
                pass
            except:
                pass

    def export(self):
        with open('./weather_history.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name','temp', 'temp_avg', 'temp_max', 'temp_min','date_time',])

            for data in WeatherHistory.objects.all().values_list('id', 'name','temp', 'temp_avg',
                                                              'temp_max', 'temp_min','date_time', ):
                writer.writerow(data)

    def call_schedu(self):
        self.save_reportstation()
        self.save_pm()
        self.save_weatherdata()
        self.history()
        self.export()
