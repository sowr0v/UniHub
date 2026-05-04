from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path(
        'university/<int:uni_id>/departments/',
        views.university_departments,
        name='university_departments',
    ),
    path('university/<int:uni_id>/', views.university_detail, name='university_detail'),
    path('events/', views.events_list, name='events'),
    path('scholarships/', views.scholarships_list, name='scholarships_list'),
    path('faq/', views.faq_page, name='faq'),
]
