from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from universities.models import University
from .forms import UniversityForm

def is_staff_user(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_user)
def dashboard(request):
    """Custom admin dashboard"""
    universities = University.objects.all()
    context = {
        'universities': universities,
        'total_universities': universities.count(),
    }
    return render(request, 'dashboard.html', context)

@login_required
@user_passes_test(is_staff_user)
def add_university(request):
    """Add new university using ModelForm"""
    if request.method == 'POST':
        form = UniversityForm(request.POST, request.FILES)
        if form.is_valid():
            university = form.save()
            messages.success(request, f'University "{university.name}" added successfully!')
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UniversityForm()
    
    context = {'form': form}
    return render(request, 'add_university.html', context)

@login_required
@user_passes_test(is_staff_user)
def edit_university(request, pk):
    """Edit existing university using ModelForm"""
    university = get_object_or_404(University, pk=pk)
    
    if request.method == 'POST':
        form = UniversityForm(request.POST, request.FILES, instance=university)
        if form.is_valid():
            university = form.save()
            messages.success(request, f'University "{university.name}" updated successfully!')
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UniversityForm(instance=university)
    
    context = {
        'form': form,
        'university': university
    }
    return render(request, 'edit_university.html', context)

@login_required
@user_passes_test(is_staff_user)
def delete_university(request, pk):
    """Delete university"""
    university = get_object_or_404(University, pk=pk)
    
    if request.method == 'POST':
        name = university.name
        university.delete()
        messages.success(request, f'University "{name}" deleted successfully!')
        return redirect('custom_admin:dashboard')
    
    context = {'university': university}
    return render(request, 'delete_university.html', context)
