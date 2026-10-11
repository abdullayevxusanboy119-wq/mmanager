from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend (index.html)
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # JWT auth
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App API routes
    path('api/', include('accounts.urls')),
    path('api/', include('products.urls')),
    path('api/', include('customers.urls')),
    path('api/', include('suppliers.urls')),
    path('api/', include('sales.urls')),
    path('api/', include('credits.urls')),
    path('api/', include('repairs.urls')),
]