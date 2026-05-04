from django.db import models
from universities.models import University

class Club(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='clubs')
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.university.name}"

    class Meta:
        verbose_name_plural = "Clubs"
        ordering = ['name']
