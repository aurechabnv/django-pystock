from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView


User = get_user_model()


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    paginate_by = 10
    ordering = ['-date_joined']
    queryset = User.objects.prefetch_related("companies").all()

    def test_func(self):
        return self.request.user.is_staff


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    fields = ("username", "email", "is_staff", "companies",)
    success_url = reverse_lazy("management:user:list")

    def test_func(self):
        return self.request.user.is_staff


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ("username", "email", "is_staff", "is_active", "companies",)
    success_url = reverse_lazy("management:user:list")

    def test_func(self):
        return self.request.user.is_staff


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy("management:user:list")

    def test_func(self):
        return self.request.user.is_staff
