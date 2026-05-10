from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_or_update_playground_service, name='add_playground_service'),
    path('manage/', views.manage_playground_services, name='manage_playground_services'),
]
