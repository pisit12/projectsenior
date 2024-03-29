import token

import self as self
from django.shortcuts import render
from rest_framework import viewsets, mixins, status
# Create your views here.
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from weather.models import ListNameStation
from weather.serializers import ListNameStationSerializer
from pydash import chunk, join
import requests


class ListNameStationViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    # permission_classes = (IsAuthenticated,) #Token e1d492289c89b9d9ee355d8478f5e1a562f8191b' 9ac769124382e80b4a7e86bca088abccb8b7e671
    # token=Token.objects.create(user=)
    # print(token.key)
    queryset = ListNameStation.objects.all()
    serializer_class = ListNameStationSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    # station_names = "HS9AN-10,HS9AS-10,HS9AT-10,HS8AK-10,"
    # station_names = "HS9AN-10,HS9AS-10,HS9AT-10,HS8AK-10,HS8AT-10,E23JWE-1,HS8KF-10,HS8INB-1,E29RZQ,HS8KAY,E29AE-8,E29WWT-2,HS8AC-10,HS7AJ-10,HS7AP-10,HS2KYA-5,HS2KYA-1,HS2AB-10,HS2UJE-10,HS2QJJ-14,HS2AR-10,E21TMW-3,E27EHM-3,E22ERY-2,E27HCD-1,E24OWX-2,E27HUQ-3,E23GYM-1,HS0QKD-2,HS2XQB-3,E24CI-1,HS0QKD-3,HS5SQI-1,HS2GJW-1,E21HVV-1,HS2PQV-1,FW6985,FW1926,EW4214,HS1FVL-10,HS1AN-10,E25ECY-1,HS1IFU-13,HS7AT-11,HS7AM-10,E20EHQ-13,HS1HTW-2,HS5GDX-1,HS3PIK-2,FW0368,E27ASY-4,HS1AL-10,APRSTH,HS3RXX-2,HS0QKD-4,E21DII-4,HS4RBS-2,HS3PKX-1,HS3NOQ-12,HS3NOQ-2,HS3PQJ-2,HS3PQJ-1,HS3PQJ-3,HS3LIQ-2,HS5GDX-2,HS3ICB-2,HS0ZGD-1,E23HMS-1,HS3LSE-11,HS3RVL-3,HS3AK-10,HS3MXC-2,HS3AU-10,HS3LSE-5,HS1MHE-1,HS4RAY-1,E24QND-1,E24QFF-1,HS4AP-10,E25HA-1,HS4LWD-1,HS4AC-10,HS4YYZ-1,E24TVS-2,E24TVS-1,E27AH-1,HS4ROI-1,HS4POQ-10,HS6NYW-3,HS6AB-10,E24OWX-1,E24YPM-1,HS6TUX,HS5XSZ-1,HS8JHY-1,HS5AM-10,HS5FXK-2,HS5ZEZ-1,HS5FXK,E28UY-13,DW2642,E22ZMG-1,HS5AC-10,HS5WFI-13"
    #
    # names = station_names.split(",")
    # chunked_names = chunk(names, 1)
    # for j in chunked_names:
    #     name = join(j, ",")
    #     obj, is_created = ListNameStation.objects.get_or_create(name=name)
    #     obj.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

