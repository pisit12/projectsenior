from wsgiref import headers

from django.core.management import BaseCommand
from django.core.serializers import json
from django.shortcuts import render
from rest_framework import viewsets, mixins, request, status, generics, response
# Create your views here.
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from weather.models import ReportStation , ListNameStation
from weather.serializers import ReportStationSerializer
from pydash import chunk, join, url
import requests
import re


class ReportStationViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):

    # permission_classes = (IsAuthenticated,)

    queryset = ReportStation.objects.all()
    serializer_class = ReportStationSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name','id']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
