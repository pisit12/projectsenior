import csv

from django.http import HttpResponse

from weather.models import ReportStation
from django.shortcuts import render


def export(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    print(writer)
    writer.writerow(['name', 'type', 'time', 'lasttime', 'lat', 'lng', 'comment'])
    # print(writer.writerow(['name', 'type', 'time', 'lasttime', 'lat', 'lng', 'comment']))
    for report in ReportStation.objects.all().values_list('name', 'type', 'time', 'lasttime', 'lat', 'lng', 'comment'):
        writer.writerow(report)
        # print(writer.writerow(report))

    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    print("csv")
    return response