from django import forms
from .models import AdmissionOpening
from django.utils import timezone

class AdmissionOpeningForm(forms.ModelForm):
    opening_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = AdmissionOpening
        fields = ['university', 'opening_datetime', 'info_link', 'is_active']
        widgets = {
            'info_link': forms.URLInput(attrs={'placeholder': 'https://example.com/admission'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.opening_datetime:
            self.initial['opening_datetime'] = timezone.localtime(self.instance.opening_datetime).strftime('%Y-%m-%dT%H:%M')
