from django.urls import path
from location_api.views import geocode_addess

urlpatterns = [
    path(r'api/location/', geocode_addess)
]