from django import forms
from .models import Club


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['university', 'name', 'description']
        labels = {
            'university': 'University',
            'name': 'Club Name',
            'description': 'Club Description',
        }
        widgets = {
            'university': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Debate Club'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Brief description of the club'
            }),
        }
