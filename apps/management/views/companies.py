from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from apps.management.models import Company


class CompanyListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Company
    queryset = Company.objects.prefetch_related("users", "locations").all()

    def test_func(self):
        return self.request.user.is_staff


class CompanyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Company
    fields = "__all__"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        if "create_and_add_site" in self.request.POST:
            return reverse_lazy("management:location:add-from-company", args=(self.object.pk,))
        else:
            return reverse_lazy("management:company:list")


class CompanyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Company
    fields = "__all__"
    success_url = reverse_lazy("management:company:list")

    def test_func(self):
        return self.request.user.is_staff


class CompanyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Company
    success_url = reverse_lazy("management:company:list")

    def test_func(self):
        return self.request.user.is_staff
