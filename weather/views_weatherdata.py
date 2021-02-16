import requests
from django.shortcuts import render
from pydash import chunk, join
from rest_framework import viewsets, mixins
# Create your views here.
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from weather.models import WeatherData, ListNameStation, PmData
from weather.serializers import WeatherDataSerializer


class WeatherDataViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    # permission_classes = (IsAuthenticated,)

    queryset = WeatherData.objects.all()
    # print(queryset)
    serializer_class = WeatherDataSerializer
    permission_classes = [AllowAny]

    filter_backends = [SearchFilter]
    search_fields = ['name', 'id']

    queryset_pm = PmData.objects.all()
    queryset_names = ListNameStation.objects.all()

    # def list(self, request, queryset_pm=queryset_pm,queryset_names=queryset_names, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     # print(queryset_pm)
    #     list_names = list(queryset_names.values_list('name'))
    #     list_pm = list(queryset_pm.values('name','pm1','pm2_5','pm10'))
    #     # dict_data = {}
    #     str_names = ""
    #     for j in list_names:
    #         str_names += join(j, ",") + ","
    #     names = str_names.split(",")
    #     chunked_names = chunk(names, 20)
    #     URL = "https://api.aprs.fi/api/get?"
    #     for j in chunked_names:
    #         name = join(j, ",")
    #         what = "wx"
    #         apikey = "149072.z1vz5VxaYwb5VkAm"
    #         format = "json"
    #         PARAMS = {'name': name, 'what': what, 'apikey': apikey, 'format': format}
    #         response = requests.get(url=URL, params=PARAMS)
    #         data = response.json()
    #         aprs_datas = data['entries']
    #         dict_data = {}
    #         # if data['entries']==[]:
    #         #     print(j)
    #         for i in aprs_datas:
    #             # print(i['name'])
    #             # print(i)
    #             for pm in list_pm:
    #                 if pm['name'] == i['name']:
    #                     i.update(pm)
    #                 pass
    #             #     print(j['name'])
    #             #     print(j)
    #         # for i in aprs_datas:
    #             obj, is_created = WeatherData.objects.update_or_create(name=i["name"])
    #             # print(obj)
    #             for j in i:
    #                 setattr(obj,j,i[j])
    #             obj.save()
    #         # for pm in list_pm:
    #         #     obj = WeatherData.objects.update(name=pm["name"])
    #         #     for j in pm:
    #         #         setattr(obj,j,pm[j])
    #         #         print(j)
    #         #         print(pm[j])

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

# print(i['name'])

#############################################
    list_names = list(queryset_names.values_list('name'))
    list_pm = list(queryset_pm.values('name', 'pm1', 'pm2_5', 'pm10'))
    # dict_data = {}
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
        PARAMS = {'name': name, 'what': what,
                  'apikey': apikey, 'format': format}
        response = requests.get(url=URL, params=PARAMS)
        data = response.json()
        aprs_datas = data['entries']
        dict_data = {}
        # if data['entries']==[]:
        #     print(j)
        for i in aprs_datas:
            # print(i['name'])
            # print(i)
            for pm in list_pm:
                if pm['name'] == i['name']:
                    i.update(pm)
                    pass
                #     print(j['name'])
                #     print(j)
            # for i in aprs_datas:
                obj, is_created = WeatherData.objects.update_or_create(
                    name=i["name"])
                # print(obj)
                for j in i:
                    setattr(obj, j, i[j])
                obj.save()
            # for pm in list_pm:
            #     obj = WeatherData.objects.update(name=pm["name"])
            #     for j in pm:
            #         setattr(obj,j,pm[j])
            #         print(j)
            #         print(pm[j])

########################################
