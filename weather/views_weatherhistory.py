from rest_framework import viewsets, mixins
from rest_framework.response import Response

from weather.models import WeatherHistory
from weather.models import WeatherData
from django.db.models import Avg, Max, Min

class WeatherHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = WeatherHistory.objects.all()
    # serializer_class.aggregate(Avg('temp'))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
