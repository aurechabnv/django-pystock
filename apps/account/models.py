from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.management.models import Company


class User(AbstractUser):
    companies = models.ManyToManyField(Company, verbose_name="Entreprises", help_text="Entreprises auxquelles l'utilisateur a accès", related_name="users")
