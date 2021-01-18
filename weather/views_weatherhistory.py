from datetime import date
from itertools import groupby

from pydash import join
from rest_framework import viewsets, mixins
# from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from weather.models import WeatherHistory
from weather.models import WeatherData
from django.db.models import Avg, Max, Min, Count

from weather.serializers import WeatherHistorySerializer


class WeatherHistoryViewSet(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):

    #permission_classes = (IsAuthenticated,)

    queryset = WeatherHistory.objects.all()
    serializer_class = WeatherHistorySerializer

    filter_backends = [SearchFilter]
    search_fields = ['id']
    list_history = list(queryset)
    # print(list_history)

    queryset_datas = WeatherData.objects.all()
    # ควรเอาไอดีไปใช้แล้ว เอาค่าที่เหลือจะตามมา
    list_datas = list(queryset_datas.values('name', 'temp','date_created'))
       # เพิ่ม id ได้ โดยให้ his_id=id\
    # date_created__day ก็มี
    dict_temp= {}
    list_temp = []
    # print(list_datas
    for j in list_datas:
        try:
            # print(queryset.filter(date_created__date=date.today(),name=j['name']))
            # print(WeatherData.objects.filter(name=j['name']).aggregate(Avg('temp')))
            if list_history ==[]:
                avg_temp_new = WeatherData.objects.filter(name=j['name']).aggregate(Avg('temp'))
                max_temp_new = WeatherData.objects.filter(name=j['name']).aggregate(Max('temp'))
                min_temp_new = WeatherData.objects.filter(name=j['name']).aggregate(Min('temp'))
                # print(avg_temp)
                dict_temp.update(j)
                dict_temp.update(avg_temp_new)
                dict_temp.update(max_temp_new)
                dict_temp.update(min_temp_new)
                dict_temp_copy = dict_temp.copy()
                list_temp.append(dict_temp_copy)
                # print(list_temp)
            else:
                # avg
                count_tempp=WeatherHistory.objects.filter(name=j['name']).count()
                avg_temp=WeatherData.objects.filter(name=j['name'],date_created__date=date.today()).aggregate(Avg('temp'))
                avg_temp_new = WeatherData.objects.filter(name=j['name'],date_created__date=date.today()).aggregate(Avg('temp'))
                j['temp__avg']=((avg_temp_new['temp__avg']*count_tempp)+avg_temp['temp__avg'])/(count_tempp+1) # calculate avg
                # max
                max_temp_new = WeatherData.objects.filter(name=j['name'],date_created__date=date.today()).aggregate(Max('temp'))
                max_temp = WeatherHistory.objects.filter(name=j['name'],date_created__date=date.today()).aggregate(Max('temp'))
                if max_temp_new['temp__max'] >= max_temp['temp__max']:
                    max_temp['temp__max'] = max_temp_new['temp__max']
                j['temp__max'] = max_temp['temp__max']
                # min
                min_temp_new = WeatherData.objects.filter(name=j['name'],date_created__date=date.today()).aggregate(Min('temp'))
                min_temp = WeatherHistory.objects.filter(name=j['name'],date_created__date=date.today()).aggregate(Min('temp'))
                if min_temp_new['temp__min'] <= min_temp['temp__min']:
                    min_temp['temp__min'] = min_temp_new['temp__min']
                j['temp__min']=min_temp['temp__min']
                # print(j['temp__min'])
                # print("******")
                #
                # # print(j.groupby([j['date_created'].dt.date])['temp'].mean())
                # print(min_temp_new['temp__min'].filter(date_created__date=date.today()))
                #
                # print("---------------------")
                # # print(j)
                # hh = WeatherHistory.objects.filter(name=j['name'],date_created__date=date.today()).aggregate(Min('temp'))
                # print(hh)
                # print("---------------------")
                # result = WeatherHistory.objects.extra(select={'day': 'date( weatherhistory.date_created )'}).values('day').annotate(available=Count('date_created'))
                # print(result)
                # j = j.groupby([j['date_created'].dt.date])
                # # print(j)


                # print(min_temp+max_temp)

                dict_temp.update(j)

                dict_temp_copy = dict_temp.copy()
                list_temp.append(dict_temp_copy)
        except:
            # print(j)
            pass

    for i in list_temp:
        try:
            obj= WeatherHistory.objects.create(name=i["name"],
                                                            temp=i["temp"], temp_avg=i["temp__avg"],
                                                            temp_max=i["temp__max"], temp_min=i["temp__min"])
            for j in i:
                setattr(obj,j,i[j])
            obj.save()
        except:
            print(i)
            pass