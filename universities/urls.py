from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('university/<int:uni_id>/', views.university_detail, name='university_detail'),
    path('events/', views.events_list, name='events'),
    path('admissions/', views.admissions_list, name='admissions'),
]
