from django.urls import path

from apps.reporting.views import dashboard, api_categories, api_stock_per_month

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('api/json/categories/', api_categories, name='api_categories'),
    path('api/json/stock-per-month/', api_stock_per_month, name='api_stock_evolution'),
]
