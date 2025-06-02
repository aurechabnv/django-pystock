from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from apps.account.views import RegisterView

app_name = 'account'
urlpatterns = [
    path('login/', LoginView.as_view(template_name="account/login.html", next_page="home"), name="login"),
    path('logout/', LogoutView.as_view(next_page="account:login"), name="logout"),
    path('register', RegisterView.as_view(), name="register"),
    path('password-reset', PasswordResetView.as_view(template_name="account/password_reset.html"),
         name="password_reset"),
    path('password-reset/done', PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"),
         name="password_reset_complete"),
]
