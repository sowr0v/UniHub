from django import forms
from .models import PlaygroundService

class PlaygroundServiceForm(forms.ModelForm):
    class Meta:
        model = PlaygroundService
        fields = ['university', 'has_playground_service']
        widgets = {
            'has_playground_service': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        }
