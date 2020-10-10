# Generated by Django 2.2.4 on 2020-10-10 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_reportstation_lng'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportstation',
            name='type',
            field=models.CharField(choices=[('AIS', 'a'), ('APRS station', 'l'), ('APRS item', 'i'), ('APRS object', 'o'), ('weather station', 'w')], default='', max_length=1),
        ),
    ]
