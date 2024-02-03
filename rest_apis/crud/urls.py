# urls.py
from django.urls import path
from .views import (
    PatientListCreateView, PatientRetrieveUpdateDeleteView,
    CounsellorListCreateView, CounsellorRetrieveUpdateDeleteView,
    AppointmentListCreateView, AppointmentRetrieveUpdateDeleteView,
    PatientAppointmentsView, CounsellorAppointmentsView, ActiveAppointmentsDateRangeView
)

urlpatterns = [
    # Patient URLs
    path('patients/', PatientListCreateView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', PatientRetrieveUpdateDeleteView.as_view(), name='patient-detail'),
    path('patients/<int:patient_id>/appointments/', PatientAppointmentsView.as_view(), name='patient-appointments'),

    # Counsellor URLs
    path('counsellors/', CounsellorListCreateView.as_view(), name='counsellor-list'),
    path('counsellors/<int:pk>/', CounsellorRetrieveUpdateDeleteView.as_view(), name='counsellor-detail'),
    path('counsellors/<int:counsellor_id>/appointments/', CounsellorAppointmentsView.as_view(), name='counsellor-appointments'),

    # Appointment URLs
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', AppointmentRetrieveUpdateDeleteView.as_view(), name='appointment-detail'),
    path('appointments/active-date-range/', ActiveAppointmentsDateRangeView.as_view(), name='active-appointments-date-range'),
]
