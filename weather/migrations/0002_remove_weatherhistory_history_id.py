# Generated by Django 2.2.4 on 2020-11-05 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weatherhistory',
            name='history_id',
        ),
    ]
