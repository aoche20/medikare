from django.db import models
from accounts.models import User
# Create your models here.
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Homme'), ('female', 'Femme')], blank=True)
    image = models.ImageField(
        upload_to='patients/profiles/',
        blank=True,    
        null=True,       
        default='default/patient.png'    
    )

    def __str__(self):
        return self.user.get_full_name()
