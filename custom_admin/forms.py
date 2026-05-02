from django import forms
from universities.models import University


class UniversityForm(forms.ModelForm):

    class Meta:
        model = University
        fields = [
            'name',
            'address',
            'contact',
            'image',
            'total_departments',
            'faculty',
            'qs_ranking',
            'publications',
            'cost',
            'admission_requirements',
            'google_maps_link',
            'website',
            'credit_system',
            'short_name',
        ]
        
    
        labels = {
            'name': 'University Name',
            'address': 'Address',
            'contact': 'Contact Information',
            'image': 'University Image',
            'total_departments': 'Total Departments',
            'faculty': 'Faculty Members',
            'qs_ranking': 'QS World Ranking',
            'publications': 'Research Publications',
            'cost': 'Annual Cost (USD)',
            'admission_requirements': 'Admission Requirements',
            'google_maps_link': 'Google Maps Navigation Link',
            'website': 'Official Website',
            'credit_system': 'Credit System',
            'short_name': 'Short Name / Acronym',
        }
        
        
        help_texts = {
            'name': 'Enter the full name of the university',
            'image': 'Upload an image file (JPG, PNG, etc.)',
            'qs_ranking': 'Leave blank if not ranked',
            'publications': 'Total number of research publications',
            'cost': 'Annual tuition cost in USD',
            'website': 'Enter the full URL (e.g., https://uap-bd.edu)',
        }
        
        # Custom widgets for better form styling
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., University of Asia Pacific'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete address'
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +1-650-723-2300'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'total_departments': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'e.g., 40'
            }),
            'faculty': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'e.g., 2240'
            }),
            'qs_ranking': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'e.g., 5'
            }),
            'publications': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'e.g., 15000'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'e.g., 55473.00'
            }),
            'admission_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'e.g., SAT: 1470-1570, GPA: 3.9+, Strong extracurriculars'
            }),
            'google_maps_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., https://maps.app.goo.gl/...'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }),
            'credit_system': forms.Select(attrs={'class': 'form-control'
            }),
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., BUET, UAP'
            }),

        }
    
    def clean_name(self):
        """
        Custom validation for university name.
        Ensures the name is not empty and has minimum length.
        """
        name = self.cleaned_data.get('name')
        if name and len(name) < 3:
            raise forms.ValidationError('University name must be at least 3 characters long.')
        return name
    
    def clean_cost(self):
        """
        Custom validation for cost field.
        Ensures cost is a positive number.
        """
        cost = self.cleaned_data.get('cost')
        if cost and cost < 0:
            raise forms.ValidationError('Cost cannot be negative.')
        return cost
    
    def clean_total_departments(self):
        """
        Custom validation for total departments.
        Ensures it's a positive integer.
        """
        total_departments = self.cleaned_data.get('total_departments')
        if total_departments and total_departments < 1:
            raise forms.ValidationError('Total departments must be at least 1.')
        return total_departments
    
    def clean_faculty(self):
        """
        Custom validation for faculty count.
        Ensures it's a positive integer.
        """
        faculty = self.cleaned_data.get('faculty')
        if faculty and faculty < 1:
            raise forms.ValidationError('Faculty count must be at least 1.')
        return faculty
    
    def clean_qs_ranking(self):
        """
        Custom validation for QS ranking.
        Ensures it's a positive integer if provided.
        """
        qs_ranking = self.cleaned_data.get('qs_ranking')
        if qs_ranking and qs_ranking < 1:
            raise forms.ValidationError('QS ranking must be a positive number.')
        return qs_ranking
