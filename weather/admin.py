from django.contrib import admin

# Register your models here.
from .models import ReportStation, WeatherData

@admin.register(ReportStation)
class ReportStationAdmin(admin.ModelAdmin):
    list_display = ('name' , 'type')

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('name' ,)