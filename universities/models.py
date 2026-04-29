from django.db import models

class University(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    total_departments = models.IntegerField()
    faculty = models.IntegerField()
    qs_ranking = models.IntegerField(null=True, blank=True)
    publications = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    admission_requirements = models.TextField()
    image = models.ImageField(upload_to='universities/', blank=True, null=True, help_text="Upload university image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"
        ordering = ['name']
