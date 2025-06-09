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
    #TODO: add some basic filtering


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
