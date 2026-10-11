from rest_framework import viewsets, filters
from .models import Product
from .serializers import ProductSerializer
from accounts.permissions import IsAdminOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'model', 'imei']

    def get_queryset(self):
        qs = Product.objects.all()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        show_archived = self.request.query_params.get('archived')
        if show_archived != 'true':
            qs = qs.filter(archived=False)
        return qs

    def perform_destroy(self, instance):
        # Soft-delete: EduCRM'dagidek archived flag orqali
        instance.archived = True
        instance.save()