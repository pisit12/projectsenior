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


    # print(list_history)
    queryset_datas = WeatherData.objects.all()
    # ควรเอาไอดีไปใช้แล้ว เอาค่าที่เหลือจะตามมา
    # queryset_pm = PmData.objects.all()

    list_history = list(queryset)
    list_datas = list(queryset_datas.values('name', 'temp', 'pressure', 'humidity'
                                            , 'pm1', 'pm2_5', 'pm10', ))
    # เพิ่ม id ได้ โดยให้ his_id=id\
    dict_all = {}
    list_all = []
    for j in list_datas:
        try:
            if list_history == []:
                # print(j)
                # print("avg_temp")
                avg_temp_new = WeatherData.objects.filter(name=j['name']).aggregate(Avg('temp'))
                max_temp_new = WeatherData.objects.filter(name=j['name']).aggregate(Max('temp'))
                min_temp_new = WeatherData.objects.filter(name=j['name']).aggregate(Min('temp'))

                avg_pressure_new = WeatherData.objects.filter(name=j['name']).aggregate(Avg('pressure'))
                max_pressure_new = WeatherData.objects.filter(name=j['name']).aggregate(Max('pressure'))
                min_pressure_new = WeatherData.objects.filter(name=j['name']).aggregate(Min('pressure'))

                avg_humidity_new = WeatherData.objects.filter(name=j['name']).aggregate(Avg('humidity'))
                max_humidity_new = WeatherData.objects.filter(name=j['name']).aggregate(Max('humidity'))
                min_humidity_new = WeatherData.objects.filter(name=j['name']).aggregate(Min('humidity'))

                avg_pm1_new = WeatherData.objects.filter(name=j['name']).aggregate(Avg('pm1'))
                max_pm1_new = WeatherData.objects.filter(name=j['name']).aggregate(Max('pm1'))
                min_pm1_new = WeatherData.objects.filter(name=j['name']).aggregate(Min('pm1'))
                #
                avg_pm2_5_new = WeatherData.objects.filter(name=j['name']).aggregate(Avg('pm2_5'))
                max_pm2_5_new = WeatherData.objects.filter(name=j['name']).aggregate(Max('pm2_5'))
                min_pm2_5_new = WeatherData.objects.filter(name=j['name']).aggregate(Min('pm2_5'))
                #
                avg_pm10_new = WeatherData.objects.filter(name=j['name']).aggregate(Avg('pm10'))
                max_pm10_new = WeatherData.objects.filter(name=j['name']).aggregate(Max('pm10'))
                min_pm10_new = WeatherData.objects.filter(name=j['name']).aggregate(Min('pm10'))

                dict_all.update(j)
                dict_all.update(avg_temp_new)
                dict_all.update(max_temp_new)
                dict_all.update(min_temp_new)

                dict_all.update(avg_pressure_new)
                dict_all.update(max_pressure_new)
                dict_all.update(min_pressure_new)

                dict_all.update(avg_humidity_new)
                dict_all.update(max_humidity_new)
                dict_all.update(min_humidity_new)

                dict_all.update(avg_pm1_new)
                dict_all.update(max_pm1_new)
                dict_all.update(min_pm1_new)

                dict_all.update(avg_pm2_5_new)
                dict_all.update(max_pm2_5_new)
                dict_all.update(min_pm2_5_new)
                #
                dict_all.update(avg_pm10_new)
                dict_all.update(max_pm10_new)
                dict_all.update(min_pm10_new)

                dict_all_copy = dict_all.copy()
                list_all.append(dict_all_copy)
            else:
                # avg

                count_weather = WeatherHistory.objects.filter(name=j['name']).count()

                # print(count_tempp)
                count_pm = PmData.objects.filter(name=j['name']).count()
                print("8888888")
                # temp
                avg_temps = WeatherData.objects.all().filter(name=j['name']).aggregate(Avg('temp'))
                print(avg_temps)

                avg_temp = WeatherHistory.objects.filter(name=j['name'],
                                                         date_created__date=date.today()).aggregate(Avg('temp'))
                print(avg_temp)
                avg_temp_new = WeatherData.objects.filter(name=j['name'],
                                                          date_created__date=date.today()).aggregate(Avg('temp'))
                print("777777")
                j['temp__avg'] = ((avg_temp_new['temp__avg'] * count_weather) + avg_temp['temp__avg']) / (
                            count_weather + 1)  # calculate avg
                max_temp_new = WeatherData.objects.filter(name=j['name'],
                                                          date_created__date=date.today()).aggregate(Max('temp'))
                max_temp = WeatherHistory.objects.filter(name=j['name'],
                                                         date_created__date=date.today()).aggregate(Max('temp'))
                if max_temp_new['temp__max'] >= max_temp['temp__max']:
                    max_temp['temp__max'] = max_temp_new['temp__max']
                j['temp__max'] = max_temp['temp__max']
                min_temp_new = WeatherData.objects.filter(name=j['name'],
                                                          date_created__date=date.today()).aggregate(Min('temp'))
                min_temp = WeatherHistory.objects.filter(name=j['name'],
                                                         date_created__date=date.today()).aggregate(Min('temp'))
                if min_temp_new['temp__min'] <= min_temp['temp__min']:
                    min_temp['temp__min'] = min_temp_new['temp__min']
                j['temp__min'] = min_temp['temp__min']
                # pm
                avg_pm1 = WeatherHistory.objects.filter(name=j['name'],
                                                        date_created__date=date.today()).aggregate(Avg('pm1'))
                # print(avg_pm1)
                avg_pm1_new = WeatherData.objects.filter(name=j['name'],
                                                         date_created__date=date.today()).aggregate(Avg('pm1'))
                j['pm1__avg'] = ((avg_pm1_new['pm1__avg'] * count_pm) + avg_pm1['pm1__avg']) / (
                        count_pm + 1)  # calculate avg
                #
                max_pm1_new = WeatherData.objects.filter(name=j['name'],
                                                         date_created__date=date.today()).aggregate(Max('pm1'))
                max_pm1 = WeatherHistory.objects.filter(name=j['name'],
                                                        date_created__date=date.today()).aggregate(Max('pm1'))
                if max_pm1_new['pm1__max'] >= max_pm1['pm1__max']:
                    max_pm1['pm1__max'] = max_pm1_new['pm1__max']
                j['pm1__max'] = max_pm1['pm1__max']
                min_pm1_new = WeatherData.objects.filter(name=j['name'],
                                                         date_created__date=date.today()).aggregate(Min('pm1'))
                min_pm1 = WeatherHistory.objects.filter(name=j['name'],
                                                        date_created__date=date.today()).aggregate(Min('pm1'))
                if min_pm1_new['pm1__min'] <= min_pm1['pm1__min']:
                    min_pm1['pm1__min'] = min_pm1_new['pm1__min']
                j['pm1__min'] = min_pm1['pm1__min']

                avg_pm2_5 = WeatherHistory.objects.filter(name=j['name'],
                                                          date_created__date=date.today()).aggregate(Avg('pm2_5'))
                avg_pm2_5_new = WeatherData.objects.filter(name=j['name'],
                                                           date_created__date=date.today()).aggregate(Avg('pm2_5'))
                j['pm2_5__avg'] = ((avg_pm2_5_new['pm2_5__avg'] * count_pm) + avg_pm2_5['pm2_5__avg']) / (
                        count_pm + 1)  # calculate avg
                max_pm2_5_new = WeatherData.objects.filter(name=j['name'],
                                                           date_created__date=date.today()).aggregate(Max('pm2_5'))
                max_pm2_5 = WeatherHistory.objects.filter(name=j['name'],
                                                          date_created__date=date.today()).aggregate(Max('pm2_5'))
                if max_pm2_5_new['pm2_5__max'] >= max_pm2_5['pm2_5__max']:
                    max_pm2_5['pm2_5__max'] = max_pm2_5_new['pm2_5__max']
                j['pm2_5__max'] = max_pm1['pm2_5__max']
                min_pm2_5_new = WeatherData.objects.filter(name=j['name'],
                                                           date_created__date=date.today()).aggregate(Min('pm2_5'))
                min_pm2_5 = WeatherHistory.objects.filter(name=j['name'],
                                                          date_created__date=date.today()).aggregate(Min('pm2_5'))
                if min_pm2_5_new['pm2_5__min'] <= min_pm2_5['pm2_5__min']:
                    min_pm2_5['p2_5__min'] = min_pm2_5_new['pm2_5__min']
                j['pm2_5__min'] = min_pm1['pm2_5__min']

                avg_pm10 = WeatherHistory.objects.filter(name=j['name'],
                                                         date_created__date=date.today()).aggregate(Avg('pm10'))
                avg_pm10_new = WeatherData.objects.filter(name=j['name'],
                                                          date_created__date=date.today()).aggregate(Avg('pm10'))
                j['pm10__avg'] = ((avg_pm10_new['pm10__avg'] * count_pm) + avg_pm10['pm10__avg']) / (
                        count_pm + 1)  # calculate avg
                max_pm10_new = WeatherData.objects.filter(name=j['name'],
                                                          date_created__date=date.today()).aggregate(Max('pm10'))
                max_pm10 = WeatherHistory.objects.filter(name=j['name'],
                                                         date_created__date=date.today()).aggregate(Max('pm10'))
                if max_pm10_new['pm10__max'] >= max_pm10['pm10__max']:
                    max_pm10['pm10__max'] = max_pm10_new['pm10__max']
                j['pm10__max'] = max_pm10['pm10__max']
                min_pm10_new = WeatherData.objects.filter(name=j['name'],
                                                          date_created__date=date.today()).aggregate(Min('pm10'))
                min_pm10 = WeatherHistory.objects.filter(name=j['name'],
                                                         date_created__date=date.today()).aggregate(Min('pm10'))
                if min_pm10_new['pm10__min'] <= min_pm10['pm10__min']:
                    min_pm10['pm10__min'] = min_pm10_new['pm10__min']
                j['pm10__min'] = min_pm10['pm10__min']
                # pressure
                avg_pressure = WeatherHistory.objects.filter(name=j['name'],
                                                             date_created__date=date.today()).aggregate(Avg('pressure'))
                avg_pressure_new = WeatherData.objects.filter(name=j['name'],
                                                              date_created__date=date.today()).aggregate(
                    Avg('pressure'))
                j['pressure__avg'] = ((avg_pressure_new['pressure__avg'] * count_weather) + avg_pressure[
                    'pressure__avg']) / (
                                             count_weather + 1)  # calculate avg
                max_pressure_new = WeatherData.objects.filter(name=j['name'],
                                                              date_created__date=date.today()).aggregate(
                    Max('pressure'))
                max_pressure = WeatherHistory.objects.filter(name=j['name'],
                                                             date_created__date=date.today()).aggregate(Max('pressure'))
                if max_pressure_new['pressure__max'] >= max_pressure['pressure__max']:
                    max_pressure['pressure__max'] = max_pressure_new['pressure__max']
                j['pressure__max'] = max_pressure['pressure__max']
                min_pressure_new = WeatherData.objects.filter(name=j['name'],
                                                              date_created__date=date.today()).aggregate(
                    Min('pressure'))
                min_pressure = WeatherHistory.objects.filter(name=j['name'],
                                                             date_created__date=date.today()).aggregate(Min('pressure'))
                if min_pressure_new['pressure__min'] <= min_pressure['pressure__min']:
                    min_pressure['pressure__min'] = min_pressure_new['pressure__min']
                j['pressure__min'] = min_pressure['pressure__min']
                # humi
                avg_humidity = WeatherHistory.objects.filter(name=j['name'],
                                                             date_created__date=date.today()).aggregate(Avg('humidity'))
                avg_humidity_new = WeatherData.objects.filter(name=j['name'],
                                                              date_created__date=date.today()).aggregate(
                    Avg('humidity'))
                j['humidity__avg'] = ((avg_humidity_new['humidity__avg'] * count_weather) + avg_humidity[
                    'humidity__avg']) / (
                                             count_weather + 1)  # calculate avg
                max_humidity_new = WeatherData.objects.filter(name=j['name'],
                                                              date_created__date=date.today()).aggregate(
                    Max('humidity'))
                max_humidity = WeatherHistory.objects.filter(name=j['name'],
                                                             date_created__date=date.today()).aggregate(Max('humidity'))
                if max_humidity_new['humidity__max'] >= max_humidity['humidity__max']:
                    max_humidity['humidity__max'] = max_humidity_new['humidity__max']
                j['humidity__max'] = max_humidity['humidity__max']
                min_humidity_new = WeatherData.objects.filter(name=j['name'],
                                                              date_created__date=date.today()).aggregate(
                    Min('humidity'))
                min_humidity = WeatherHistory.objects.filter(name=j['name'],
                                                             date_created__date=date.today()).aggregate(Min('humidity'))
                if min_humidity_new['humidity__min'] <= min_humidity['humidity__min']:
                    min_humidity['humidity__min'] = min_humidity_new['humidity__min']
                j['humidity__min'] = min_humidity['humidity__min']

                dict_all.update(j)
                # print(dict_temp)
                dict_all_copy = dict_all.copy()
                list_all.append(dict_all_copy)
        except:
            pass
    for i in list_all:
        try:
            # print(i)
            obj = WeatherHistory.objects.create(
                name=i['name'],
                temp=i['temp'],
                temp_avg=i['temp__avg'], temp_max=i['temp__max'], temp_min=i['temp__min'],
                pm1=i['pm1'],
                pm1_avg=i['pm1__avg'], pm1_max=i['pm1__max'], pm1_min=i['pm1__min'],
                pm2_5=i['pm2_5'],
                pm2_5_avg=i['pm2_5__avg'], pm2_5_min=i['pm2_5__min'], pm2_5_max=i['pm2_5__max'],
                pm10=i['pm10'],
                pm10_avg=i['pm10__avg'], pm10_max=i['pm10__max'], pm10_min=i['pm10__min'],
                pressure=i['pressure'],
                pressure_avg=i['pressure__avg'], pressure_max=i['pressure__max'], pressure_min=i['pressure__min'],
                humidity=i['humidity'],
                humidity_avg=i['humidity__avg'], humidity_max=i['humidity__max'], humidity_min=i['humidity__min'], )
            for j in i:
                setattr(obj, j, i[j])
                # print(j)
                # print(i[j])
            # print(obj)
            obj.save()
        except:
            # print(i)
            obj = WeatherHistory.objects.create(
                name=i['name'],
                temp=i['temp'],
                temp_avg=i['temp__avg'], temp_max=i['temp__max'], temp_min=i['temp__min'],
                pressure=i['pressure'],
                pressure_avg=i['pressure__avg'], pressure_max=i['pressure__max'], pressure_min=i['pressure__min'],
                humidity=i['humidity'],
                humidity_avg=i['humidity__avg'], humidity_max=i['humidity__max'], humidity_min=i['humidity__min'],
            )
            # print(obj)
            for j in i:
                setattr(obj, j, i[j])
                # print(j)
                # print(i[j])
            obj.save()
            # print(i)
            pass
