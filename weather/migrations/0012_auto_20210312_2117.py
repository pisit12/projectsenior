# Generated by Django 2.2.4 on 2021-03-12 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0011_reportstation_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weatherhistory',
            name='humidity',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='humidity_avg',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='humidity_max',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='humidity_min',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm1',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm10',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm10_avg',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm10_max',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm10_min',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm1_avg',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm1_max',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm1_min',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm2_5',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm2_5_avg',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm2_5_max',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pm2_5_min',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pressure',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pressure_avg',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pressure_max',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='pressure_min',
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]