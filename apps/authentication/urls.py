from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from apps.authentication.views import RegisterView

urlpatterns = [
    path('login/', LoginView.as_view(template_name="authentication/login.html", next_page='home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
]
