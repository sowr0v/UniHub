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
    website = models.URLField(max_length=500, blank=True, null=True)
    short_name = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., BUET,BRACU,NSU,AIUB, UAP")
    CREDIT_CHOICES = [
        ('Open', 'Open Credit'),
        ('Closed', 'Closed Credit'),
    ]
    credit_system = models.CharField(max_length=10, choices=CREDIT_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"
        ordering = ['name']


class Event(models.Model):
    # Links this event to a specific university
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200, help_text="e.g., Main Auditorium or Zoom Link")

    def __str__(self):
        return f"{self.title} - {self.university.name}"

    class Meta:
        ordering = ['event_date']  # Shows the closest events first


class Admission(models.Model):
    # Links this admission cycle to a specific university
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='admissions')
    degree_level = models.CharField(max_length=100, help_text="e.g., Bachelor's Fall 2026")
    deadline = models.DateField()
    apply_link = models.URLField(blank=True, null=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.university.name} - {self.degree_level}"

    class Meta:
        ordering = ['deadline']  # Shows the most urgent deadlines first