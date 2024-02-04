from django.contrib import admin
from .models import Patient, Counsellor, Appointment

class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_user_email', 'is_active']
    search_fields = ['name', 'user__email']
    list_filter = ['is_active']

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'

class CounsellorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_user_email', 'is_active']
    search_fields = ['name', 'user__email']
    list_filter = ['is_active']

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'counsellor', 'appointment_date', 'is_active']
    search_fields = ['patient__name', 'counsellor__name', 'appointment_date']
    list_filter = ['is_active']

admin.site.register(Patient, PatientAdmin)
admin.site.register(Counsellor, CounsellorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
