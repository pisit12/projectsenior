from django.shortcuts import render
from rest_framework import viewsets, mixins
# Create your views here.
from rest_framework.viewsets import GenericViewSet

from weather.models import ReportStation, WeatherData
from weather.serializers import ReportStationSerializer, WeatherDataSerializer


class ReportStationViewSet(mixins.ListModelMixin,
                   GenericViewSet):
    queryset = ReportStation.objects.all()
    serializer_class = ReportStationSerializer
    # def get_queryset(self):
    #     user = self.request.user
    #     # return ReportStation.objects.all()
