from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from apps.management.models import Company, Location

User = get_user_model()


class CompanyListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Company

    def test_func(self):
        return self.request.user.is_staff


class LocationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Location
    paginate_by = 10
    ordering = ('name',)

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        """
        Filter the queryset based on user company rights, and user filter input
        :return: Queryset of stocks
        """
        queryset = super().get_queryset()

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(city__icontains=query) |
                Q(company__name__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add query fields back into the context
        :return: Updated context data
        """
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            "q": self.request.GET.get("q", ""),
        }
        return context


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User

    def test_func(self):
        return self.request.user.is_staff


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    fields = "__all__"
    success_url = reverse_lazy("management:company-list")

class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    fields = "__all__"
    success_url = reverse_lazy("management:company-list")

class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    success_url = reverse_lazy("management:company-list")


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy("management:location-list")

class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy("management:location-list")

class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    success_url = reverse_lazy("management:location-list")


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = "__all__"
    success_url = reverse_lazy("management:user-list")

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = "__all__"
    success_url = reverse_lazy("management:user-list")

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("management:user-list")
