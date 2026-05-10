from django.shortcuts import render, redirect
from .forms import PlaygroundServiceForm
from .models import PlaygroundService
from django.contrib import messages

def add_or_update_playground_service(request):
    if request.method == 'POST':
        form = PlaygroundServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Playground service status added/updated successfully!')
            return redirect('manage_playground_services')
    else:
        form = PlaygroundServiceForm()
    return render(request, 'add_playground_service.html', {'form': form})

def manage_playground_services(request):
    playground_services = PlaygroundService.objects.select_related('university').all()
    return render(request, 'manage_playground_services.html', {'playground_services': playground_services})
