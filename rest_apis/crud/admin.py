from django.contrib import admin
from .models import Patient, Counsellor, Appointment

class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'is_active']
    search_fields = ['name', 'email']
    list_filter = ['is_active']

class CounsellorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'is_active']
    search_fields = ['name', 'email']
    list_filter = ['is_active']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'counsellor', 'appointment_date', 'is_active']
    search_fields = ['patient__name', 'counsellor__name', 'appointment_date']
    list_filter = ['is_active']

admin.site.register(Patient, PatientAdmin)
admin.site.register(Counsellor, CounsellorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
