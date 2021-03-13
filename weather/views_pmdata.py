import re


from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from weather.models import PmData, ReportStation
from weather.serializers import PmDataSerializer


class PmDataViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    queryset = PmData.objects.all()

    serializer_class = PmDataSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'id']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)