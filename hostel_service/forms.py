from django import forms
from .models import HostelService

class HostelServiceForm(forms.ModelForm):
    class Meta:
        model = HostelService
        fields = ['university', 'has_hostel_service']
        widgets = {
            'has_hostel_service': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        }
