from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from doctors.models import DoctorProfile
from patients.models import PatientProfile

@receiver(post_save, sender=User)
def create_profile_based_on_role(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'doctor':
            DoctorProfile.objects.create(user=instance)
        elif instance.role == 'patient':
            PatientProfile.objects.create(user=instance)
