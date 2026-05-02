from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from universities.models import University
from .forms import UniversityForm
from django.contrib.auth.models import User
from django.db.models import Q
import csv
import io

def is_staff_user(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_user)
def dashboard(request):
    """Custom admin dashboard"""
    universities = University.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        universities = universities.filter(
            Q(name__icontains=search_query) |
            Q(short_name__icontains=search_query)
        )
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


@login_required
@user_passes_test(is_staff_user)
def upload_universities_csv(request):
    """Bulk upload universities from a CSV file"""
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file:
            messages.error(request, "Please select a file to upload.")
            return redirect('custom_admin:upload_csv')
            
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "This is not a valid CSV file.")
            return redirect('custom_admin:upload_csv')
            
        try:
            # Read and decode the file
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            
            # Skip the header row
            next(io_string)
            
            count = 0
            for row in csv.reader(io_string, delimiter=',', quotechar='"'):
                # Expected columns: Name, Address, Contact, Total Departments, Faculty, QS Ranking, Publications, Cost, Admission Requirements, Website, Short Name, Credit System
                if len(row) < 3:
                    continue # Skip empty or invalid rows
                    
                University.objects.create(
                    name=row[0].strip(),
                    address=row[1].strip() if len(row) > 1 else "",
                    contact=row[2].strip() if len(row) > 2 else "",
                    total_departments=int(row[3].strip() or 0) if len(row) > 3 else 0,
                    faculty=int(row[4].strip() or 0) if len(row) > 4 else 0,
                    qs_ranking=int(row[5].strip()) if len(row) > 5 and row[5].strip() else None,
                    publications=int(row[6].strip() or 0) if len(row) > 6 else 0,
                    cost=row[7].strip() or "0.00" if len(row) > 7 else "0.00",
                    admission_requirements=row[8].strip() if len(row) > 8 else "",
                    website=row[9].strip() if len(row) > 9 else "",
                    short_name=row[10].strip() if len(row) > 10 else "",
                    credit_system=row[11].strip() if len(row) > 11 else None,
                )
                count += 1
                
            messages.success(request, f"Successfully imported {count} universities.")
            return redirect('custom_admin:dashboard')
            
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
            return redirect('custom_admin:upload_csv')
            
    return render(request, 'upload_csv.html')