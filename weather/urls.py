from django.contrib import admin
from django.urls import include, path
from .views import ReportStationViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('reportstation', ReportStationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]