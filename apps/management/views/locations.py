from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from apps.management.models import Location, Company


class LocationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Location
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        """
        Filter the queryset based on user company rights, and user filter input
        :return: Queryset of stocks
        """
        queryset = Location.objects.select_related("company")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(city__icontains=query) |
                Q(company__name__icontains=query)
            )

        return queryset.order_by("-created")

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


class LocationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy("management:location:list")

    def test_func(self):
        return self.request.user.is_staff


class LocationCreateFromCompanyView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy("management:location:list")

    def test_func(self):
        return self.request.user.is_staff

    def get_object(self, queryset=None):
        queryset = Company.objects.all()
        return super().get_object(queryset)

    def get_initial(self):
        company = self.get_object()
        return {'company': company}


class LocationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy("management:location:list")

    def test_func(self):
        return self.request.user.is_staff


class LocationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Location
    success_url = reverse_lazy("management:location:list")

    def test_func(self):
        return self.request.user.is_staff
