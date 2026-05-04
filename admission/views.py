from datetime import datetime, time, timedelta
from urllib.parse import quote

from django.shortcuts import render
from django.utils import timezone

from universities.models import Admission as ApplicationRound
from .models import AdmissionOpening


def admissions_hub(request):
    """Unified admissions view: portal opening countdowns + degree application deadlines."""
    now = timezone.now()
    today = timezone.localdate()
    q = request.GET.get('q', '').strip()

    openings_base = AdmissionOpening.objects.filter(is_active=True).select_related(
        'university'
    )
    if q:
        openings_base = openings_base.filter(university__name__icontains=q)

    openings_upcoming = list(
        openings_base.filter(opening_datetime__gt=now).order_by(
            'opening_datetime',
            'university__name',
            'id',
        )
    )
    openings_past = list(
        openings_base.filter(opening_datetime__lte=now).order_by(
            '-opening_datetime',
            'university__name',
            'id',
        )[:15]
    )

    deadlines_qs = ApplicationRound.objects.filter(
        is_open=True,
        deadline__gte=today,
    ).select_related('university')
    if q:
        deadlines_qs = deadlines_qs.filter(university__name__icontains=q)
    deadlines_qs = deadlines_qs.order_by('deadline', 'university__name', 'degree_level', 'id')

    deadline_rows = []
    week_l = today + timedelta(days=7)
    fort_l = today + timedelta(days=14)
    deadlines_closing_week = 0
    deadlines_closing_fortnight = 0

    for app in deadlines_qs:
        days_left = (app.deadline - today).days
        if app.deadline <= week_l:
            deadlines_closing_week += 1
        if app.deadline <= fort_l:
            deadlines_closing_fortnight += 1

        end_day = app.deadline + timedelta(days=1)
        title = f"Apply — {app.degree_level} ({app.university.name})"
        gcal_url = (
            'https://www.google.com/calendar/render?action=TEMPLATE'
            f'&text={quote(title)}'
            f'&dates={app.deadline.strftime("%Y%m%d")}/{end_day.strftime("%Y%m%d")}'
        )
        urgency = 'critical' if days_left <= 7 else ('soon' if days_left <= 30 else 'ok')
        app.gcal_url = gcal_url
        app.days_left = days_left
        app.urgency = urgency
        deadline_rows.append(app)

    next_week = now + timedelta(days=7)
    openings_next_7 = sum(
        1
        for o in openings_upcoming
        if o.opening_datetime <= next_week
    )

    # Unified timeline: soonest event first (deadlines at start of local day vs portal datetimes)
    timeline = []
    for app in deadline_rows:
        start_of_day = timezone.make_aware(
            datetime.combine(app.deadline, time.min),
            timezone.get_current_timezone(),
        )
        timeline.append(
            {
                'sort_key': start_of_day,
                'kind': 'deadline',
                'deadline': app,
            }
        )
    for o in openings_upcoming:
        timeline.append(
            {
                'sort_key': o.opening_datetime,
                'kind': 'portal',
                'opening': o,
            }
        )
    timeline.sort(key=lambda row: row['sort_key'])
    timeline_preview = timeline[:30]

    context = {
        'openings_upcoming': openings_upcoming,
        'openings_past': openings_past,
        'deadlines': deadline_rows,
        'timeline_preview': timeline_preview,
        'search_query': q,
        'current_time': now,
        'today': today,
        'stats': {
            'opening_count': len(openings_upcoming),
            'deadline_count': len(deadline_rows),
            'openings_next_7': openings_next_7,
            'deadlines_week': deadlines_closing_week,
            'deadlines_fortnight': deadlines_closing_fortnight,
        },
    }
    return render(request, 'admissions_hub.html', context)
