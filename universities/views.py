from django.shortcuts import render
from .models import University
from django.shortcuts import render, get_object_or_404
from .models import University, Event, Admission

def home(request):
    universities = University.objects.all()

    # Location and Fee
    location_query = request.GET.get('location')
    if location_query:
        universities = universities.filter(address__icontains=location_query)

    max_fee = request.GET.get('max_fee')
    if max_fee:
        universities = universities.filter(cost__lte=max_fee)

    # Advanced Filters

    # Degree / Course Type
    course_type = request.GET.get('course_type')
    if course_type:
        universities = universities.filter(course_type__icontains=course_type)

    # Subject Group
    subject_group = request.GET.get('subject_group')
    if subject_group:
        universities = universities.filter(subject_group__icontains=subject_group)

    # Language
    language = request.GET.get('language')
    if language:
        universities = universities.filter(language__icontains=language)

    # Institution Type
    institution_type = request.GET.get('institution_type')
    if institution_type:
        universities = universities.filter(institution_type__icontains=institution_type)
    # Sorting by Credit
    credit_system = request.GET.get('credit_system')
    if credit_system:
        # This matches the database field to the dropdown choice
        universities = universities.filter(credit_system=credit_system)



    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'ranking':
        universities = universities.order_by('qs_ranking')
    elif sort_by == 'fee_low':
        universities = universities.order_by('cost')
    elif sort_by == 'fee_high':
        universities = universities.order_by('-cost')

    context = {
        'universities': universities
    }
    return render(request, 'home.html', context)



def university_detail(request, uni_id):
    # Fetch specific university
    university = get_object_or_404(University, id=uni_id)

    context = {
        'university': university
    }
    return render(request, 'university_detail.html', context)

def events_list(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def admissions_list(request):
    # Show open admissions
    admissions = Admission.objects.filter(is_open=True)
    return render(request, 'admissions.html', {'admissions': admissions})