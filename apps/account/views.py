from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import FormView

from apps.account.forms import RegisterForm, ProfileForm


User = get_user_model()


class RegisterView(FormView):
    template_name = "account/register.html"
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = "/"

    def form_valid(self, form):
        user: User = form.save()
        if user:
            login(self.request, user)

        return super(RegisterView, self).form_valid(form)


@login_required(login_url="account:login")
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour.")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "account/profile.html", {"form": form})
