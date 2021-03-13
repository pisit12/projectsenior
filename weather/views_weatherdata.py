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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)