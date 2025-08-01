from django.db import models
from accounts.models import User
from doctors.models import DoctorProfile
from patients.models import PatientProfile


class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="slots")
    weekday = models.IntegerField(choices=[
        (0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'), (3, 'Jeudi'),
        (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')
    ])
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('doctor', 'weekday', 'start_time')
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f"{self.doctor.full_name} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"

    
# appointments/models.py
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('rejected', 'Rejeté'),
    ]

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_doctor')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_patient')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')
