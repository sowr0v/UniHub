from django.contrib import admin
from .models import AdmissionOpening

@admin.register(AdmissionOpening)
class AdmissionOpeningAdmin(admin.ModelAdmin):
    list_display = ['university', 'opening_datetime', 'is_active', 'created_at']
    list_filter = ['is_active', 'opening_datetime']
    search_fields = ['university__name']
    list_editable = ['is_active']
    date_hierarchy = 'opening_datetime'
    ordering = ['opening_datetime']
