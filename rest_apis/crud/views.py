# views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Patient, Counsellor, Appointment
from .serializers import PatientSerializer, CounsellorSerializer, AppointmentSerializer
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class PatientAPIView(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        queryset = Patient.objects.filter(user__is_active=True)
        return queryset


class CounsellorAPIView(viewsets.ModelViewSet):
    serializer_class = CounsellorSerializer

    def get_queryset(self):
        queryset = Counsellor.objects.filter(user__is_active=True)
        return queryset


class AppointmentApiView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        # Check if the patient and counsellor are active
        patient = serializer.validated_data['patient']
        counsellor = serializer.validated_data['counsellor']

        if not patient.is_active:
            return Response({"detail": "The patient must be active to create an appointment."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not counsellor.is_active:
            return Response({"detail": "The counsellor must be active to create an appointment."},
                            status=status.HTTP_400_BAD_REQUEST)

        # If both patient and counsellor are active, proceed with the appointment creation
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)   
