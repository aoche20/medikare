from rest_framework import serializers
from .models import  AvailabilitySlot, Appointment
from datetime import datetime

 
class AvailabilitySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilitySlot
        fields = '__all__'




class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['status']

    def validate(self, data):
        doctor = data['doctor']
        date = data['date']
        start_time = data['start_time']
        end_time = data['end_time']

        # Vérifie que le créneau est dans les horaires du médecin
        weekday = date.weekday()
        slot_ok = AvailabilitySlot.objects.filter(
            doctor=doctor,
            weekday=weekday,
            start_time__lte=start_time,
            end_time__gte=end_time
        ).exists()

        if not slot_ok:
            raise serializers.ValidationError("Ce créneau n'est pas dans les heures d’ouverture du médecin.")

        # Vérifie les chevauchements
        overlapping = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status__in=['pending', 'accepted']
        )

        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)

        if overlapping.exists():
            raise serializers.ValidationError("Un autre rendez-vous existe déjà pour ce créneau.")

        return data
