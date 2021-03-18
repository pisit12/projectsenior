import csv
import re
from datetime import datetime, date

from itertools import chain

import pandas as pd
from django.db.models import Avg
from fbprophet import Prophet
import matplotlib.pyplot as plt

import pytz
import requests
from django.shortcuts import render
from fbprophet.plot import plot_plotly, plot_components_plotly
from pydash import join, chunk
from rest_framework import viewsets

from django.http import HttpResponse
from weather.models import ReportStation, ListNameStation, PmData, WeatherData, WeatherHistory
from weather.serializers import ReportStationSerializer, WeatherDataSerializer, WeatherHistorySerializer, \
    ListNameStationSerializer


class WeatherViewset(viewsets.ModelViewSet):
    serializer_class = ListNameStationSerializer
    # serializer_class = ReportStationSerializer
    # serializer_class = WeatherDataSerializer
    search_fields = ['name']

    def get_queryset(self):
        data_report = ReportStation.objects.all()
        data_weather = WeatherData.objects.all()
        # print(data)
        list_data = list(chain(data_report, data_weather))
        return list_data

    def save_listname(self):
        queryset = ListNameStation.objects.all()
        serializer_class = ListNameStationSerializer
        station_names = "HS9AN-10,HS9AS-10,HS9AT-10,HS8AK-10,HS8AT-10,E23JWE-1,HS8KF-10,HS8INB-1,E29RZQ,HS8KAY,E29AE-8,E29WWT-2,HS8AC-10,HS7AJ-10,HS7AP-10,HS2KYA-5,HS2KYA-1,HS2AB-10,HS2UJE-10,HS2QJJ-14,HS2AR-10,E21TMW-3,E27EHM-3,E22ERY-2,E27HCD-1,E24OWX-2,E27HUQ-3,E23GYM-1,HS0QKD-2,HS2XQB-3,E24CI-1,HS0QKD-3,HS5SQI-1,HS2GJW-1,E21HVV-1,HS2PQV-1,FW6985,FW1926,EW4214,HS1FVL-10,HS1AN-10,E25ECY-1,HS1IFU-13,HS7AT-11,HS7AM-10,E20EHQ-13,HS1HTW-2,HS5GDX-1,HS3PIK-2,FW0368,E27ASY-4,HS1AL-10,APRSTH,HS3RXX-2,HS0QKD-4,E21DII-4,HS4RBS-2,HS3PKX-1,HS3NOQ-12,HS3NOQ-2,HS3PQJ-2,HS3PQJ-1,HS3PQJ-3,HS3LIQ-2,HS5GDX-2,HS3ICB-2,HS0ZGD-1,E23HMS-1,HS3LSE-11,HS3RVL-3,HS3AK-10,HS3MXC-2,HS3AU-10,HS3LSE-5,HS1MHE-1,HS4RAY-1,E24QND-1,E24QFF-1,HS4AP-10,E25HA-1,HS4LWD-1,HS4AC-10,HS4YYZ-1,E24TVS-2,E24TVS-1,E27AH-1,HS4ROI-1,HS4POQ-10,HS6NYW-3,HS6AB-10,E24OWX-1,E24YPM-1,HS6TUX,HS5XSZ-1,HS8JHY-1,HS5AM-10,HS5FXK-2,HS5ZEZ-1,HS5FXK,E28UY-13,DW2642,E22ZMG-1,HS5AC-10,HS5WFI-13"

        names = station_names.split(",")
        chunked_names = chunk(names, 1)
        for j in chunked_names:
            name = join(j, ",")
            obj, is_created = ListNameStation.objects.get_or_create(name=name)
            obj.save()

    def save_reportstation(self):
        list_name = ListNameStation.objects.all()
        list_names = list(list_name.values_list('name'))
        # print("list_names")
        str_names = ""
        for j in list_names:
            str_names += join(j, ",") + ","
        names = str_names.split(",")
        chunked_names = chunk(names, 20)
        URL = "https://api.aprs.fi/api/get?"

        for j in chunked_names:
            name = join(j, ",")
            what = "loc"
            apikey = "149072.5M4NG9sB5ZNWSCx"
            # 149072.5M4NG9sB5ZNWSCx
            # 155078.nzsdK4hEn2R2n13o
            format = "json"
            PARAMS = {'name':  name, 'what': what, 'apikey': apikey, 'format': format}
            api_request = requests.get(url=URL, params=PARAMS)
            # print("call api 1")
            api_request.raise_for_status()
            data_weathers = api_request.json()
            aprs_datas = data_weathers['entries']
            for i in aprs_datas:
                date_data = {}
                timestamp = i['lasttime']
                date_time = datetime.fromtimestamp(int(timestamp))
                timezone = pytz.timezone("Asia/Bangkok")
                i['date_time'] = date_time.astimezone(timezone)
                date_data.update(i)
                i.update(date_data)
                obj, is_created = ReportStation.objects.update_or_create(name=i["name"])
                for j in i:
                    setattr(obj, j, i[j])
                obj.save()

    def save_pm(self):
        queryset_station = ReportStation.objects.all()
        list_pm = list(queryset_station.values('name', 'comment'))
        pm_total = []
        pmdata = []
        for i in list_pm:
            # print(i['comment'])
            name_pm = i['comment'].split("PM")
            # print(name_pm)
            try:
                # print(name_pm[1])
                num_pm = re.findall(r'(?<=\[)(.*?)(?=\])', name_pm[1])  # x
                # print(num_pm)
                list_key = ['pm1', 'pm2_5', 'pm10']  # j
                output = {}
                output.update(i)
                for j, x in enumerate(num_pm):
                    # print(x)
                    output[list_key[j]] = x
                    # print(output)
                pmdata.append(output)
                # print(pmdata)
            except:
                pass

        for i in pmdata:
            try:
                obj, is_created = PmData.objects.update_or_create(
                    name=i['name'], pm1=i['pm1'],
                    pm2_5=i['pm2_5'], pm10=i['pm10'])
                for j in i:
                    setattr(obj, j, i[j])
                    # print(i[j])
                obj.save()
            except:
                # print(i)
                pass

    def save_weatherdata(self):
        queryset_pm = PmData.objects.all()
        queryset_names = ListNameStation.objects.all()

        list_names = list(queryset_names.values_list('name'))
        list_pm = list(queryset_pm.values('name', 'pm1', 'pm2_5', 'pm10'))

        str_names = ""
        for j in list_names:
            str_names += join(j, ",") + ","
        names = str_names.split(",")
        chunked_names = chunk(names, 20)
        URL = "https://api.aprs.fi/api/get?"
        for j in chunked_names:
            name = join(j, ",")
            what = "wx"
            apikey = "149072.5M4NG9sB5ZNWSCx"
            format = "json"
            PARAMS = {'name': name, 'what': what, 'apikey': apikey, 'format': format}
            response = requests.get(url=URL, params=PARAMS)

            response.raise_for_status()
            datas_weather = response.json()
            aprs_datas = datas_weather['entries']
            for i in aprs_datas:
                for pm in list_pm:
                    if pm['name'] == i['name']:
                        i.update(pm)
                    pass
                date_data = {}
                timestamp = i['time']
                date_time = datetime.fromtimestamp(int(timestamp))
                timezone = pytz.timezone("Asia/Bangkok")
                i['date_time'] = date_time.astimezone(timezone)
                date_data.update(i)
                i.update(date_data)
                obj, is_created = WeatherData.objects.update_or_create(name=i["name"])

                for j in i:
                    setattr(obj, j, i[j])
                obj.save()

    def history(self):
        queryset = WeatherHistory.objects.all()
        queryset_datas = WeatherData.objects.all()
        list_history = list(queryset.values_list('name', 'temp', 'temp_avg', 'temp_max', 'temp_min', 'date_time', ))
        list_datas = list(queryset_datas.values_list('name', 'temp', 'date_time'))
        dict_all = {}
        list_all = []
        # print(list_datas[0][2].date())
        # print(datetime.today().date())
        if list_history == []:
            try:
                for j in list_datas:
                    turple={}
                    turple['name']=j[0]
                    turple['temp']=j[1]
                    turple['temp_avg'] = j[1]
                    turple['temp_max'] = j[1]
                    turple['temp_min'] = j[1]
                    timezone = pytz.timezone("Asia/Bangkok")
                    turple['date_time'] = j[2].astimezone(timezone)
                    dict_all.update(turple)
                    # print(dict_all)
                    dict_all_copy = dict_all.copy()
                    list_all.append(dict_all_copy)
            except:
                    pass
        else:
            for j in list_datas:

                # dict_all.update(j)
                # dict_all_copy = dict_all.copy()
                # list_all.append(dict_all_copy)
                u = WeatherHistory.objects.filter(name=j[0],date_time=j[2])
                print(u)
                # if WeatherHistory.objects.filter(date_time=j[2])
                # print(WeatherHistory.objects.filter(name=j[0],date_time=j[2]))
            try:
                pass
            except:
                pass
        # for j in list_datas:
        #     if list_history == []:
        #         try:
        #             turple={}
        #             turple['name']=j[0]
        #             turple['temp']=j[1]
        #             turple['temp_avg'] = j[1]
        #             turple['temp_max'] = j[1]
        #             turple['temp_min'] = j[1]
        #             timezone = pytz.timezone("Asia/Bangkok")
        #             turple['date_time'] = j[2].astimezone(timezone)
        #             dict_all.update(turple)
        #             # print(dict_all)
        #             dict_all_copy = dict_all.copy()
        #             list_all.append(dict_all_copy)
        #         except:
        #             pass
        #     else:
        #         turple={}
        #         turple['name']=j[0]
        #         turple['temp']=j[1]
        #         timezone = pytz.timezone("Asia/Bangkok")
        #         turple['date_time'] = j[2].astimezone(timezone)
        #
        #         for i in list_history:
        #             try:
        #                 count = 0
        #                 if i[0] == j[0]:
        #                     count += 1
        #                     turple['temp_avg'] = (i[2] * count + j[1]) / (count + 1)
        #                     if i[3] <= j[1]:
        #                         turple['temp_max'] = j[1]
        #                     if i[3] > j[1]:
        #                         turple['temp_max'] = i[3]
        #                     if i[4] >= j[1]:
        #                         turple['temp_min'] = j[1]
        #                     if i[4] < j[1]:
        #                         turple['temp_min'] = i[4]
        #                     dict_all.update(turple)
        #                     dict_all_copy = dict_all.copy()
        #                     list_all.append(dict_all_copy)
        #             except:
        #                 pass
        #
        # for i in list_all:
        #     try:
        #         obj = WeatherHistory.objects.create(name=i['name'])
        #         for j in i:
        #             setattr(obj, j, i[j])
        #         obj.save()
        #         pass
        #     except:
        #         pass

    def export(self):
        try:
            df = pd.read_csv('./weather/weather_history2.csv')
        except:
            pass
        print(df)
        # with open('./weather/weather_history.csv', 'w') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(['id', 'name','temp', 'temp_avg', 'temp_max', 'temp_min','date_time',])
        #
        #     for data in WeatherHistory.objects.all().values_list('id', 'name','temp', 'temp_avg',
        #                                                       'temp_max', 'temp_min','date_time', ):
        #         timezone = pytz.timezone("Asia/Bangkok")
        #         try:
        #             edit_datedata = data[6].astimezone(timezone)
        #             local_data = edit_datedata.strftime('%m/%d/%Y %H:%M:%S')
        #             tuple_data = (data[0],data[1],data[2],data[3],data[4],data[5],local_data)
        #         except:
        #             pass
        #         writer.writerow(tuple_data)

    def forecast(self):
        plt.rcParams['figure.figsize'] = (20, 10)
        plt.style.use('ggplot')

        pd.plotting.register_matplotlib_converters()
        temp_df = pd.read_csv('./weather/weather_history.csv',
                              index_col='date_time', parse_dates=True)
        temp_df.head()

        df = temp_df.reset_index()
        # print(df)
        df['cap'] = 40
        df['floor'] = 0
        df = df.rename(columns={'date_time': 'ds', 'temp': 'y'})

        # ax = plt.gca()
        # df.set_index('ds').y.plot().figure
        # plt.show()
        m = Prophet(daily_seasonality=True)
        m.fit(df)
        future = m.make_future_dataframe(periods=2)
        future['cap'] = 50
        future['floor'] = 0
        future.tail(5)
        fcst = m.predict(future)
        m.plot(fcst)
        # len(fcst.yhat[:])
        print(fcst)
        # print(len(fcst.yhat[:]))
        # fcst.yhat[0] แล้ววนลูปถึง  data in len(fcst.yhat[:]
        # fig2 = m.plot_components(fcst)
        # fig1.show()

        # plot_plotly(m,fcst)
        plot_components_plotly(m,fcst).show()



    def call_schedu(self):
        self.save_listname()
        self.save_reportstation()
        self.save_pm()
        self.save_weatherdata()
        self.history()
        self.export()
        self.forecast()
