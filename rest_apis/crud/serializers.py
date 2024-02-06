from rest_framework import serializers, status
from .models import Patient, Counsellor, Appointment
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_password(self, value):
        # Custom password strength validation
        min_length = 8
        if len(value) < min_length:
            raise serializers.ValidationError(
                f"Password must be at least {min_length} characters long."
            )

        return value
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

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

    def validate(self, data):
        patient = data['patient']
        counsellor = data['counsellor']

        # Check if there is an existing active appointment for the patient and counsellor
        existing_active_appointment = Appointment.objects.filter(
            patient=patient,
            counsellor=counsellor,
            is_active=True
        ).exclude(id=data.get('id'))

        if existing_active_appointment.exists():
            raise serializers.ValidationError("A patient and counsellor can have only one active appointment at a time.")

        return data