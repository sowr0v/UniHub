from django.shortcuts import render
from .models import AdmissionOpening
from django.utils import timezone

def admission_countdown_list(request):
    admissions = AdmissionOpening.objects.filter(is_active=True)
    current_time = timezone.now()
    
    context = {
        'admissions': admissions,
        'current_time': current_time,
    }
    return render(request, 'admission_countdown.html', context)
