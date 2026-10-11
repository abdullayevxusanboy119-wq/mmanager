from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Sale
from .serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    """
    Sotuvlar hech qachon PATCH/PUT orqali tahrirlanmaydi (moliyaviy yozuv sifatida).
    Faqat list, create, retrieve, destroy ruxsat etiladi.
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['customer_name']
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        qs = Sale.objects.all()
        sale_type = self.request.query_params.get('type')
        if sale_type:
            qs = qs.filter(type=sale_type)
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            qs = qs.filter(date__date__gte=date_from)
        if date_to:
            qs = qs.filter(date__date__lte=date_to)
        return qs