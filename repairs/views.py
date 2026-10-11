from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Repair
from .serializers import RepairSerializer
from accounts.permissions import IsAdminOrReadOnly


class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['customer_name', 'phone', 'model']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def advance_status(self, request, pk=None):
        """Frontend'dagi updateRepairStatus() tugmasiga mos: received -> repairing -> ready."""
        repair = self.get_object()
        repair.advance_status()
        repair.save()
        return Response(RepairSerializer(repair).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def notify(self, request, pk=None):
        """Frontend'dagi notifyRepairReady() tugmasiga mos: mijozga SMS yuborilgan deb belgilanadi."""
        repair = self.get_object()
        repair.notified = True
        repair.save()
        return Response(RepairSerializer(repair).data, status=status.HTTP_200_OK)