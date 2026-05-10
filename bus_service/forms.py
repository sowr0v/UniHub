from django.db import models

class BusService(models.Model):

    BUS_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('upcoming', 'Up Coming'),
        ('depend', 'Depend on Students Needed'),
    ]

    university = models.CharField(max_length=200)

    has_bus_service = models.CharField(
        max_length=20,
        choices=BUS_CHOICES
    )