from rest_framework import generics
from rest_framework import viewsets
from .models import DoctorProfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from .serializers import DoctorProfileSerializer
from accounts.permissions import IsDoctor

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsDoctor]


    def get_queryset(self):
        # Limite l'accès uniquement au profil du médecin connecté
        return DoctorProfile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)



@api_view(['GET'])
def available_slots(request, doctor_id, date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    weekday = date.weekday()
    slots = AvailabilitySlot.objects.filter(doctor_id=doctor_id, weekday=weekday)

    appointments = Appointment.objects.filter(doctor_id=doctor_id, date=date, status__in=['pending', 'accepted'])

    taken_ranges = [(a.start_time, a.end_time) for a in appointments]

    available = []
    for slot in slots:
        taken = any(slot.start_time < end and slot.end_time > start for start, end in taken_ranges)
        if not taken:
            available.append({
                'start': slot.start_time,
                'end': slot.end_time,
            })

    return Response(available)

 

    