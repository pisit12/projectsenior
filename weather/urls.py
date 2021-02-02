from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
#
# from weather import views_reportstation

from weather.views_listname import ListNameStationViewSet
from weather.views_reportstation import ReportStationViewSet
from weather.views_weatherdata import WeatherDataViewSet
# from weather.views_weatherhistory import WeatherHistoryViewSet
from weather.views_pmdata import PmDataViewSet



router = routers.DefaultRouter()

router.register('listnamestation',ListNameStationViewSet)
router.register('reportstation', ReportStationViewSet)
router.register('weatherdata', WeatherDataViewSet)
# router.register('weatherhistory', WeatherHistoryViewSet)
router.register('pmdata', PmDataViewSet)



urlpatterns = [

    path('', include(router.urls)),
    # path('report/', views_reportstation.ReportStationAPIView.as_view(), name='reportstationapiview')
    # path('reportstation/', views_reportstation.ReportStationList.as_view()),
]