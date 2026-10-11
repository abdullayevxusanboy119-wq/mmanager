from rest_framework import viewsets, filters
from .models import Customer
from .serializers import CustomerSerializer
from accounts.permissions import IsAdminOrReadOnly


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone', 'email']