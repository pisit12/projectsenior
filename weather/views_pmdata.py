import re


from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from weather.models import PmData , ReportStation
from weather.serializers import PmDataSerializer


class PmDataViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):

    queryset = PmData.objects.all()

    serializer_class = PmDataSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name','id']
    # search_fields = ['id']

    queryset_station = ReportStation.objects.all()
    # list_pm = list(ReportStation.objects.values('name','comment'))
    # print(list_pm)

    def list(self, request,queryset_station=queryset_station, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        list_pm = list(queryset_station.values('name','comment'))
        # print(list_pm)
        pm_total = []
        # data = {}
        pmdata = []
        # # list_only_pm=list(ReportStation.objects.values('comment'))
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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

####################
    # pm_total = []
    # # data = {}
    # pmdata = []
    # # list_only_pm=list(ReportStation.objects.values('comment'))
    # for i in list_pm:
    #     name_pm = i['comment'].split("PM")
    #     # print(name_pm)
    #     try:
    #         # print(name_pm[1])
    #         num_pm = re.findall(r'(?<=\[)(.*?)(?=\])', name_pm[1]) # x
    #         # print(num_pm)
    #         list_key = ['pm1', 'pm2_5', 'pm10'] # j
    #         output = {}
    #         output.update(i)
    #         for j,x in enumerate(num_pm):
    #             # print(x)
    #             output[list_key[j]] = x
    #         # print(output)
    #         pmdata.append(output)
    #         # print(pmdata)
    #     except:
    #         pass
    #
    # for i in pmdata:
    #     try:
    #         obj, is_created = PmData.objects.update_or_create(
    #             name=i['name'],pm1=i['pm1'],
    #             pm2_5=i['pm2_5'],pm10=i['pm10'])
    #         for j in i:
    #             setattr(obj,j,i[j])
    #             # print(i[j])
    #             obj.save()
    #     except:
    #         # print(i)
    #         pass
##########################################