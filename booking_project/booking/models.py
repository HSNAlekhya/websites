from django.db import models


class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    booking_date = models.DateField()
    booking_time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.booking_date}"

# Create your models here.
