from django.db import models

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    def __str__(self):
        return self.patient_name

# Create your models here.
