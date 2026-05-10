from django.shortcuts import render, redirect
from .forms import HostelServiceForm
from .models import HostelService
from django.contrib import messages

def add_or_update_hostel_service(request):
    if request.method == 'POST':
        form = HostelServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hostel service status added/updated successfully!')
            return redirect('manage_hostel_services')
    else:
        form = HostelServiceForm()
    return render(request, 'add_hostel_service.html', {'form': form})

def manage_hostel_services(request):
    hostel_services = HostelService.objects.select_related('university').all()
    return render(request, 'manage_hostel_services.html', {'hostel_services': hostel_services})
