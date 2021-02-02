from django.db import models, IntegrityError
import os.path
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.
from django.utils import timezone

class ListNameStation(models.Model):
    # namestation_id = models.ForeignKey('namestation_id',on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=60 ,default='')

    def __str__(self):
        return '[list name station id:{}] {}'.format(self.id, self.name)

class ReportStation(models.Model):
    # reportstation_id = models.ForeignKey('reportstation_id',on_delete=models.CASCADE, null=True)
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
    comment = models.CharField(max_length=200 ,default='')

    def __str__(self):
        return '[weather report id:{}] {}'.format(self.id, self.name)


class WeatherData(models.Model):
    # weatherdata_id = models.ForeignKey('weatherdata_id',on_delete=models.CASCADE, null=True)
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
    pm1 = models.FloatField(default=0.00000)
    pm2_5 = models.FloatField(default=0.00000)
    pm10 = models.FloatField(default=0.00000)
    date_created = models.DateTimeField(auto_now_add=True)


    # created = models.DateTimeField(auto_now_add=True)
    # date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[weather data id:{}] {}'.format(self.id, self.name)

class WeatherHistory(models.Model):
    name = models.CharField(max_length=60 ,default='')
    history_id = models.ForeignKey(WeatherData,related_name='history',on_delete=models.CASCADE, null=True)
    temp = models.FloatField(default=0.00, null=True)
    temp_avg = models.FloatField(default=0.00)
    temp_max = models.FloatField(default=0.00)
    temp_min = models.FloatField(default=0.00)
    pm1_avg = models.FloatField(default=0.00)
    pm1_max = models.FloatField(default=0.00)
    pm1_min = models.FloatField(default=0.00)
    pm1 = models.FloatField(default=0.00)
    date_created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ['history_id']

    def __str__(self):
        return '[weather history id:{}] {}'.format(self.id, self.name)

class PmData(models.Model):
    name = models.CharField(max_length=60 ,default='')
    pm1 = models.FloatField(default=0.00000)
    pm2_5 = models.FloatField(default=0.00000)
    pm10 = models.FloatField(default=0.00000)

    def __str__(self):
        return '[pm id : {}] {}'.format(self.id, self.name)