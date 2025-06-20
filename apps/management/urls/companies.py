from django.urls import path

from apps.management.views.companies import CompanyListView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView

app_name = 'company'

urlpatterns = [
    path('', CompanyListView.as_view(), name='list'),
    path('add/', CompanyCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', CompanyUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', CompanyDeleteView.as_view(), name='delete'),
]