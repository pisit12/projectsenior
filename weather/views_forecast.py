import pandas as pd
import numpy as np
from fbprophet import Prophet
import matplotlib.pyplot as plt
from rest_framework import viewsets, mixins, status
# Create your views here.
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from weather.models import ReportStation, ForecastWeather
from weather.serializers import ForecastSerializer
import os.path


class ForecastViewset(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = ForecastWeather.objects.all()
    serializer_class = ForecastSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        plt.rcParams['figure.figsize'] = (20, 10)
        plt.style.use('ggplot')

        pd.plotting.register_matplotlib_converters()
        temp_df = pd.read_csv('./weather/weather_history.csv',
                              index_col='date_time', parse_dates=True)
        temp_df.head()
        # print(temp_df)
        # temp_df.describe(include='0')
        # X = temp_df['date_time','temp','temp_avg','temp_max','temp_min']
        # y = temp_df.iloc[:,3]
        # train_dataset = pd.DataFrame()
        # train_dataset['ds'] = pd.to_datetime(X["date_time"])
        # train_dataset['y'] = y
        # train_dataset.head(2)
        # prophet_basic = Prophet()
        # prophet_basic.fit(train_dataset)
        # future = prophet_basic.make_future_dataframe(periods=5)
        # future.tail(5)
        # forecast = prophet_basic.predict(future)
        # print(forecast)
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
        print(fcst)
        # fig2 = m.plot_components(fcst)
        # fig1.show()

        # plot_plotly(m,fcst)
        # plot_components_plotly(m,fcst).show()

        page = self.paginate_queryset(queryset)
        # print(page)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            # print(page)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # plt.rcParams['figure.figsize'] = (20, 10)
    # plt.style.use('ggplot')

    # pd.plotting.register_matplotlib_converters()

    # sales_df = pd.read_csv('./retail_sales.csv',
    #                         index_col='date', parse_dates=True)
    # sales_df.head()

    # df = sales_df.reset_index()
    # df.head()

    # df = df.rename(columns={'date': 'ds', 'sales': 'y'})
    # df.head()

    # df.set_index('ds').y.plot().figure
    # plt.show()
