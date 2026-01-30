from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter

class ProductListView(generics.ListAPIView):
    # Optimization: select_related fetches the Category in the same SQL join
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    
    # Define which fields the user is allowed to sort by
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at'] # Default sort: Newest first
    
    # Define which fields the Search bar looks at
    search_fields = ['name', 'description']

class ProductListView(generics.ListAPIView):
    # 'select_related' for foreign keys (Category)
    # 'only' to fetch only the fields we need (reduces memory usage)
    queryset = Product.objects.filter(is_active=True).select_related('category').only(
        'name', 'price', 'slug', 'category__name'
    )
    # ... rest of the view

git add apps/catalog/models.py apps/catalog/views.py core/settings.py
git commit -m "perf(database): implement query profiling and composite indexing" -m "Added Django Debug Toolbar for profiling, implemented PostgreSQL functional indexes, and optimized QuerySets with select_related."
git push origin main

from drf_spectacular.utils import extend_schema

class ProductListView(generics.ListAPIView):
    # This tag groups the endpoint in Swagger
    @extend_schema(tags=['Products'], summary="List all active products with filters")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

