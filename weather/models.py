from django.db import models

# Create your models here.
class ReportStation(models.Model):
    name = models.CharField(max_length=60)
    location = models.IntegerField(default=0.0)
    # cover = models.ImageField(null=True, blank=True)
    temp = models.IntegerField(default=0.0)
    humid = models.IntegerField(default=0.0)
    pressure = models.IntegerField(default=0.0)
    pm2_5 = models.IntegerField(default=0.0)
    pm10 = models.IntegerField(default=0.0)
    wind = models.IntegerField(default=0.0)

    # Model Save override to set id as filename
    def save(self, *args, **kwargs):
        if self.id is None:
            cover = self.cover_file
            self.cover_file = None
            super(ReportStation, self).save(*args, **kwargs)
            self.cover_file = cover
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(ReportStation, self).save(*args, **kwargs)


    def __str__(self):
        return self.title