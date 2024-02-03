from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Counsellor(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, related_name="appointments", on_delete=models.CASCADE)
    counsellor = models.ForeignKey(Counsellor, related_name="appointments", on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
