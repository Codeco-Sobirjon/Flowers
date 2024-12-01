from django_filters import rest_framework as filters
from apps.flowers.models import Flower


class FlowerFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = filters.BaseInFilter(field_name="category__id", lookup_expr="in")
    package = filters.CharFilter(field_name="package__name", lookup_expr="icontains")
    size = filters.CharFilter(field_name="flower_size__name", lookup_expr="icontains")
    compound = filters.CharFilter(field_name="flower_compound__name", lookup_expr="icontains")
    quantity = filters.NumberFilter(field_name="quantity")
    in_stock = filters.BooleanFilter(field_name="in_stock")
    showcase_online = filters.BooleanFilter(field_name="showcase_online")
    is_popular = filters.BooleanFilter(field_name="is_popular")
    is_new = filters.BooleanFilter(field_name="is_new")
    country = filters.CharFilter(field_name="country__name", lookup_expr="icontains")
    plantation = filters.CharFilter(field_name="plantation", lookup_expr="icontains")
    stem_height = filters.NumberFilter(field_name="stem_height")
    volume = filters.NumberFilter(field_name="volume")
    head_outer_diameter = filters.NumberFilter(field_name="head_outer_diameter")

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte", label="Minimum price")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte", label="Maximum price")

    class Meta:
        model = Flower
        fields = ['name', 'category', 'package', 'size', 'compound', 'quantity', 'in_stock',
                  'showcase_online', 'is_popular', 'is_new', 'plantation', 'stem_height', 'volume',
                  'head_outer_diameter', 'country', 'min_price', 'max_price', 'country']
