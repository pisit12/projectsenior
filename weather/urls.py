from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from weather.views_reportstation import ReportStationViewSet
from weather.views_weatherdata import WeatherDataViewSet
from weather.views_weatherhistory import WeatherHistoryViewSet

router = routers.DefaultRouter()
router.register('reportstation', ReportStationViewSet)
router.register('weatherdata', WeatherDataViewSet)
router.register('weatherhistory', WeatherHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]