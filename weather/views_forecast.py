import pandas as pd
import numpy as np
import pytz
from fbprophet import Prophet
import matplotlib.pyplot as plt
from pandas import DataFrame
from rest_framework import viewsets, mixins, status
# Create your views here.
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from sklearn.metrics import r2_score

from weather.models import ReportStation, ForecastWeather
from weather.serializers import ForecastSerializer
import os.path


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from fbprophet import Prophet
import statsmodels.api as sm # Time series analysis
import datetime as dt
from datetime import datetime, date

from sklearn.metrics import r2_score


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

        page = self.paginate_queryset(queryset)
        # print(page)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            # print(page)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

