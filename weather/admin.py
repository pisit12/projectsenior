from django.contrib import admin

# Register your models here.
from .models import ReportStation, WeatherData, ListNameStation, WeatherHistory


@admin.register(ListNameStation)
class ListNameStationAdmin(admin.ModelAdmin):
    list_display = ('name_stations' ,)

@admin.register(ReportStation)
class ReportStationAdmin(admin.ModelAdmin):
    list_display = ('name' , 'lasttime')

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('name' , 'time')


@admin.register(WeatherHistory)
class WeatherHistoryAdmin(admin.ModelAdmin):
    list_display = ('name' , 'temp')