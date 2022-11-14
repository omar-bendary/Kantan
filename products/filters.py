
from django_filters.rest_framework import FilterSet
import django_filters
from .models import Product


class ProductFilter(FilterSet):

    type = django_filters.CharFilter(method='type_custom_filter')
    length = django_filters.CharFilter(method='length_custom_filter')
    width = django_filters.CharFilter(method='width_custom_filter')
    height = django_filters.CharFilter(method='height_custom_filter')
    material = django_filters.CharFilter(method='material_custom_filter')

    class Meta:
        model = Product
        fields = {
            'material': ['exact'],
            'details__price': ['gt', 'lt'],

        }

    def type_custom_filter(self, queryset,  name, value):
        params = self.request.query_params.get('type')
        params_list = params.split(',')

        print(params_list)
        return queryset.filter(details__type__in=params_list)

    def length_custom_filter(self, queryset,  name, value):
        params = self.request.query_params.get('length')
        params_list = params.split(',')

        return queryset.filter(details__size__length__in=params_list)

    def width_custom_filter(self, queryset,  name, value):
        params = self.request.query_params.get('width')
        params_list = params.split(',')

        return queryset.filter(details__size__width__in=params_list)

    def height_custom_filter(self, queryset,  name, value):
        params = self.request.query_params.get('height')
        params_list = params.split(',')

        return queryset.filter(details__size__height__in=params_list)

    def material_custom_filter(self, queryset,  name, value):
        params = self.request.query_params.get('material')
        params_list = params.split(',')

        return queryset.filter(material__in=params_list)
