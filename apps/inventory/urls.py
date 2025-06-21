from django.urls import path

from apps.inventory.views import InventoryView, InventoryCreateView, InventoryUpdateView, \
    InventoryDeleteView, MovementsView

app_name = 'stock'
urlpatterns = [
    path('inventory/', InventoryView.as_view(), name='list'),
    path('inventory/add/', InventoryCreateView.as_view(), name='add'),
    path('inventory/<int:pk>/edit/', InventoryUpdateView.as_view(), name='edit'),
    path('inventory/<int:pk>/delete/', InventoryDeleteView.as_view(), name='delete'),
    path('movements/', MovementsView.as_view(), name='movements'),
]
