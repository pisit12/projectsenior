# #
# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from rest_framework.reverse import reverse
# #
# #
# # @api_view(['GET'])
# # def api_root(request, format="json"):
# #     return Response({
# #         'users': reverse('user-list', request=request, format=format),
# #         'snippets': reverse('snippet-list', request=request, format=format)
# #     })
#
# from django.shortcuts import render
# from weather.models import ReportStation
# import requests
#
# def get_reportstation(request):
#     all_stations = {}
#     if request.user in request.GET:
#         name = request.GET['name']
#         URL = 'https://api.aprs.fi/api/get?'
#         what = "loc"
#         apikey = "149072.z1vz5VxaYwb5VkAm"
#         format = "json"
#         PARAMS = {'name': name, 'what': what, 'apikey': apikey, 'format': format}
#         response = requests.get(url=URL, params=PARAMS)
#         data = response.json()
#         stations_datas = data['entries']
#
#         for i in stations_datas:
#             obj, is_created = ReportStation.objects.update_or_create(name=i["name"])
#             for j in i:
#                 setattr(obj, j, i[j])
#
#                 print(j)
#             obj.save()
#             all_stations = ReportStation.objects.all().order_by('-id')
#
#     return render(request,'weather/reportstation',{"all_stations":all_stations})
#
#     #
#     # queryset_list_name = ListNameStation.objects.all()
#     #
#     # station_names = queryset_list_name.values_list('name_stations')
#     #
#     # list_names = list(station_names)
#     # str_names = ""
#     # for j in list_names:
#     #     str_names += join(j, ",") + ","
#     # names = str_names.split(",")
#     # chunked_names = chunk(names, 20)
#     # name_pm = []
#     # chunked_pm = []
#     #
#     # for j in chunked_names:
#     #     name = join(j, ",")
#     #     what = "loc"
#     #     apikey = "149072.z1vz5VxaYwb5VkAm"
#     #     format = "json"
#     #     PARAMS = {'name': name, 'what': what, 'apikey': apikey, 'format': format}
#     #     r = requests.get(url=URL, params=PARAMS)
#     #     data = r.json()
#     #
#     #     # a = data['entries']
#     #     for i in data['entries']:
#     #         obj, is_created = ReportStation.objects.update_or_create(name=i["name"])
#     #         for j in i:
#     #             setattr(obj, j, i[j])
#     #         obj.save()
