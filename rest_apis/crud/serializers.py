# serializers.py
from rest_framework import serializers, status
from .models import Patient, Counsellor, Appointment
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.response import Response

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class CounsellorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counsellor
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(f"Error saving appointment: {str(e)}")

        return instance