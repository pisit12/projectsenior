import re

from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from weather.models import PmData , ReportStation
from weather.serializers import PmDataSerializer


class PmDataViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):

    queryset = PmData.objects.all()

    serializer_class = PmDataSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id']

    queryset_station = ReportStation.objects.all()

    list_pm = list(ReportStation.objects.values('name','comment'))

    pm_total = []
    # data = {}
    pmdata = []

    for pm_all in list_pm:
        pm_total = re.findall(r'(?<=\[)(.*?)(?=\])', pm_all['comment'])
        list_key = ['pm1', 'pm2_5', 'pm10']
        output = {}
        output.update(pm_all)
        for i, x in enumerate(pm_total):
            output[list_key[i]] = x
        # print(output)

        pmdata.append(output)
    # print(pmdata)

    for i in pmdata:
        try:
            obj, is_created = PmData.objects.update_or_create(name=i['name'],
                                                              pm1=i['pm1'],
                                                              pm2_5=i['pm2_5'],
                                                              pm10=i['pm10'])
            for j in i:
                setattr(obj,j,i[j])
                print(i[j])
            obj.save()
        except:
            print(i)
            pass







