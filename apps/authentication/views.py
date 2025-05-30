from django.contrib.auth import login
from django.views.generic import FormView

from apps.authentication.forms import RegisterForm


class RegisterView(FormView):
    template_name = "authentication/register.html"
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)

        return super(RegisterView, self).form_valid(form)
