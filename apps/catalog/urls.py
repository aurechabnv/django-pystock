from django.urls import path

from apps.catalog.views import CatalogView, CatalogCreateView, CatalogUpdateView, CatalogDeleteView

app_name = 'product'
urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='list'),
    path('catalog/add/', CatalogCreateView.as_view(), name='add'),
    path('catalog/<int:pk>/edit/', CatalogUpdateView.as_view(), name='edit'),
    path('catalog/<int:pk>/delete/', CatalogDeleteView.as_view(), name='delete'),
]
