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
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
User = get_user_model()


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class PatientAPIView(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        queryset = Patient.objects.filter(user__is_active=True)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        patient = self.get_object()
        patient = User.objects.get(id=patient.user_id)
        patient.is_active = False
        patient.save()
        return Response(data='deleted')


class CounsellorAPIView(viewsets.ModelViewSet):
    serializer_class = CounsellorSerializer

    def get_queryset(self):
        queryset = Counsellor.objects.filter(user__is_active=True)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        counsellor = self.get_object()
        counsellor = User.objects.get(id=counsellor.user_id)
        counsellor.is_active = False
        counsellor.save()
        return Response(data='deleted')


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
    
    @action(detail=False, methods=['GET'])
    def appointments_by_email(self, request):
        email = request.query_params.get('email')
        
        if not email :
            return Response({"detail": "'email' required."},
                            status=status.HTTP_400_BAD_REQUEST)

        
        if email:
            user = get_object_or_404(User, email=email, counsellor__isnull=False)
            appointments = Appointment.objects.filter(counsellor=user.counsellor, is_active=True)

        else:
            return Response({"detail": "'role' must be either 'counsellor' or 'patient'."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
