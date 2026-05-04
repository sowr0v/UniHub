from django.db import models
from universities.models import University

class AdmissionOpening(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='admission_openings')
    opening_datetime = models.DateTimeField()
    info_link = models.URLField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.university.name} - {self.opening_datetime}"

    class Meta:
        ordering = ['opening_datetime']
        verbose_name = "Admission Opening"
        verbose_name_plural = "Admission Openings"
