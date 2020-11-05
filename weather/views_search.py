# from rest_framework import filters, generics
# from rest_framework.filters import SearchFilter
#
# from weather.models import WeatherData
# from weather.serializers import WeatherDataSerializer
#
# from rest_framework import viewsets, mixins
#
# # class StationListView(generics.ListAPIView):
# #     queryset = ReportStation.objects.all()
# #     serializer_class = ReportStationSerializer
# #     filter_backends = [filters.SearchFilter]
# #     search_fields = ['name']
#
# class SearchViewSet(mixins.ListModelMixin,
#                            viewsets.GenericViewSet):
#     queryset = WeatherData.objects.all()
#     serializer_class = WeatherDataSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['name']
#
#     # def get_search_fields(self, view, request):
#     #     if request.query_params.get('name_only'):
#     #         return ['name']
#     #     return super(SearchViewSet, self).get_search_fields(view, request)
#
# # class StationSearchFilter(filter.SearchFilter):
# #     def get_search_fields(self, view, request):
# #         if request.query_params.get('name_only'):
# #             return ['name']
# #         return super(StationSearchFilter, self).get_search_fields(view, request)