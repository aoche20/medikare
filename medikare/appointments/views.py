from rest_framework import viewsets
from .models import  AvailabilitySlot, Appointment
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class AvailabilitySlotViewSet(viewsets.ModelViewSet):
    queryset = AvailabilitySlot.objects.all()
    serializer_class = AvailabilitySlotSerializer


# appointments/views.py


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)
        return Appointment.objects.filter(patient=user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        appointment = self.get_object()
        if appointment.doctor != request.user:
            return Response({'detail': "Non autorisé."}, status=403)
        appointment.status = 'accepted'
        appointment.save()
        return Response({'detail': "Rendez-vous accepté."})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        appointment = self.get_object()
        if appointment.doctor != request.user:
            return Response({'detail': "Non autorisé."}, status=403)
        appointment.status = 'rejected'
        appointment.save()
        return Response({'detail': "Rendez-vous rejeté."})
