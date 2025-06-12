from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from apps.inventory.forms import MovementForm, StockForm
from apps.inventory.models import Stock, Movement


class InventoryView(LoginRequiredMixin, ListView):
    model = Stock
    context_object_name = "stocks"
    paginate_by = 5
    ordering = ['-created']

    def get_queryset(self):
        # TODO: update filters
        queryset = super().get_queryset()

        # query = self.request.GET.get("q")
        # if query:
        #     query_by_sku = Stock.objects.filter(sku__icontains=query)
        #     query_by_name = Stock.objects.filter(name__icontains=query)
        #     queryset = query_by_sku.union(query_by_name).order_by("-created")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["filters"] = {
        #     "q": self.request.GET.get("q", "")
        # }
        return context


class InventoryCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    form_class = StockForm
    success_url = reverse_lazy('stock:list')


@login_required(login_url='account:login')
def inventory_update(request, pk):
    stock = Stock.objects.get(pk=pk)
    defaults = {
        "type": Movement.MovementType.INBOUND,
        "quantity": 0,
        "product": stock.product.id,
        "to_location": stock.location.id,
    }

    if request.method == "POST":
        form = MovementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock:list')
    else:
        form = MovementForm(initial=defaults)

    return render(request, 'inventory/movement_form.html', {
        'initial_location': stock.location.id,
        'form': form,
    })


class InventoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Stock
    success_url = reverse_lazy('stock:list')
