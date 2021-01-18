import requests
from django.shortcuts import render
from pydash import chunk, join
from rest_framework import viewsets, mixins
# Create your views here.
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from weather.models import WeatherData, ListNameStation
from weather.serializers import WeatherDataSerializer


class WeatherDataViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    #permission_classes = (IsAuthenticated,)

    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer

    filter_backends = [SearchFilter]
    search_fields = ['id']

    # URL = "https://api.aprs.fi/api/get?"
    #
    # queryset_list_name = ListNameStation.objects.all()
    #
    # station_names = queryset_list_name.values_list('name_stations',)
    #
    # # station_names_id = queryset_list_name.values('id')
    # list_names = list(station_names)
    # str_names = ""
    # for j in list_names:
    #     str_names += join(j, ",") + ","
    # names = str_names.split(",")
    # chunked_names = chunk(names, 20)
    # # entries=[]
    #
    # for j in chunked_names:
    #     name = join(j, ",")
    #     what = "wx"
    #     apikey = "149072.z1vz5VxaYwb5VkAm"
    #     format = "json"
    #     PARAMS = {'name': name, 'what': what, 'apikey': apikey, 'format': format}
    #     r = requests.get(url=URL, params=PARAMS)
    #     data = r.json()
    #     a = data['entries']
    #     if data['entries']==[]:
    #         print(j)
    #     for i in a:
    #         obj,is_created = WeatherData.objects.update_or_create(name=i["name"])
    #         for j in i:
    #             setattr(obj,j,i[j])
    #         obj.save()

########################################


    # station_names_id = list(queryset_list_name.values('id', 'name_stations'))
    #
    # chunked_names = chunk(station_names_id, 20)
    # name_test = "HS9AN-10,HS9AS-10,HS9AT-10,HS8AK-10,HSAT-10"
    # names = name_test.split(",")
    # chunked_names = chunk(names, 1)
    # for j in chunked_names:
    #     name = join(j, ",")
    #     first_edit_name = join(j, ",")
    #     name = ListNameStation.objects.filter(id=j['id'])
    #     print(name)
    #     # name=first_edit_name(name=j['name_station'])
    #     # print(name)
    #     what = "wx"
    #     apikey = "149072.z1vz5VxaYwb5VkAm"
    #     format = "json"
    #     PARAMS = {'name': name, 'what': what, 'apikey': apikey, 'format': format}
        # r = requests.get(url=URL, params=PARAMS)
        # data = r.json()
        # test
        # data = {'command': 'get', 'result': 'ok', 'found': 20, 'what': 'wx', 'entries': [
        #     {'name': 'HS9AN-10', 'time': '1605399033', 'temp': '32.0', 'pressure': '1000.0', 'humidity': '75',
        #      'wind_direction': '0', 'wind_speed': '0.0', 'wind_gust': '0.0', 'luminosity': '0'},
        #     {'name': 'HS9AS-10', 'time': '1605398611', 'temp': '27.5', 'pressure': '1008.0', 'humidity': '65',
        #      'wind_direction': '0', 'wind_speed': '0.0', 'wind_gust': '0.0', 'luminosity': '0'},
        #     {'name': 'HS9AT-10', 'time': '1605397381', 'temp': '28.9', 'pressure': '1006.0', 'humidity': '88',
        #      'wind_direction': '0', 'wind_speed': '0.0', 'wind_gust': '0.0', 'luminosity': '0'},
        #     {'name': 'HS8AK-10', 'time': '1605398873', 'temp': '31.0', 'pressure': '1010.0', 'humidity': '70',
        #      'wind_direction': '0', 'wind_speed': '0.0', 'wind_gust': '0.0', 'luminosity': '0'},
        #     {'name': 'HS8AT-10', 'time': '1605398790', 'temp': '25.5', 'pressure': '1008.0', 'humidity': '66',
        #      'wind_direction': '0', 'wind_speed': '0.0', 'wind_gust': '0.0', 'luminosity': '0'},
        #     {'name': 'E23JWE-1', 'time': '1605398915', 'temp': '31.0', 'pressure': '1009.0', 'humidity': '69',
        #      'wind_direction': '0', 'wind_speed': '0.0', 'wind_gust': '0.0', 'luminosity': '17'}]}
        # a = data['entries']
        # for i in a:
        #     obj,is_created = WeatherData.objects.update_or_create(name=i["name"])
        #     for j in i:
        #         setattr(obj,j,i[j])
        #     # print(obj)
        #     obj.save()