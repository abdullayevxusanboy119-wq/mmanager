from rest_framework import viewsets, filters
from .models import Supplier
from .serializers import SupplierSerializer
from accounts.permissions import IsAdminOrReadOnly


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'contact', 'phone', 'email']