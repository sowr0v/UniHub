from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_or_update_hostel_service, name='add_hostel_service'),
    path('manage/', views.manage_hostel_services, name='manage_hostel_services'),
]
