from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_not_required
from django.shortcuts import render, redirect

from apps.account.forms import RegisterForm, ProfileForm


User = get_user_model()


@login_not_required
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user: User = form.save()
        if user:
            login(request, user)
            return redirect("home")

    return render(request, "account/register.html", {"form": form})


def profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Votre profil a été mis à jour.")

    return render(request, "account/profile.html", {"form": form})
