from django.shortcuts import render, redirect, get_object_or_404
from .forms import BusServiceForm
from .models import BusService
from universities.models import University
from django.contrib import messages

def add_bus_service(request):
    if request.method == 'POST':
        form = BusServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bus service status added/updated successfully!')
            return redirect('manage_bus_services')
    else:
        form = BusServiceForm()
    return render(request, 'add_bus_service.html', {'form': form})

def manage_bus_services(request):
    bus_services = BusService.objects.select_related('university').all()
    return render(request, 'manage_bus_services.html', {'bus_services': bus_services})
