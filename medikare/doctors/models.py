from django.db import models
from accounts.models import User

class Specialty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(
        upload_to='doctors/profiles/',  # Dossier où les images seront sauvegardées
        blank=True,                     # Optionnel (peut être vide)
        null=True,                      # Optionnel en base de données
        default='default/doctor.png'    # Image par défaut (optionnel)
    )

    def __str__(self):
        return f"{self.user.full_name} ({self.specialty})"
