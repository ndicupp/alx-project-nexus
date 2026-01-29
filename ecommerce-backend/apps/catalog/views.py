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
