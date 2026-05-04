from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import University, Event, Admission, Scholarship, FaqCategory, FaqItem

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

    today = timezone.localdate()
    spotlight_deadlines = (
        Admission.objects.filter(is_open=True, deadline__gte=today)
        .select_related('university')
        .order_by('deadline')[:5]
    )
    for row in spotlight_deadlines:
        row.days_left = (row.deadline - today).days

    featured_scholarships = list(
        Scholarship.objects.filter(is_active=True, is_featured=True)
        .select_related('university')
        .order_by('sort_order', 'title')[:6]
    )

    context = {
        'universities': universities,
        'spotlight_deadlines': spotlight_deadlines,
        'spotlight_has_deadlines': bool(spotlight_deadlines),
        'featured_scholarships': featured_scholarships,
        'spotlight_has_scholarships': bool(featured_scholarships),
    }
    return render(request, 'home.html', context)

def university_detail(request, uni_id):
    university = get_object_or_404(
        University.objects.prefetch_related('departments'),
        id=uni_id,
    )
    clubs = university.clubs.all()  # Get all clubs for this university
    listed_departments = university.departments.count()
    now = timezone.now()
    upcoming_events = university.events.filter(event_date__gte=now).order_by('event_date')
    past_events = list(
        university.events.filter(event_date__lt=now).order_by('-event_date')[:6]
    )
    today = timezone.localdate()
    admissions_list = list(
        university.admissions.filter(is_open=True).order_by('deadline')
    )
    for adm in admissions_list:
        adm.days_left = (adm.deadline - today).days

    context = {
        'university': university,
        'clubs': clubs,
        'department_count_display': listed_departments or university.total_departments,
        'has_department_list': listed_departments > 0,
        'admissions_list': admissions_list,
        'today': today,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'scholarships_list': university.scholarships.filter(is_active=True).order_by(
            'sort_order', 'title'
        ),
    }
    return render(request, 'university_detail.html', context)


def university_departments(request, uni_id):
    university = get_object_or_404(University, id=uni_id)
    departments = university.departments.all()
    context = {
        'university': university,
        'departments': departments,
    }
    return render(request, 'departments.html', context)

def events_list(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(event_date__gte=now).select_related(
        'university'
    ).order_by('event_date')
    past_events = list(
        Event.objects.filter(event_date__lt=now)
        .select_related('university')
        .order_by('-event_date')[:24]
    )
    return render(
        request,
        'events.html',
        {
            'upcoming_events': upcoming_events,
            'past_events': past_events,
        },
    )


def scholarships_list(request):
    qs = Scholarship.objects.filter(is_active=True).select_related('university')
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            | Q(tagline__icontains=q)
            | Q(description__icontains=q)
            | Q(university__name__icontains=q)
        )
    qs = qs.order_by('sort_order', 'deadline', 'title')
    return render(
        request,
        'scholarships.html',
        {'scholarships': qs, 'search_query': q},
    )


def faq_page(request):
    sections = []
    for cat in FaqCategory.objects.order_by('sort_order', 'name'):
        items = list(
            cat.items.filter(is_published=True).order_by('sort_order', 'pk')
        )
        if items:
            sections.append({'category': cat, 'items': items})
    return render(request, 'faq.html', {'faq_sections': sections})