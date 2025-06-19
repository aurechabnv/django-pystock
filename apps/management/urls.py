from django.urls import path

from apps.management.views.companies import CompanyListView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView
from apps.management.views.locations import LocationListView, LocationCreateView, LocationUpdateView, LocationDeleteView
from apps.management.views.users import UserListView, UserCreateView, UserUpdateView, UserDeleteView

app_name = "management"

urlpatterns = [
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('companies/add/', CompanyCreateView.as_view(), name='company-add'),
    path('companies/<int:pk>/edit/', CompanyUpdateView.as_view(), name='company-edit'),
    path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company-delete'),

    path('locations/', LocationListView.as_view(), name='location-list'),
    path('locations/add/', LocationCreateView.as_view(), name='location-add'),
    path('locations/<int:pk>/edit/', LocationUpdateView.as_view(), name='location-edit'),
    path('locations/<int:pk>/delete/', LocationDeleteView.as_view(), name='location-delete'),

    path('users/', UserListView.as_view(), name='user-list'),
    path('users/add/', UserCreateView.as_view(), name='user-add'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user-edit'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]
