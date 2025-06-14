from django.urls import path

from apps.inventory.views import InventoryView, InventoryCreateView, InventoryDeleteView, \
    inventory_update, MovementsView

app_name = 'stock'
urlpatterns = [
    path('inventory/', InventoryView.as_view(), name='list'),
    path('inventory/add/', InventoryCreateView.as_view(), name='add'),
    path('inventory/<int:pk>/edit/', inventory_update, name='edit'),
    path('inventory/<int:pk>/delete/', InventoryDeleteView.as_view(), name='delete'),
    path('movements/', MovementsView.as_view(), name='movements'),
]
