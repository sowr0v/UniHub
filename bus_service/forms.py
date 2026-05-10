from django import forms from .models
import BusService class BusServiceForm(forms.ModelForm):
    class Meta:
        model = BusService
        fields = ['university', 'has_bus_service']
        widgets = { 'has_bus_service': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]), }