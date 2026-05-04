from django.shortcuts import render
from .models import University
from django.shortcuts import render, get_object_or_404
from .models import University, Event

def home(request):
    universities = University.objects.prefetch_related('clubs').all()

    location_query = request.GET.get('location')
    if location_query:
        universities = universities.filter(address__icontains=location_query)

    max_fee = request.GET.get('max_fee')
    if max_fee:
        universities = universities.filter(cost__lte=max_fee)

    course_type = request.GET.get('course_type')
    if course_type:
        universities = universities.filter(course_type__icontains=course_type)

    subject_group = request.GET.get('subject_group')
    if subject_group:
        universities = universities.filter(subject_group__icontains=subject_group)

    language = request.GET.get('language')
    if language:
        universities = universities.filter(language__icontains=language)

    institution_type = request.GET.get('institution_type')
    if institution_type:
        universities = universities.filter(institution_type__icontains=institution_type)

    credit_system = request.GET.get('credit_system')
    if credit_system:
        universities = universities.filter(credit_system=credit_system)

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
    university = get_object_or_404(University, id=uni_id)
    clubs = university.clubs.all()  # Get all clubs for this university
    context = {
        'university': university,
        'clubs': clubs
    }
    return render(request, 'university_detail.html', context)

def events_list(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})