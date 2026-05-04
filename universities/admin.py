from django.contrib import admin
from .models import University, Department, Event, Scholarship, FaqCategory, FaqItem
from clubs.models import Club

class ClubInline(admin.TabularInline):
    model = Club
    extra = 0  # Number of empty forms to display


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0


class EventInline(admin.TabularInline):
    model = Event
    extra = 0


class FaqItemInline(admin.TabularInline):
    model = FaqItem
    extra = 0


@admin.register(FaqCategory)
class FaqCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'sort_order']
    inlines = [FaqItemInline]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FaqItem)
class FaqItemAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_published', 'sort_order']
    list_filter = ['category', 'is_published']


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'university', 'deadline', 'is_active', 'is_featured', 'sort_order']
    list_filter = ['is_active', 'is_featured', 'university']
    search_fields = ['title', 'tagline', 'university__name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'university', 'event_date', 'location']
    list_filter = ['event_date', 'university']
    search_fields = ['title', 'description', 'university__name']
    ordering = ['-event_date']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'description_short']
    list_filter = ['university']
    search_fields = ['name', 'university__name']

    @admin.display(description='Description')
    def description_short(self, obj):
        if not obj.description:
            return '—'
        return (obj.description[:60] + '…') if len(obj.description) > 60 else obj.description


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact', 'total_departments', 'faculty', 'qs_ranking', 'cost']
    list_filter = ['qs_ranking', 'total_departments']
    search_fields = ['name', 'address']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'contact')
        }),
        ('Image', {
            'fields': ('image',),
            'description': 'Upload an image file '
        }),
        ('Academic Details', {
            'fields': ('total_departments', 'faculty', 'qs_ranking', 'publications')
        }),
        ('Admission Information', {
            'fields': ('cost', 'admission_requirements')
        }),
    )
    inlines = [DepartmentInline, ClubInline, EventInline]
