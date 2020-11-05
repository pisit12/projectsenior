from django.db import models, IntegrityError
import os.path
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.
from django.utils import timezone


class ReportStation(models.Model):
    name = models.CharField(max_length=60 ,default='')
    type_choices = [
            ('a', 'AIS'),
            ('l', 'APRS station'),
            ('i', 'APRS item'),
            ('o', 'APRS object'),
            ('w', 'weather station'),
        ]
    type = models.CharField(
            max_length=16,
            choices=type_choices,
            default='',
        )
    time= models.IntegerField(default=0)
    lasttime = models.IntegerField(default=0)
    lat = models.FloatField(default=0.00000)
    lng = models.FloatField(default=0.00000)

    def __str__(self):
        return '[weather report id:{}] {}'.format(self.id, self.name)



class WeatherData(models.Model):
    name = models.CharField(max_length=60 ,default='')
    time = models.IntegerField(default=0, null=True)
    temp = models.FloatField(default=0.00, null=True)
    pressure = models.FloatField(default=0.00, null=True)
    humidity = models.FloatField(default=0.00, null=True)
    wind_direction = models.FloatField(default=0.00, null=True)
    wind_speed = models.FloatField(default=0.00, null=True)
    wind_gust = models.FloatField(default=0.00, null=True)
    rain_1h = models.FloatField(default=0.00, null=True)
    rain_24h = models.FloatField(default=0, null=True) #,min_value=1, max_value=24
    rain_mn = models.FloatField(default=0.00, null=True)
    luminosity = models.FloatField(default=0.00, null=True)

    # created = models.DateTimeField(auto_now_add=True)
    # date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[weather data id:{}] {}'.format(self.id, self.name)

class WeatherHistory(models.Model):
    # history_id = models.ForeignKey('WeatherData', on_delete=models.CASCADE, null=True)
    temp_avg = models.FloatField(default=0.00)
    temp_max = models.FloatField(default=0.00)
    temp_min = models.FloatField(default=0.00)

