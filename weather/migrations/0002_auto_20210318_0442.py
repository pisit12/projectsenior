# Generated by Django 2.2.4 on 2021-03-17 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastWeather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60)),
                ('temp', models.FloatField(default=0.0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PmData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60)),
                ('pm1', models.FloatField(default=0.0)),
                ('pm2_5', models.FloatField(default=0.0)),
                ('pm10', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AlterModelOptions(
            name='reportstation',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='weatherhistory',
            options={'ordering': ['-date_time']},
        ),
        migrations.RenameField(
            model_name='listnamestation',
            old_name='name_stations',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='weatherdata',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='weatherhistory',
            name='history_id',
        ),
        migrations.AddField(
            model_name='reportstation',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='weatherdata',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='weatherdata',
            name='pm1',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherdata',
            name='pm10',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherdata',
            name='pm2_5',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='weatherhistory',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
