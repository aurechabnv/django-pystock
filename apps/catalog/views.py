from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.catalog.forms import ProductForm
from apps.catalog.models import Product


class CatalogView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 5
    ordering = ['-created']

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get("q")
        if query:
            query_by_sku = Product.objects.filter(sku__icontains=query)
            query_by_name = Product.objects.filter(name__icontains=query)
            queryset = query_by_sku.union(query_by_name).order_by("-created")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            "q": self.request.GET.get("q", "")
        }
        return context


class CatalogCreateView(LoginRequiredMixin, CreateView):
    model = Product
    context_object_name = 'product'
    form_class = ProductForm
    success_url = reverse_lazy('product:list')


class CatalogUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    context_object_name = 'product'
    form_class = ProductForm
    success_url = reverse_lazy('product:list')


class CatalogDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('product:list')
