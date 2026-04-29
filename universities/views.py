from django.shortcuts import render
from .models import University
from django.shortcuts import render, get_object_or_404

def home(request):
    universities = University.objects.all()

    # 1. Location & Fee (Existing)
    location_query = request.GET.get('location')
    if location_query:
        universities = universities.filter(location__icontains=location_query)

    max_fee = request.GET.get('max_fee')
    if max_fee:
        universities = universities.filter(tuition_fee__lte=max_fee)

    # --- NEW ADVANCED FILTERS ---

    # 2. Degree / Course Type (e.g., Bachelor, Master)
    course_type = request.GET.get('course_type')
    if course_type:
        universities = universities.filter(course_type__icontains=course_type)

    # 3. Subject Group
    subject_group = request.GET.get('subject_group')
    if subject_group:
        universities = universities.filter(subject_group__icontains=subject_group)

    # 4. Language
    language = request.GET.get('language')
    if language:
        universities = universities.filter(language__icontains=language)

    # 5. Institution Type (e.g., University, Applied Sciences)
    institution_type = request.GET.get('institution_type')
    if institution_type:
        universities = universities.filter(institution_type__icontains=institution_type)

    # --- END NEW FILTERS ---

    # 6. Sorting (Existing)
    sort_by = request.GET.get('sort')
    if sort_by == 'ranking':
        universities = universities.order_by('ranking')
    elif sort_by == 'fee_low':
        universities = universities.order_by('tuition_fee')
    elif sort_by == 'fee_high':
        universities = universities.order_by('-tuition_fee')

    context = {
        'universities': universities
    }
    return render(request, 'home.html', context)


def university_detail(request, uni_id):
    # Fetch the specific university or return a 404 error if it doesn't exist
    university = get_object_or_404(University, id=uni_id)

    context = {
        'university': university
    }
    return render(request, 'university_detail.html', context)
