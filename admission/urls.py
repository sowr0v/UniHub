from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'admission'

urlpatterns = [
    path('', views.admissions_hub, name='admissions_hub'),
    path(
        'countdown/',
        RedirectView.as_view(
            pattern_name='admission:admissions_hub',
            permanent=True,
        ),
        name='countdown_list',
    ),
]
