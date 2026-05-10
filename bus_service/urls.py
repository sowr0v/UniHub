from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_bus_service, name='add_bus_service'),
    path('manage/', views.manage_bus_services, name='manage_bus_services'),
]
