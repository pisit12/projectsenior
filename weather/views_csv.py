# import csv
#
# from django.http import HttpResponse
#
# from weather.models import ReportStation
# from django.shortcuts import render
#
# def export():
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(content_type='text/csv')
#
#     with open('test.csv', 'w') as f:
#         writer = csv.writer(f)
#         writer.writerow(['name', 'type',])
#         for report in ReportStation.objects.all().values_list('id', 'name',
#             'temp', 'temp_avg', 'temp_max', 'temp_min',
#             'pressure', 'pressure_avg', 'pressure_max', 'pressure_min',
#             'humidity', 'humidity_avg', 'humidity_max', 'humidity_min',
#             'pm1', 'pm1_avg', 'pm1_max', 'pm1_min',
#             'pm2_5', 'pm2_5_avg', 'pm2_5_max', 'pm2_5_min',
#             'pm10', 'pm10_avg', 'pm10_max', 'pm10_min',):
#             writer.writerow(report)
#
#     response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
#     print("csv")
#     return HttpResponse(status=200)
