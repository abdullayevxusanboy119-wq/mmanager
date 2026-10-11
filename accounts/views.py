from datetime import date
from django.db.models import Sum

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from sales.models import Sale
from credits.models import Credit
from products.models import Product


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()

        today_sales_qs = Sale.objects.filter(date__date=today)
        today_profit = today_sales_qs.aggregate(total=Sum('profit'))['total'] or 0
        today_sales_count = today_sales_qs.count()

        for credit in Credit.objects.all():
            old_status = credit.status
            credit.refresh_status()
            if credit.status != old_status:
                credit.save()

        total_debt = Credit.objects.aggregate(total=Sum('remaining'))['total'] or 0
        overdue_count = Credit.objects.filter(status='overdue').count()

        low_stock_count = sum(
            1 for p in Product.objects.filter(archived=False) if p.qty <= p.min_qty
        )

        return Response({
            'today_profit': today_profit,
            'today_sales_count': today_sales_count,
            'total_sales_count': Sale.objects.count(),
            'total_debt': total_debt,
            'overdue_credits_count': overdue_count,
            'low_stock_count': low_stock_count,
        })