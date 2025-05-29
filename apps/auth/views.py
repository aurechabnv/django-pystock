from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.shortcuts import render, redirect

def login_view(request):
    context = {}

    if request.method == "POST":
        form = AuthenticationForm(None, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Vous êtes connecté.")
            return redirect("index")
    else:
        form = AuthenticationForm()

    context["form"] = form
    return render(request, "auth/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté.")
    return redirect("index")


def reset_password_view(request):
    context = {}

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        # if form.is_valid():
        #     user = form.get_user()
        #     login(request, user)
        #     messages.success(request, "Vous êtes connecté.")
        #     return redirect("index")
    else:
        form = PasswordResetForm()

    context["form"] = form
    return render(request, "auth/reset_password.html", context)
