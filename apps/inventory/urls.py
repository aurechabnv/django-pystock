from django.urls import path

from apps.inventory.views import InventoryView, inventory_create_view, inventory_update_view, \
    inventory_delete_view, MovementsView

app_name = 'stock'
urlpatterns = [
    path('inventory/', InventoryView.as_view(), name='list'),
    path('inventory/add/', inventory_create_view, name='add'),
    path('inventory/<int:pk>/edit/', inventory_update_view, name='edit'),
    path('inventory/<int:pk>/delete/', inventory_delete_view, name='delete'),
    path('movements/', MovementsView.as_view(), name='movements'),
]
