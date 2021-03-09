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

        sales_df = pd.read_csv('E:/project/new/seniorProject/weather/retail_sales.csv',
                            index_col='date', parse_dates=True)
        # sales_df = open('/retail_sales.csv')

        sales_df.head()

        df = sales_df.reset_index()
        df.head()

        df = df.rename(columns={'date': 'ds', 'sales': 'y'})
        df.head()

        df.set_index('ds').y.plot().figure
        plt.show()
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