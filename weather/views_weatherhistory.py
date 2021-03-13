from requests import Response
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from weather.models import WeatherHistory
from weather.models import WeatherData

from weather.serializers import WeatherHistorySerializer

class WeatherHistoryViewSet(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'id']
    serializer_class = WeatherHistorySerializer

    queryset = WeatherHistory.objects.all()
    queryset_datas = WeatherData.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
