from django.contrib import admin
from .models import University

admin.site.register(University)
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
