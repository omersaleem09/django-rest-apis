from django.urls import path, include
from .views import PatientAPIView, CounsellorAPIView, AppointmentApiView, CreateUserView

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'patients', PatientAPIView, basename="patients")
router.register(r'counsellors', CounsellorAPIView, basename="counsellors")
router.register(r'appointments', AppointmentApiView, basename="appointments")


urlpatterns = [
    path('', include(router.urls)),
    path('register/', CreateUserView.as_view(), name='create_user'),
]