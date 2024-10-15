from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from commons.custom_pagination import StandardResultPagination
from commons.custom_filter import ProductFilter

from .models import  Product
from .serializers import ProductSerializer




class ProductViewSet(viewsets.ModelViewSet):
    """
    This view handle the product CRUD operations
    permission is limited to the Admin User
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    pagination_class = StandardResultPagination
    search_fields = ["category__name", "name"]
    
    def get_queryset(self):
        return Product.objects.filter(is_available=True)
    
    
    
    
    
    