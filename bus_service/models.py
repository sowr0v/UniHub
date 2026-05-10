from django.db import models
from universities.models import University

class BusService(models.Model):
    university = models.OneToOneField(
        University, 
        on_delete=models.CASCADE,
        related_name='busservice'
    )
    has_bus_service = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.university.name} - {'Yes' if self.has_bus_service else 'No'}"

# Create your models here.
