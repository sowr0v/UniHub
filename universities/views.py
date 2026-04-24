from django.shortcuts import render
from .models import University

def home(request):
    universities = University.objects.all()
    context = {
        'universities': universities
    }
    return render(request, 'home.html', context)
