from datetime import date
from itertools import groupby
from pydash import join
from rest_framework import viewsets, mixins
# from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from weather.models import WeatherHistory, PmData
from weather.models import WeatherData
from django.db.models import Avg, Max, Min, Count

from weather.serializers import WeatherHistorySerializer


class WeatherHistoryViewSet(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = WeatherHistory.objects.all()
    serializer_class = WeatherHistorySerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name','id']

    list_history = list(queryset)
    # print(list_history)
    queryset_datas = WeatherData.objects.all()
    # ควรเอาไอดีไปใช้แล้ว เอาค่าที่เหลือจะตามมา
    queryset_pm = PmData.objects.all()

    list_pm = list(queryset_pm.values('name','pm1'))
    list_datas = list(queryset_datas.values('name', 'temp','date_created'))
       # เพิ่ม id ได้ โดยให้ his_id=id\
    # date_created__day ก็มี
    list_all=[]
    list_all = list_datas+list_pm
    # print(list_all)
    # print(list_pm)
    dict_all={}

        # print(datas)
    dict_temp= {}
    list_temp = []
    # print(list_datas
    # for j in list_all:
    #     try:
    #         # print(j)
    #         # print(queryset.filter(date_created__date=date.today(),name=j['name']))
    #         # print(WeatherData.objects.filter(name=j['name']).aggregate(Avg('temp')))
    #         if list_history ==[]:
    #             # print(j)
    #             avg_temp_new = WeatherData.objects.filter(name=j['name']).aggregate(Avg('temp'))
    #             max_temp_new = WeatherData.objects.filter(name=j['name']).aggregate(Max('temp'))
    #             min_temp_new = WeatherData.objects.filter(name=j['name']).aggregate(Min('temp'))
    #
    #             avg_pm1_new = PmData.objects.filter(name=j['name']).aggregate(Avg('pm1'))
    #             max_pm1_new = PmData.objects.filter(name=j['name']).aggregate(Max('pm1'))
    #             min_pm1_new = PmData.objects.filter(name=j['name']).aggregate(Min('pm1'))
    #             # print(avg_pm1_new)
    #             # avg_pm2_5_new = PmData.objects.filter(name=j['name']).aggregate(Avg('pm2_5'))
    #             # max_pm2_5_new = PmData.objects.filter(name=j['name']).aggregate(Max('pm2_5'))
    #             # min_pm2_5_new = PmData.objects.filter(name=j['name']).aggregate(Min('pm2_5'))
    #             #
    #             # avg_pm10_new = PmData.objects.filter(name=j['name']).aggregate(Avg('pm10'))
    #             # max_pm10_new = PmData.objects.filter(name=j['name']).aggregate(Max('pm10'))
    #             # min_pm10_new = PmData.objects.filter(name=j['name']).aggregate(Min('pm10'))
    #             # print(avg_temp)
    #             dict_temp.update(j)
    #             dict_temp.update(avg_temp_new)
    #             dict_temp.update(max_temp_new)
    #             dict_temp.update(min_temp_new)
    #
    #             dict_temp.update(avg_pm1_new)
    #             dict_temp.update(max_pm1_new)
    #             dict_temp.update(min_pm1_new)
    #             # print(dict_temp)
    #
    #             # dict_temp.update(avg_pm2_5_new)
    #             # dict_temp.update(max_pm2_5_new)
    #             # dict_temp.update(min_pm2_5_new)
    #             #
    #             # dict_temp.update(avg_pm10_new)
    #             # dict_temp.update(max_pm10_new)
    #             # dict_temp.update(min_pm10_new)
    #             dict_temp_copy = dict_temp.copy()
    #             list_temp.append(dict_temp_copy)
    #
    #             # print(list_temp)
    #         else:
    #             # avg
    #             count_tempp=WeatherHistory.objects.filter(name=j['name']).count()
    #             # print(count_tempp)
    #             count_pm=PmData.objects.filter(name=j['name']).count()
    #             # print(count_pm)
    #             # print(j)
    #             #temp
    #             avg_temp=WeatherHistory.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(Avg('temp'))
    #             # print(avg_temp)
    #             avg_temp_new = WeatherData.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(Avg('temp'))
    #             j['temp__avg']=((avg_temp_new['temp__avg']*count_tempp)+avg_temp['temp__avg'])/(count_tempp+1) # calculate avg
    #             # print(avg_temp_new)
    #             # max
    #             max_temp_new = WeatherData.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(Max('temp'))
    #             max_temp = WeatherHistory.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(Max('temp'))
    #             if max_temp_new['temp__max'] >= max_temp['temp__max']:
    #                 max_temp['temp__max'] = max_temp_new['temp__max']
    #             j['temp__max'] = max_temp['temp__max']
    #             # min
    #             min_temp_new = WeatherData.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(Min('temp'))
    #             min_temp = WeatherHistory.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(Min('temp'))
    #             if min_temp_new['temp__min'] <= min_temp['temp__min']:
    #                 min_temp['temp__min'] = min_temp_new['temp__min']
    #             j['temp__min']=min_temp['temp__min']
    #             # print(min_temp)
    #             #pm
    #             # if WeatherHistory.objects.filter(name=j['name'],pm1=j['pm1']) ==[]:
    #             avg_pm1 = WeatherHistory.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(
    #                 Avg('pm1'))
    #             # print(avg_pm1)
    #             avg_pm1_new = PmData.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(
    #                 Avg('pm1'))
    #             j['pm1__avg'] = ((avg_pm1_new['pm1__avg'] * count_pm) + avg_pm1['pm1__avg']) / (
    #                             count_pm + 1)  # calculate avg
    #                 # max
    #             max_pm1_new = PmData.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(
    #                     Max('pm1'))
    #             max_pm1 = WeatherHistory.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(
    #                     Max('pm1'))
    #             if max_pm1_new['pm1__max'] >= max_pm1['pm1__max']:
    #                 max_pm1['pm1__max'] = max_pm1_new['pm1__max']
    #             j['pm1__max'] = max_pm1['pm1__max']
    #                 # min
    #             min_pm1_new = PmData.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(
    #                 Min('pm1'))
    #             min_pm1 = WeatherHistory.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(
    #                 Min('pm1'))
    #             if min_pm1_new['pm1__min'] <= min_pm1['pm1__min']:
    #                 min_pm1['pm1__min'] = min_pm1_new['pm1__min']
    #             j['pm1__min'] = min_pm1['pm1__min']
    #
    #             dict_temp.update(j)
    #             # print(dict_temp)
    #             dict_temp_copy = dict_temp.copy()
    #             list_temp.append(dict_temp_copy)
    #     except:
    #         # print(j)
    #         # avg_temp = WeatherHistory.objects.filter(name=j['name'], date_created__date=date.today()).aggregate(
    #         #     Avg('temp'))
    #         # print(avg_temp)
    #         pass
    # for i in list_temp:
    #     try:
    #         # print(i)
    #         obj= WeatherHistory.objects.create(
    #             name=i['name'],temp=i['temp'], temp_avg=i['temp__avg'],
    #             temp_max=i['temp__max'], temp_min=i['temp__min'],pm1_avg=i['pm1__avg'],
    #             pm1_max=i['pm1__max'],pm1_min=i['pm1__min'],pm1=i['pm1'])
    #         # print(obj)
    #         # obj = WeatherHistory.objects.create(name=i['name'],
    #         #                                     temp=i['temp'], temp_avg=i['temp__avg'],
    #         #                                     temp_max=i['temp__max'], temp_min=i['temp__min'])
    #         # print(obj)
    #         for j in i:
    #             setattr(obj,j,i[j])
    #             # print(j)
    #             # print(i[j])
    #         # print(obj)
    #         obj.save()
    #     except:
    #         # print(i)
    #         obj = WeatherHistory.objects.create(
    #             name=i['name'],temp=i['temp'], temp_avg=i['temp__avg'],
    #             temp_max=i['temp__max'], temp_min=i['temp__min'])
    #         # print(obj)
    #         for j in i:
    #             setattr(obj, j, i[j])
    #             # print(j)
    #             # print(i[j])
    #         obj.save()
    #
    #         # print(i)
    #         pass