from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from universities.models import University
from .forms import UniversityForm
from django.contrib.auth.models import User


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


@login_required
@user_passes_test(is_staff_user)
def manage_users(request):
    """View to list all non-admin users"""
    # Grab all users where is_staff is False
    students = User.objects.filter(is_staff=False).order_by('-date_joined')

    context = {
        'students': students,
        'total_students': students.count()
    }
    return render(request, 'manage_users.html', context)


@login_required
@user_passes_test(is_staff_user)
def delete_student(request, user_id):
    """Securely deletes a student account"""
    if request.method == 'POST':
        # Ensure we only delete non-staff users
        student = get_object_or_404(User, id=user_id, is_staff=False)
        username = student.username
        student.delete()
        messages.success(request, f"Student '{username}' has been permanently removed.")

    return redirect('custom_admin:manage_users')