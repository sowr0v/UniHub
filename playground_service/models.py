from django.db import models
from universities.models import University

class PlaygroundService(models.Model):
    university = models.OneToOneField(
        University, 
        on_delete=models.CASCADE,
        related_name='playgroundservice'
    )
    has_playground_service = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.university.name} - {'Yes' if self.has_playground_service else 'No'}"
