from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

from apps.catalog.models import Product
from apps.inventory.forms import MovementForm, StockForm
from apps.inventory.models import Stock, Movement, Location


class InventoryView(ListView):
    model = Stock
    context_object_name = "stocks"
    paginate_by = 10

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

        return queryset.order_by("-last_modified")

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


class InventoryCreateView(View):
    form_class = StockForm
    template_name = "inventory/stock_form.html"

    def get(self, request):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("stock:list")

        return render(request, self.template_name, {"form": form})


class InventoryUpdateView(UserPassesTestMixin, View):
    form_class = MovementForm
    template_name = "inventory/movement_form.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock = None

    def test_func(self):
        """
        User must have access to the location's company to access stock.
        This check prevents access to unauthorized items from direct url.
        """
        self.stock = Stock.objects.select_related("location").get(pk=self.kwargs["pk"])
        return self.request.user.is_staff or self.stock.location.company in self.request.user.companies.all()

    def get_initial(self):
        return {
            "type": Movement.MovementType.INBOUND,
            "quantity": 0,
            "product": self.stock.product.id,
            "to_location": self.stock.location.id,
        }

    def get_context_data(self, form):
        return {
            'initial_location': self.stock.location.id,
            'stock_id': self.stock.id,
            'form': form,
        }

    def get(self, request, pk):
        form = self.form_class(initial=self.get_initial(), user=request.user)
        return render(request, self.template_name, self.get_context_data(form))

    def post(self, request, pk):
        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('stock:list')

        return render(request, self.template_name, self.get_context_data(form))


class InventoryDeleteView(UserPassesTestMixin, DeleteView):
    model = Stock
    success_url = reverse_lazy("stock:list")

    def test_func(self):
        """
        User must have access to the location's company to access stock.
        This check prevents access to unauthorized items from direct url.
        """
        stock = Stock.objects.select_related("location").get(pk=self.kwargs["pk"])
        return self.request.user.is_staff or stock.location.company in self.request.user.companies.all()


class MovementsView(ListView):
    model = Movement
    context_object_name = "movements"
    paginate_by = 10

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

        return queryset.order_by("-date")

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
