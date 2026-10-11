from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Credit
from .serializers import CreditSerializer, CreditPaymentSerializer
from accounts.permissions import IsAdminOrReadOnly


class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['customer_name', 'phone']

    def list(self, request, *args, **kwargs):
        # ro'yxat chiqishidan oldin barcha kreditlar statusini yangilaymiz (muddati o'tganlarni belgilash uchun)
        for credit in self.get_queryset():
            old_status = credit.status
            credit.refresh_status()
            if credit.status != old_status:
                credit.save()
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def pay(self, request, pk=None):
        credit = self.get_object()
        serializer = CreditPaymentSerializer(data=request.data, context={'credit': credit})
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        credit.paid += amount
        credit.remaining -= amount
        credit.refresh_status()
        credit.save()

        return Response(CreditSerializer(credit).data, status=status.HTTP_200_OK)