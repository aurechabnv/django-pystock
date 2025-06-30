from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.management.models import Company


class UserRole:
    EMPLOYEE = "employee"
    MANAGER = "manager"
    EMPLOYEE_PERMS = [
        "view_product", "add_product", "change_product", "delete_product",
        "view_stock", "add_stock", "change_stock", "delete_stock",
        "view_movement"
    ]
    MANAGER_PERMS = [
        "view_company", "add_company", "change_company", "delete_company",
        "view_location", "add_location", "change_location", "delete_location",
        "view_user", "add_user", "change_user", "delete_user",
        "view_category", "add_category", "change_category", "delete_category"
    ]


class User(AbstractUser):
    companies = models.ManyToManyField(Company, blank=True, verbose_name="Entreprises", help_text="Entreprises auxquelles l'utilisateur a accès", related_name="users")
