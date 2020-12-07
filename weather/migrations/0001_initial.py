# Generated by Django 2.2.4 on 2020-11-19 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListNameStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_stations', models.CharField(default='', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='ReportStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60)),
                ('type', models.CharField(choices=[('a', 'AIS'), ('l', 'APRS station'), ('i', 'APRS item'), ('o', 'APRS object'), ('w', 'weather station')], default='', max_length=16)),
                ('time', models.IntegerField(default=0)),
                ('lasttime', models.IntegerField(default=0)),
                ('lat', models.FloatField(default=0.0)),
                ('lng', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60)),
                ('time', models.IntegerField(default=0, null=True)),
                ('temp', models.FloatField(default=0.0, null=True)),
                ('pressure', models.FloatField(default=0.0, null=True)),
                ('humidity', models.FloatField(default=0.0, null=True)),
                ('wind_direction', models.FloatField(default=0.0, null=True)),
                ('wind_speed', models.FloatField(default=0.0, null=True)),
                ('wind_gust', models.FloatField(default=0.0, null=True)),
                ('rain_1h', models.FloatField(default=0.0, null=True)),
                ('rain_24h', models.FloatField(default=0, null=True)),
                ('rain_mn', models.FloatField(default=0.0, null=True)),
                ('luminosity', models.FloatField(default=0.0, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60)),
                ('temp', models.FloatField(default=0.0, null=True)),
                ('temp_avg', models.FloatField(default=0.0)),
                ('temp_max', models.FloatField(default=0.0)),
                ('temp_min', models.FloatField(default=0.0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('history_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history', to='weather.WeatherData')),
            ],
        ),
    ]
