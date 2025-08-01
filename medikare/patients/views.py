from rest_framework import generics
from .models import PatientProfile
from rest_framework import viewsets
from .serializers import PatientProfileSerializer
from accounts.permissions import IsPatient

class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes=[IsPatient]


    def get_queryset(self):
        # Limite l'accès uniquement au profil du médecin connecté
        return DoctorProfile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
