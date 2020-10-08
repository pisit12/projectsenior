from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from weather.models import ReportStation


class ReportStationViewSet(viewsets.ModelViewSet):
    queryset = ReportStation.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     # return ReportStation.objects.all()
