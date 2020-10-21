from django.db import models

# Create your models here.
class ReportStation(models.Model):
    name = models.CharField(max_length=60)
    type_choices = [
            ('AIS', 'a'),
            ('APRS station', 'l'),
            ('APRS item', 'i'),
            ('APRS object', 'o'),
            ('weather station', 'w'),
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
    # cover = models.ImageField(null=True, blank=True)

    def __str__(self):
        return '[weather id:{}] {}'.format(self.id, self.name)

class WeatherData(models.Model):
    name = models.CharField(max_length=60 ,default='')
    temp = models.FloatField(default=0.00)
    time = models.FloatField(default=0.00)
    pressure = models.FloatField(default=0.00)
    humidity = models.FloatField(default=0.00)
    wind_direction = models.FloatField(default=0.00)
    wind_speed = models.FloatField(default=0.00)
    wind_gust = models.FloatField(default=0.00)
    rain_1h = models.FloatField(default=0.00)
    rain_24h = models.FloatField(default=0) #,min_value=1, max_value=24
    rain_mn = models.FloatField(default=0.00)
    luminosity = models.FloatField(default=0.00)

    def __str__(self):
        return '[weather id:{}] {}'.format(self.id, self.name)
    # Model Save override to set id as filename
    # def save(self, *args, **kwargs):
    #     if self.id is None:
    #         cover = self.cover_file
    #         self.cover_file = None
    #         super(ReportStation, self).save(*args, **kwargs)
    #         self.cover_file = cover
    #         if 'force_insert' in kwargs:
    #             kwargs.pop('force_insert')
    #
    #     super(ReportStation, self).save(*args, **kwargs)

class WeatherHistory(models.Model):
    temp_avg = models.FloatField(default=0.00)
    temp_max = models.FloatField(default=0.00)
    temp_min = models.FloatField(default=0.00)

