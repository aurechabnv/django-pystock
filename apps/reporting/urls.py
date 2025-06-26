from django.urls import path

from apps.reporting.views import DashboardView, ApiCategoriesView, ApiStockPerMonthView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('json/categories/', ApiCategoriesView.as_view(), name='api_categories'),
    path('json/stock-per-month/', ApiStockPerMonthView.as_view(), name='api_stock_evolution'),
]
