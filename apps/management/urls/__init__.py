from django.urls import path, include

app_name = "management"

urlpatterns = [
    path('companies/', include('apps.management.urls.companies')),
    path('locations/', include('apps.management.urls.locations')),
    path('users/', include('apps.management.urls.users')),
]
