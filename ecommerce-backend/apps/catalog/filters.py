from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    # Allow users to find products between two prices
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    
    # Filter by category name instead of just ID
    category_name = filters.CharFilter(field_name="category__name", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'category_name']
