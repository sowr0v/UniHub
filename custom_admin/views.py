from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from universities.models import University, Department, Event, Scholarship, FaqCategory, FaqItem
from .forms import UniversityForm
from django.contrib.auth.models import User
from django.db.models import Q, Count
import csv
import io
from admission.models import AdmissionOpening
from admission.forms import AdmissionOpeningForm
from clubs.models import Club
from clubs.forms import ClubForm
from universities.forms import (
    DepartmentForm,
    EventForm,
    ScholarshipForm,
    FaqCategoryForm,
    FaqItemForm,
)

def is_staff_user(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_user)
def dashboard(request):
    """Custom admin dashboard"""
    universities = University.objects.annotate(dept_listed_count=Count('departments')).all()
    search_query = request.GET.get('search')
    if search_query:
        universities = universities.filter(
            Q(name__icontains=search_query) |
            Q(short_name__icontains=search_query)
        )
    context = {
        'universities': universities,
        'total_universities': University.objects.count(),
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
    # Get non-staff users
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
        # Ensure user is not staff
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
            # Read and decode CSV
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            
            # Skip header
            next(io_string)
            
            count = 0
            for row in csv.reader(io_string, delimiter=',', quotechar='"'):
                # Expected: Name, Address, Contact, Total Departments, Faculty, QS Ranking, Publications, Cost, Admission Requirements, Website, Short Name, Credit System
                if len(row) < 3:
                    continue
                    
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


@login_required
@user_passes_test(is_staff_user)
def manage_admissions(request):
    admissions = AdmissionOpening.objects.all().order_by('opening_datetime')
    context = {
        'admissions': admissions,
        'total_admissions': admissions.count(),
    }
    return render(request, 'manage_admissions.html', context)

@login_required
@user_passes_test(is_staff_user)
def manage_departments(request):
    departments = Department.objects.select_related('university').all()
    context = {
        'departments': departments,
        'total_departments': departments.count(),
    }
    return render(request, 'manage_departments.html', context)


@login_required
@user_passes_test(is_staff_user)
def add_department(request):
    initial = {}
    uid = request.GET.get('university')
    if uid and str(uid).isdigit():
        if University.objects.filter(pk=int(uid)).exists():
            initial['university'] = int(uid)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            dept = form.save()
            messages.success(
                request,
                f'Department "{dept.name}" for "{dept.university.name}" added successfully!',
            )
            return redirect('custom_admin:manage_departments')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepartmentForm(initial=initial)

    context = {
        'form': form,
        'form_title': 'Add Department',
        'submit_label': 'Add Department',
    }
    return render(request, 'department_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            dept = form.save()
            messages.success(
                request,
                f'Department "{dept.name}" updated successfully!',
            )
            return redirect('custom_admin:manage_departments')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepartmentForm(instance=department)

    context = {
        'form': form,
        'form_title': 'Edit Department',
        'submit_label': 'Update Department',
    }
    return render(request, 'department_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        uni_name = department.university.name
        name = department.name
        department.delete()
        messages.success(
            request,
            f'Department "{name}" ({uni_name}) deleted successfully!',
        )
        return redirect('custom_admin:manage_departments')

    context = {'department': department}
    return render(request, 'delete_department.html', context)


@login_required
@user_passes_test(is_staff_user)
def manage_events(request):
    now = timezone.now()
    upcoming = Event.objects.filter(event_date__gte=now).select_related('university').order_by(
        'event_date'
    )
    past_events = list(
        Event.objects.filter(event_date__lt=now)
        .select_related('university')
        .order_by('-event_date')[:200]
    )
    context = {
        'upcoming_events': upcoming,
        'past_events': past_events,
        'total_upcoming': upcoming.count(),
    }
    return render(request, 'manage_events.html', context)


@login_required
@user_passes_test(is_staff_user)
def add_event(request):
    initial = {}
    uid = request.GET.get('university')
    if uid and str(uid).isdigit():
        if University.objects.filter(pk=int(uid)).exists():
            initial['university'] = int(uid)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            ev = form.save()
            messages.success(
                request,
                f'Event "{ev.title}" for "{ev.university.name}" added successfully!',
            )
            return redirect('custom_admin:manage_events')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm(initial=initial)

    context = {
        'form': form,
        'form_title': 'Add Event',
        'submit_label': 'Save event',
    }
    return render(request, 'event_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            ev = form.save()
            messages.success(
                request,
                f'Event "{ev.title}" updated successfully!',
            )
            return redirect('custom_admin:manage_events')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'form_title': 'Edit Event',
        'submit_label': 'Update event',
    }
    return render(request, 'event_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        title = event.title
        uni = event.university.name
        event.delete()
        messages.success(
            request,
            f'Event "{title}" ({uni}) deleted successfully!',
        )
        return redirect('custom_admin:manage_events')

    context = {'event': event}
    return render(request, 'delete_event.html', context)


@login_required
@user_passes_test(is_staff_user)
def manage_clubs(request):
    clubs = Club.objects.select_related('university').all()
    context = {
        'clubs': clubs,
        'total_clubs': clubs.count(),
    }
    return render(request, 'manage_clubs.html', context)

@login_required
@user_passes_test(is_staff_user)
def add_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save()
            messages.success(request, f'Club "{club.name}" added successfully!')
            return redirect('custom_admin:manage_clubs')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClubForm()
    
    context = {
        'form': form,
        'form_title': 'Add Club',
        'submit_label': 'Add Club',
    }
    return render(request, 'club_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def edit_club(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            club = form.save()
            messages.success(request, f'Club "{club.name}" updated successfully!')
            return redirect('custom_admin:manage_clubs')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClubForm(instance=club)
    
    context = {
        'form': form,
        'form_title': 'Edit Club',
        'submit_label': 'Update Club',
    }
    return render(request, 'club_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def delete_club(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        name = club.name
        club.delete()
        messages.success(request, f'Club "{name}" deleted successfully!')
        return redirect('custom_admin:manage_clubs')
    
    context = {'club': club}
    return render(request, 'delete_club.html', context)

@login_required
@user_passes_test(is_staff_user)
def add_admission(request):
    if request.method == 'POST':
        form = AdmissionOpeningForm(request.POST)
        if form.is_valid():
            admission = form.save()
            messages.success(request, f'Admission opening for "{admission.university.name}" added successfully!')
            return redirect('custom_admin:manage_admissions')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdmissionOpeningForm()
    
    context = {'form': form}
    return render(request, 'add_admission.html', context)

@login_required
@user_passes_test(is_staff_user)
def edit_admission(request, pk):
    admission = get_object_or_404(AdmissionOpening, pk=pk)
    
    if request.method == 'POST':
        form = AdmissionOpeningForm(request.POST, instance=admission)
        if form.is_valid():
            admission = form.save()
            messages.success(request, f'Admission opening for "{admission.university.name}" updated successfully!')
            return redirect('custom_admin:manage_admissions')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdmissionOpeningForm(instance=admission)
    
    context = {
        'form': form,
        'admission': admission
    }
    return render(request, 'edit_admission.html', context)

@login_required
@user_passes_test(is_staff_user)
def delete_admission(request, pk):
    admission = get_object_or_404(AdmissionOpening, pk=pk)
    
    if request.method == 'POST':
        university_name = admission.university.name
        admission.delete()
        messages.success(request, f'Admission opening for "{university_name}" deleted successfully!')
        return redirect('custom_admin:manage_admissions')
    
    context = {'admission': admission}
    return render(request, 'delete_admission.html', context)


# --- Scholarships (staff) ---


@login_required
@user_passes_test(is_staff_user)
def manage_scholarships(request):
    scholarships = Scholarship.objects.select_related('university').order_by(
        'sort_order', 'university__name', 'title'
    )
    context = {
        'scholarships': scholarships,
        'total': scholarships.count(),
    }
    return render(request, 'manage_scholarships.html', context)


@login_required
@user_passes_test(is_staff_user)
def add_scholarship(request):
    initial = {}
    uid = request.GET.get('university')
    if uid and str(uid).isdigit() and University.objects.filter(pk=int(uid)).exists():
        initial['university'] = int(uid)
    if request.method == 'POST':
        form = ScholarshipForm(request.POST, request.FILES)
        if form.is_valid():
            s = form.save()
            messages.success(request, f'Scholarship "{s.title}" saved.')
            return redirect('custom_admin:manage_scholarships')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = ScholarshipForm(initial=initial)
    return render(
        request,
        'scholarship_form.html',
        {
            'form': form,
            'form_title': 'Add scholarship',
            'submit_label': 'Save scholarship',
        },
    )


@login_required
@user_passes_test(is_staff_user)
def edit_scholarship(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    if request.method == 'POST':
        form = ScholarshipForm(request.POST, request.FILES, instance=scholarship)
        if form.is_valid():
            form.save()
            messages.success(request, 'Scholarship updated.')
            return redirect('custom_admin:manage_scholarships')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = ScholarshipForm(instance=scholarship)
    return render(
        request,
        'scholarship_form.html',
        {
            'form': form,
            'form_title': 'Edit scholarship',
            'submit_label': 'Update scholarship',
        },
    )


@login_required
@user_passes_test(is_staff_user)
def delete_scholarship(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    if request.method == 'POST':
        title = scholarship.title
        scholarship.delete()
        messages.success(request, f'"{title}" removed.')
        return redirect('custom_admin:manage_scholarships')
    return render(request, 'delete_scholarship.html', {'scholarship': scholarship})


# --- FAQ categories & items ---


@login_required
@user_passes_test(is_staff_user)
def manage_faq_categories(request):
    categories = FaqCategory.objects.all().order_by('sort_order', 'name')
    return render(
        request,
        'manage_faq_categories.html',
        {'categories': categories, 'total': categories.count()},
    )


@login_required
@user_passes_test(is_staff_user)
def add_faq_category(request):
    if request.method == 'POST':
        form = FaqCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ section added.')
            return redirect('custom_admin:manage_faq_categories')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = FaqCategoryForm()
    return render(
        request,
        'faq_category_form.html',
        {
            'form': form,
            'form_title': 'Add FAQ section',
            'submit_label': 'Save section',
        },
    )


@login_required
@user_passes_test(is_staff_user)
def edit_faq_category(request, pk):
    category = get_object_or_404(FaqCategory, pk=pk)
    if request.method == 'POST':
        form = FaqCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section updated.')
            return redirect('custom_admin:manage_faq_categories')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = FaqCategoryForm(instance=category)
    return render(
        request,
        'faq_category_form.html',
        {
            'form': form,
            'form_title': 'Edit FAQ section',
            'submit_label': 'Update section',
        },
    )


@login_required
@user_passes_test(is_staff_user)
def delete_faq_category(request, pk):
    category = get_object_or_404(FaqCategory, pk=pk)
    if request.method == 'POST':
        n = category.name
        category.delete()
        messages.success(request, f'Section "{n}" and its questions were removed.')
        return redirect('custom_admin:manage_faq_categories')
    return render(request, 'delete_faq_category.html', {'category': category})


@login_required
@user_passes_test(is_staff_user)
def manage_faq_items(request):
    items = FaqItem.objects.select_related('category').order_by(
        'category__sort_order', 'category__name', 'sort_order', 'pk'
    )
    return render(
        request,
        'manage_faq_items.html',
        {'items': items, 'total': items.count()},
    )


@login_required
@user_passes_test(is_staff_user)
def add_faq_item(request):
    if not FaqCategory.objects.exists():
        messages.warning(
            request,
            'Create at least one FAQ section before adding questions.',
        )
        return redirect('custom_admin:add_faq_category')
    if request.method == 'POST':
        form = FaqItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ entry published.')
            return redirect('custom_admin:manage_faq')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = FaqItemForm()
    return render(
        request,
        'faq_item_form.html',
        {
            'form': form,
            'form_title': 'Add FAQ entry',
            'submit_label': 'Save entry',
        },
    )


@login_required
@user_passes_test(is_staff_user)
def edit_faq_item(request, pk):
    item = get_object_or_404(FaqItem, pk=pk)
    if request.method == 'POST':
        form = FaqItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ entry updated.')
            return redirect('custom_admin:manage_faq')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = FaqItemForm(instance=item)
    return render(
        request,
        'faq_item_form.html',
        {
            'form': form,
            'form_title': 'Edit FAQ entry',
            'submit_label': 'Update entry',
        },
    )


@login_required
@user_passes_test(is_staff_user)
def delete_faq_item(request, pk):
    item = get_object_or_404(FaqItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'FAQ entry removed.')
        return redirect('custom_admin:manage_faq')
    return render(request, 'delete_faq_item.html', {'item': item})
