from django.urls import path

from apps.management.views.users import UserListView, UserCreateView, UserUpdateView, UserDeleteView

app_name = 'user'

urlpatterns = [
    path('', UserListView.as_view(), name='list'),
    path('add/', UserCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
]