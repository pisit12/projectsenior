import csv
import re
import sqlite3
from datetime import datetime, date
import datetime as dt
from itertools import chain

import matplotlib as mpl
import pandas as pd
import statsmodels.api as sm
from django.db.models import Avg
from fbprophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns

import pytz
import requests
from django.shortcuts import render
from fbprophet.plot import plot_plotly, plot_components_plotly
from pandas import DataFrame
from pydash import join, chunk
from rest_framework import viewsets
from sklearn.metrics import r2_score


from django.http import HttpResponse
from weather.models import ReportStation, ListNameStation, PmData, WeatherData, WeatherHistory
from weather.serializers import ReportStationSerializer, WeatherDataSerializer, WeatherHistorySerializer, \
    ListNameStationSerializer


from sqlalchemy import create_engine


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
        # queryset = ListNameStation.objects.all()
        # serializer_class = ListNameStationSerializer
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
            apikey = "155078.nzsdK4hEn2R2n13o"
            # 149072.5M4NG9sB5ZNWSCx
            # 155078.nzsdK4hEn2R2n13o
            format = "json"
            PARAMS = {'name': name, 'what': what, 'apikey': apikey, 'format': format}
            api_request = requests.get(url=URL, params=PARAMS)
            # print("call api 1")
            # api_request.raise_for_status()
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
            apikey = "155078.nzsdK4hEn2R2n13o"
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

    def export(self):
        try:
            df = pd.read_csv('./weather/weather_history.csv')
            print(df)
            with open('./weather/weather_history.csv', 'a') as f:
                writer = csv.writer(f)
                # writer.writerow(['id', 'name','temp','date_time',])

                for data in WeatherData.objects.all().values_list('id', 'name','temp', 'pressure'
                        , 'humidity','pm1','pm2_5','pm10','date_time', ):

                    timezone = pytz.timezone("Asia/Bangkok")
                    try:
                        edit_datedata = data[3].astimezone(timezone)
                        local_data = edit_datedata.strftime('%Y-%m-%d')
                        tuple_data = (data[0],data[1],data[2],data[3],data[4],data[5]
                                      ,data[6],data[7],local_data)
                    except:
                        pass
                    writer.writerow(tuple_data)
        except:
            with open('./weather/weather_history.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'name','temp', 'pressure'
                        , 'humidity','pm1','pm2_5','pm10','date_time', ])
                for data in WeatherData.objects.all().values_list('id', 'name','temp', 'pressure'
                        , 'humidity','pm1','pm2_5','pm10','date_time', ):
                    timezone = pytz.timezone("Asia/Bangkok")
                    try:
                        edit_datedata = data[8].astimezone(timezone)
                        local_data = edit_datedata.strftime('%Y-%m-%d')
                        tuple_data = (data[0],data[1],data[2],data[3],data[4],data[5]
                                      ,data[6],data[7],local_data)
                    except:
                        pass
                    writer.writerow(tuple_data)
    # โหมมด 'a'เขียน row เพิ่ม
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

    def add_data_history(self):
        data_df = pd.read_csv('./weather/weather_history.csv')
        # print(data_df)
        data_df = data_df.reset_index()
        # df=data_df[['id','name','temp','date_time']].groupby(['name','date_time']).agg({'temp':['mean','max','min']})
        d_f= data_df[['id','name','temp','pressure','humidity','pm1','pm2_5','pm10','date_time']].groupby(['name','date_time']).agg({'temp':['mean','max','min'],
                                                                                          'pressure':['mean','max','min'],
                                                                                          'humidity':['mean','max','min'],
                                                                                          'pm1':['mean','max','min'],
                                                                                          'pm2_5':['mean','max','min'],
                                                                                          'pm10':['mean','max','min'],})
        # print(d_f)
        dict_all={}
        list_data=[]
        for row in d_f.iterrows():
            dict_data={}
            dict_data['name'],dict_data['temp_avg'],dict_data['temp_max'],dict_data['temp_min'],dict_data['date_time']=row[0][0],row[1][0],row[1][1],row[1][2],row[0][1]
            dict_data['pressure_avg'], dict_data['pressure_max'], dict_data['pressure_min']=row[1][3],row[1][4],row[1][5]
            dict_data['humidity'], dict_data['humidity_max'], dict_data['humidity_min']=row[1][6],row[1][7],row[1][8]
            dict_data['pm1'], dict_data['pm1_max'], dict_data['pm1_min']=row[1][9],row[1][10],row[1][11]
            dict_data['pm2_5_avg'], dict_data['pm2_5_max'], dict_data['pm2_5_min']=row[1][12],row[1][13],row[1][14]
            dict_data['pm10_avg'], dict_data['pm10_max'], dict_data['pm10_min']=row[1][15],row[1][16],row[1][17]
            date_time_str = dict_data['date_time']
            date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d')
            dict_data['date_time'] = date_time_obj
            dict_all.update(dict_data)
            dict_all_copy = dict_all.copy()
            list_data.append(dict_all_copy)
        # for i in list_data:
        #     print(type(i['date_time']))
        for data in list_data:
            # print(data)
            obj, is_created = WeatherHistory.objects.update_or_create(name=data["name"],date_time=data['date_time'])

            for j in data:
                setattr(obj, j, data[j])
            obj.save()

        with open('./weather/weather_forecast.csv', 'w') as f:

            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'temp_avg', 'temp_max', 'temp_min','date_time',])

            for data in WeatherHistory.objects.all().values_list('id', 'name',
                                                'temp_avg', 'temp_max', 'temp_min','date_time', ):
                timezone = pytz.timezone("Asia/Bangkok")
                try:
                    edit_datedata = data[5].astimezone(timezone)
                    local_data = edit_datedata.strftime('%Y-%m-%d')
                    tuple_data = (data[0],data[1],data[2],data[3],data[4],local_data)
                except:
                    pass
                writer.writerow(tuple_data)

    def forecast(df):
        pd.plotting.register_matplotlib_converters()
        mpl.rcParams['figure.figsize'] = (20, 10)
        sns.set()
        # df = pd.read_csv('./weather/weather_forecast.csv',
        #                  parse_dates=True, usecols=['date_time', 'temp_avg', 'name'])
        #
        # df.head()
        # print(type(data[0][0]))
        # convert = int(data[0][0])
        # print(type(convert))
        # dt_object = datetime.timestamp(convert)
        #
        # print("dt_object =", dt_object)
        # print("type(dt_object) =", type(dt_object))

        # date = datetime(year=int(datas[0:4]), month=int(datas[4:6]), day=int(datas[6:8]))
        # # dt_object = datetime.datetime.datetime.fromtimestamp(date)
        # s = date.strftime("%Y%m%d")
        # print(s)
        # print(date)

        # df = DataFrame(data,columns=['timestamp','temp'])
        # t_avg = df['temp']
        # df["TAVG"] = df.apply(t_avg, axis=1)
        # df = df[["TAVG"]]
        # df = df.dropna()
        # df.head()
        # train_df = df.reset_index()
        # train_df = train_df.rename(columns={"timestamp": "ds", "TAVG": "y"})
        #
        # model = Prophet(weekly_seasonality=True,
        #                 daily_seasonality=True)
        # model.fit(train_df)
        #
        # test_df = df.rename(columns={"timestamp": "ds", "temp": "y"})
        # test_pred = model.predict(test_df)
        #
        # model_score = r2_score(test_df["y"], test_pred["yhat"])
        # print(model_score)
        #
        # future_df = model.make_future_dataframe(periods=1)  # +1 year of data!
        # prediction = model.predict(future_df)
        # model.plot_components(prediction)
        # print(prediction)
        #
        #
        #
        # ax6 = prediction.plot(x="ds", y="yhat")
        # ax6.set_xlim(pd.Timestamp("2020-01-01"), pd.Timestamp("2021-03-31"))
        # ax6.set_xlabel("Date (YYYY-MM)")
        # ax6.set_ylabel("Temperature (C)")
        # ax6.set_title("Temperature Predictions for 2020-2021")



        # scorce_test = r2_score(train_df["y"], fcst["yhat"])
        # print(scorce_test)

        # df['cap'] = 40
        # df['floor'] = 0
        # df = df.rename(columns={'date_time': 'ds', 'temp': 'y'})
        # print(df)
        # m = Prophet(daily_seasonality=True) #model
        # m.fit(df)
        # future = m.make_future_dataframe(periods=2)
        # future['cap'] = 50
        # future['floor'] = 0
        # future.tail(5)
        # fcst = m.predict(future)
        # m.plot(fcst)
        # print(fcst)




        # future = m.make_future_dataframe(periods=2)

        # names=[]
        #
        # for data in df['name']:
        #     # print(name)
        #     names.append(df[(df['name'] == data)])
        # # print(a)
        # a=df.values.tolist()
        # list_forecast=[]
        # dict_forecast={}
        # for data_tolist in a:
        #     dict_forecast['name'] = data_tolist[0]
        #     dict_forecast_copy=dict_forecast.copy()
        #     list_forecast.append(dict_forecast_copy)
        # # print(list_forecast)
        # data_forecast=[]
        # # print(df['date_time'])
        # # for item, data in df['DateTime'].iteritems():
        # #     # data.reset_index()
        # #     # data.head()
        # #     df['date_time'] = pd.to_datetime(df['date_time'])
        # #     # if data['date_time'] == datetime.today().date():
        # #     print(data['date_time'])
        # #     # df['DateTime'] = pd.to_datetime(df['DateTime'])
        # # print(names)


        # for train_df in names:
        #     # datas = datas.rename(columns={'date_time': 'ds', 'temp_avg': 'y'})
        #     # print(datas)
        #     # m = Prophet(daily_seasonality=True)  # model
        #     # m.fit(datas)
        #     # future = m.make_future_dataframe(periods=2)
        #     # future['cap'] = 50
        #     # future['floor'] = -50
        #     # future.tail(5)
        #     # fcst = m.predict(future)
        #     # m.plot(fcst)
        #     # print(fcst)
        #     # เพิ่มfieldเข้าไป
        #     train_df = train_df.reset_index()
        #     train_df = train_df.rename(columns={"date_time": "ds", "temp_avg": "y"})
        #     model = Prophet()
        #     model.fit(train_df)
        #     test_df = train_df.rename(columns={"date_time": "ds", "temp_avg": "y"})
        #     test_pred = model.predict(test_df)
        #
        #     model_score = r2_score(test_df["y"], test_pred["yhat"])
        #     print(model_score)



            # print(data.ds)
            # print(data)
            # m = Prophet(daily_seasonality=True) #model
            # m.fit(data)
            # print(m)
            # future = m.make_future_dataframe(periods=2)
            # future['cap'] = 50
            # future['floor'] = 0
            # future.tail(5)
            # fcst = m.predict(future)
            #
            # print(fcst)

        # for data in names:
        #     print(data)
            # print(data['name'])
        # print(data_forecast[0])
        # for i in a:
            # print(i['name'])
            # for j in i['date_time']:
            #     print(type(j))


    def call_schedu(self):
        self.save_listname()
        self.save_reportstation()
        self.save_pm()
        self.save_weatherdata()
        # self.history()
        self.export()
        self.add_data_history()
        # self.forecast()
