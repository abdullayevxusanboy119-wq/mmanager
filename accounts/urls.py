from django.urls import path
from .views import CurrentUserView, DashboardView

urlpatterns = [
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]