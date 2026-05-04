from django import forms
from django.utils import timezone

from .models import Department, Event, Scholarship, FaqCategory, FaqItem


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['university', 'name', 'description', 'image']
        labels = {
            'university': 'University',
            'name': 'Department Name',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'university': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computer Science and Engineering',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional: programs, focus areas, or notes',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }


class EventForm(forms.ModelForm):
    event_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Event
        fields = ['university', 'title', 'description', 'event_date', 'location', 'image']
        labels = {
            'university': 'University',
            'title': 'Event title',
            'description': 'Description',
            'event_date': 'Date & time',
            'location': 'Location or link',
            'image': 'Image',
        }
        widgets = {
            'university': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Fall Open House 2026',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'What to expect, registration links, etc.',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Main auditorium, or Zoom link',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.event_date:
            self.initial['event_date'] = timezone.localtime(self.instance.event_date).strftime(
                '%Y-%m-%dT%H:%M'
            )


class ScholarshipForm(forms.ModelForm):
    deadline = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )

    class Meta:
        model = Scholarship
        fields = [
            'university',
            'title',
            'tagline',
            'description',
            'deadline',
            'apply_link',
            'is_active',
            'is_featured',
            'image',
            'sort_order',
        ]
        labels = {
            'university': 'University',
            'title': 'Scholarship name',
            'tagline': 'Short highlight',
            'description': 'Full description',
            'deadline': 'Deadline',
            'apply_link': 'Apply / info link',
            'is_active': 'Visible on site',
            'is_featured': 'Featured on home page',
            'image': 'Image',
            'sort_order': 'Display order (lower first)',
        }
        widgets = {
            'university': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Merit Scholarship 2026'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'apply_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.deadline:
            self.initial['deadline'] = self.instance.deadline.isoformat()


class FaqCategoryForm(forms.ModelForm):
    class Meta:
        model = FaqCategory
        fields = ['name', 'slug', 'sort_order']
        labels = {
            'name': 'Section name',
            'slug': 'URL slug (optional, auto if empty)',
            'sort_order': 'Order',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Admissions'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'auto-generated if blank'}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class FaqItemForm(forms.ModelForm):
    class Meta:
        model = FaqItem
        fields = ['category', 'question', 'answer', 'sort_order', 'is_published']
        labels = {
            'category': 'Section',
            'question': 'Question',
            'answer': 'Answer',
            'sort_order': 'Order in section',
            'is_published': 'Published',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
