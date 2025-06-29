import calendar
from datetime import datetime, timedelta

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.utils.translation import gettext
from django.views import View
from django.views.generic import TemplateView

from apps.catalog.models import Product, Category
from apps.inventory.models import Movement


class DashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'reporting/dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        product_count = Product.objects.count()
        product_low_count = Product.objects.filter(stock__is_low=True).count()
        return {
            "product_count": product_count,
            "product_low_count": product_low_count
        }


class ApiCategoriesView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        data = Category.objects.values("name", nb_of_items=Count('products')).order_by('name')
        return JsonResponse({
            "labels": [obj["name"] for obj in data],
            "data": [obj["nb_of_items"] for obj in data],
        }, safe=False)


class ApiStockPerMonthView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        # Filter movements based on date
        today = datetime.now()
        six_months_prior = today - timedelta(days=30*6)
        movements = Movement.objects.filter(date__gt=six_months_prior)

        # Get data sets for each movement type
        inbound = movements.filter(type=Movement.MovementType.INBOUND).values("date__month").annotate(nb_of_stocks=Sum("quantity"))
        outbound = movements.filter(type=Movement.MovementType.OUTBOUND).values("date__month").annotate(nb_of_stocks=Sum("quantity"))
        transfer = movements.filter(type=Movement.MovementType.TRANSFER).values("date__month").annotate(nb_of_stocks=Sum("quantity"))

        # Convert the data sets to dict to ease parsing
        inbound_dict = {obj["date__month"]: obj["nb_of_stocks"] for obj in inbound}
        outbound_dict = {obj["date__month"]: obj["nb_of_stocks"] for obj in outbound}
        transfer_dict = {obj["date__month"]: obj["nb_of_stocks"] for obj in transfer}

        # Take out the labels, distinct and sorted
        labels = sorted(list(set(list(inbound_dict.keys()) + list(outbound_dict.keys()) + list(transfer_dict.keys()))))

        # Prepare the data lists and default empty values to zero
        data1, data2, data3 = [], [], []
        for label in labels:
            if label in inbound_dict.keys():
                data1.append(inbound_dict[label])
            else:
                data1.append(0)

            if label in outbound_dict.keys():
                # set outbound values to negative for the bar chart
                data2.append(-abs(outbound_dict[label]))
            else:
                data2.append(0)

            if label in transfer_dict.keys():
                data3.append(transfer_dict[label])
            else:
                data3.append(0)

        # Get the months' translated labels
        labels = [gettext(calendar.month_name[month_number]).capitalize() for month_number in labels]

        return JsonResponse({
            "labels": list(labels),
            "in": data1,
            "out": data2,
            "tr": data3,
        }, safe=False)
