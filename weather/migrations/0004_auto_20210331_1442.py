# Generated by Django 2.2.4 on 2021-03-31 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_auto_20210329_0438'),
    ]

    operations = [
        migrations.AddField(
            model_name='weatherhistory',
            name='humidity_avg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='humidity_max',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='humidity_min',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pm10_avg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pm10_max',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pm10_min',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pm1_avg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pm1_max',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pm1_min',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pm2_5_avg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pm2_5_max',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pm2_5_min',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pressure_avg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pressure_max',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='pressure_min',
            field=models.FloatField(default=0.0),
        ),
    ]
