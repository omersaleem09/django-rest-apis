from django.db import models
from django.core.exceptions import ValidationError

class Patient(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Counsellor(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, related_name="appointments", on_delete=models.CASCADE)
    counsellor = models.ForeignKey(Counsellor, related_name="appointments", on_delete=models.CASCADE)
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
        return f"{self.patient.name}'s appointment with {self.counsellor.name}"
    