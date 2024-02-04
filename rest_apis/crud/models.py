from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.email

class Counsellor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.user.email

class Appointment(models.Model):
    patient = models.ForeignKey(User, related_name="appointments_as_patient", on_delete=models.CASCADE)
    counsellor = models.ForeignKey(User, related_name="appointments_as_counsellor", on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def clean(self):
        if Appointment.objects.filter(
            patient=self.patient, is_active=True
        ).exclude(id=self.id).exists() or \
            Appointment.objects.filter(
                counsellor=self.counsellor, is_active=True
            ).exclude(id=self.id).exists():
            raise ValidationError("A patient and counsellor can have only one active appointment at a time.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.username}'s appointment with {self.counsellor.username}"
