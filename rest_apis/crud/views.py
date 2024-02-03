# views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Patient, Counsellor, Appointment
from .serializers import PatientSerializer, CounsellorSerializer, AppointmentSerializer
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.filter(is_active = True)
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


class PatientRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.filter(is_active = True)
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CounsellorListCreateView(generics.ListCreateAPIView):
    queryset = Counsellor.objects.filter(is_active = True)
    serializer_class = CounsellorSerializer
    permission_classes = [IsAuthenticated]


class CounsellorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Counsellor.objects.filter(is_active = True)
    serializer_class = CounsellorSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.filter(is_active = True)
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


class AppointmentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.filter(is_active = True)
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class PatientAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Appointment.objects.filter(patient_id=patient_id, is_active = True)

class CounsellorAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        counsellor_id = self.kwargs['counsellor_id']
        return Appointment.objects.filter(counsellor_id=counsellor_id, is_active = True)

class ActiveAppointmentsDateRangeView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if not start_date or not end_date:
            return Appointment.objects.none()

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        return Appointment.objects.filter(
            is_active=True,
            appointment_date__range=(start_date, end_date)
        ).order_by('-appointment_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)