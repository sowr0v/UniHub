from django.db import models
from universities.models import University

class HostelService(models.Model):
    university = models.OneToOneField(
        University, 
        on_delete=models.CASCADE,
        related_name='hostelservice'
    )
    has_hostel_service = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.university.name} - {'Yes' if self.has_hostel_service else 'No'}"
