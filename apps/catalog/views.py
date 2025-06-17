from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.catalog.forms import ProductForm
from apps.catalog.models import Product
from apps.inventory.models import Stock


class CatalogView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 8
    ordering = ['-last_modified']

    def get_queryset(self):
        """
        Support queryset filtering based on user input
        :return: Queryset of products
        """
        queryset = super().get_queryset()

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(sku__icontains=query) | Q(name__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add query fields back into the context
        :return: Updated context data
        """
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            "q": self.request.GET.get("q", "")
        }
        return context


class CatalogCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:list')


class CatalogUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:list')


class CatalogDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product:list')

    def get_object(self, queryset=None):
        obj = super().get_object()

        # add known stocks for information
        stocks = Stock.objects.filter(product=obj)
        obj.stocks = stocks

        return obj
