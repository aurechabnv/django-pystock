from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.catalog.forms import ProductForm
from apps.catalog.models import Product
from apps.inventory.models import Stock


class CatalogView(PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    permission_required = 'catalog.view_product'
    paginate_by = 8

    def get_queryset(self):
        """
        Support queryset filtering based on user input
        :return: Queryset of products
        """
        queryset = Product.objects.prefetch_related('categories')

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(sku__icontains=query) | Q(name__icontains=query)
            )

        return queryset.order_by("-last_modified")

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


class CatalogCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:list')
    permission_required = 'catalog.add_product'


class CatalogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:list')
    permission_required = 'catalog.change_product'


class CatalogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product:list')
    permission_required = 'catalog.delete_product'

    def get_object(self, queryset=None):
        obj = super().get_object()

        # add known stocks for information
        stocks = Stock.objects.filter(product=obj)
        obj.stocks = stocks

        return obj
