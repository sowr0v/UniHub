from django.urls import path
from . import views

app_name = 'admission'

urlpatterns = [
    path('countdown/', views.admission_countdown_list, name='countdown_list'),
]
