from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import Form
from django.shortcuts import render, redirect
from django.views.generic import ListView

from apps.catalog.models import Product
from apps.inventory.forms import MovementForm, StockForm
from apps.inventory.models import Stock, Movement, Location


class InventoryView(LoginRequiredMixin, ListView):
    model = Stock
    context_object_name = "stocks"
    paginate_by = 10
    ordering = ['-last_modified']

    def get_queryset(self):
        """
        Filter the queryset based on user company rights, and user filter input
        :return: Queryset of stocks
        """
        queryset = Stock.objects.select_related("product", "location", "location__company")

        # Make sure normal user has company access
        if not self.request.user.is_staff:
            queryset = queryset.filter(location__company__in=self.request.user.companies.all())

        low_stock = self.request.GET.get("low_stock") == "on"
        if low_stock:
            queryset = queryset.filter(is_low=low_stock)

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(product__sku__icontains=query) |
                Q(product__name__icontains=query) |
                Q(location__name__icontains=query) |
                Q(location__company__name__icontains=query)
            )

        return queryset.all()

    def get_context_data(self, **kwargs):
        """
        Add query fields back into the context
        :return: Updated context data
        """
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            "q": self.request.GET.get("q", ""),
            "low_stock": self.request.GET.get("low_stock", ""),
        }
        return context


@login_required()
def inventory_create_view(request):
    if request.method == "POST":
        form = StockForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('stock:list')
    else:
        form = StockForm(user=request.user)

    return render(request, 'inventory/stock_form.html', { 'form': form })


@login_required()
def inventory_update_view(request, pk):
    stock = Stock.objects.get(pk=pk)
    defaults = {
        "type": Movement.MovementType.INBOUND,
        "quantity": 0,
        "product": stock.product.id,
        "to_location": stock.location.id,
    }

    # user must have access to the location's company to access stock
    # this check prevents access to unauthorized items from direct url
    if not request.user.is_staff and stock.location.company not in request.user.companies.all():
        messages.error(request, "Vous n'avez pas accès à ce stock")
        return redirect("stock:list")

    if request.method == "POST":
        form = MovementForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('stock:list')
    else:
        form = MovementForm(initial=defaults, user=request.user)

    return render(request, 'inventory/movement_form.html', {
        'initial_location': stock.location.id,
        'stock_id': stock.id,
        'form': form,
    })


@login_required()
def inventory_delete_view(request, pk):
    stock = Stock.objects.get(pk=pk)

    # user must have access to the location's company to access stock
    # this check prevents access to unauthorized items from direct url
    if not request.user.is_staff and stock.location.company not in request.user.companies.all():
        messages.error(request, "Vous n'avez pas accès à ce stock")
        return redirect("stock:list")

    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            stock.delete()
            messages.success(request, "Stock supprimé")
            return redirect('stock:list')

    return render(request, 'inventory/stock_confirm_delete.html', { 'object': stock })


class MovementsView(LoginRequiredMixin, ListView):
    model = Movement
    context_object_name = "movements"
    paginate_by = 10
    ordering = ['-date']

    def get_queryset(self):
        """
        Filter the queryset based on user company rights, and user filter input
        :return: Queryset of movements
        """
        queryset = Movement.objects.select_related("product", "to_location", "from_location")

        # Make sure normal user has company access
        if not self.request.user.is_staff:
            user_companies = self.request.user.companies.all()
            queryset = queryset.filter(
                Q(to_location__company__in=user_companies) |
                Q(from_location__company__in=user_companies)
            )

        product = self.request.GET.get("p")
        location = self.request.GET.get("l")
        if product and location:
            queryset = queryset.filter(
                Q(product__id=product, to_location__id=location) |
                Q(product__id=product, from_location__id=location)
            )

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(product__name__icontains=query) |
                Q(to_location__name__icontains=query) |
                Q(from_location__name__icontains=query)
            )

        return queryset.all()

    def get_context_data(self, **kwargs):
        """
        Add query fields back into the context
        :return: Updated context data
        """
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            "q": self.request.GET.get("q", ""),
        }

        product_id = self.request.GET.get("p")
        location_id = self.request.GET.get("l")
        if product_id and location_id:
            product = Product.objects.get(id=product_id)
            location = Location.objects.get(id=location_id)
            context["filters"]["product"] = str(product)
            context["filters"]["location"] = str(location)

        return context
