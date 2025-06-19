from django.urls import path

from apps.management.views.locations import LocationListView, LocationCreateView, LocationUpdateView, LocationDeleteView

app_name = 'location'

urlpatterns = [
    path('', LocationListView.as_view(), name='list'),
    path('add/', LocationCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', LocationUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', LocationDeleteView.as_view(), name='delete'),
]