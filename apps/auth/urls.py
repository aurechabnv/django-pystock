from django.urls import path

from apps.auth import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset-pwd/', views.reset_password_view, name='reset_password'),
]
