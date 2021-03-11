from datetime import date, datetime
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

    list_history = list(queryset)
    list_datas = list(queryset_datas.values('name', 'temp', 'pressure', 'humidity'
                                             , 'pm1', 'pm2_5', 'pm10', 'time'))
    dict_all = {}
    list_all = []
    for j in list_datas:
        try:
            if list_history is None:

                # datas_new = WeatherData.objects.all().filter(j['name']).aggregate(Avg('temp'))
                # j_data= j
                # datas_new = WeatherData.objects.all().filter(j['name']).aggregate(Avg('temp'),Max('temp'),Min('temp'),
                #                                         Avg('pressure'),Max('pressure'),Min('pressure'),
                #                                         Avg('humidity'),Max('humidity'),Min('humidity'),
                #                                         Avg('pm1'),Max('pm1'),Min('pm1'),
                #                                         Avg('pm2_5'),Max('pm2_5'),Min('pm2_5'),
                #                                         Avg('pm10'),Max('pm10'),Min('pm10'),)

                timestamp = j['time']
                # print(timestamp)
                data_datetime = datetime.fromtimestamp(timestamp)
                print(data_datetime)
                date_time = data_datetime.strftime('%Y-%m-%d ')
                print(date_time)
                # print(dt_object)

                dict_all.update(j)
                dict_all.update(datas_new)

                dict_all_copy = dict_all.copy()
                list_all.append(dict_all_copy)


            else:
                # avg
                count_weather = WeatherHistory.objects.filter(name=j['name']).count()
                # print(count_tempp)
                count_pm = PmData.objects.filter(name=j['name']).count()
                timestamp = j['time']
                # print(timestamp)
                data_datetime = datetime.fromtimestamp(timestamp)
                # print(data_datetime)
                date_time = data_datetime.strftime('%Y-%m-%d ')
                # print(date_time)



                new_datas = WeatherData.objects.all().filter(name=j['name'],
                                            date_created=data_datetime).aggregate(Avg('temp'),Max('temp'),Min('temp'),
                                                                                       Avg('pm1'),Max('pm1'),Min('pm1'))
                old_datas = WeatherHistory.objects.all().filter(name=j['name'],
                                            date_created__date=date.today()).aggregate(Avg('temp'),Max('temp'),Min('temp'),
                                                                                       Avg('pm1'),Max('pm1'),Min('pm1'))

                # j['temp__avg'] = (new_datas['temp__avg'])



                print(new_datas)


                # # tem
                # avg_temp = WeatherHistory.objects.filter(name=j['name'],
                #                                          date_created__date=date.today()).aggregate(Avg('temp'))
                #
                # avg_temp_new = WeatherData.objects.filter(name=j['name'],
                #                                           date_created__date=date.today()).aggregate(Avg('temp'))
                #
                # j['temp__avg'] = ((avg_temp_new['temp__avg'] * count_weather) + avg_temp['temp__avg']) / (
                #             count_weather + 1)  # calculate avg
                # max_temp_new = WeatherData.objects.filter(name=j['name'],
                #                                           date_created__date=date.today()).aggregate(Max('temp'))
                # max_temp = WeatherHistory.objects.filter(name=j['name'],
                #                                          date_created__date=date.today()).aggregate(Max('temp'))
                # if max_temp_new['temp__max'] >= max_temp['temp__max']:
                #     max_temp['temp__max'] = max_temp_new['temp__max']
                # j['temp__max'] = max_temp['temp__max']
                # min_temp_new = WeatherData.objects.filter(name=j['name'],
                #                                           date_created__date=date.today()).aggregate(Min('temp'))
                # min_temp = WeatherHistory.objects.filter(name=j['name'],
                #                                          date_created__date=date.today()).aggregate(Min('temp'))
                # if min_temp_new['temp__min'] <= min_temp['temp__min']:
                #     min_temp['temp__min'] = min_temp_new['temp__min']
                # j['temp__min'] = min_temp['temp__min']

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
            # obj.save()
        except:
            # print(i)
            # obj = WeatherHistory.objects.create(
            #     name=i['name'],
            #     temp=i['temp'],
            #     temp_avg=i['temp__avg'], temp_max=i['temp__max'], temp_min=i['temp__min'],
            #     pressure=i['pressure'],
            #     pressure_avg=i['pressure__avg'], pressure_max=i['pressure__max'], pressure_min=i['pressure__min'],
            #     humidity=i['humidity'],
            #     humidity_avg=i['humidity__avg'], humidity_max=i['humidity__max'], humidity_min=i['humidity__min'],
            # )
            # # print(obj)
            # for j in i:
            #     setattr(obj, j, i[j])
                # print(j)
                # print(i[j])
            # obj.save()
            # print(i)
            pass
