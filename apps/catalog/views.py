from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.catalog.models import Product


class CatalogView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 5
    ordering = ['-created']


class CatalogCreateView(CreateView):
    model = Product
    context_object_name = 'product'
    fields = '__all__'
    success_url = reverse_lazy('product:list')


class CatalogUpdateView(UpdateView):
    model = Product
    context_object_name = 'product'
    fields = '__all__'
    success_url = reverse_lazy('product:list')


class CatalogDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('product:list')
