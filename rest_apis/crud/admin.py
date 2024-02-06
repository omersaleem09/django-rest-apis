from django.contrib import admin
from .models import Patient, Counsellor, Appointment, User

class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_user_email', 'get_user_active']
    search_fields = ['name', 'get_user_email']
    list_filter = ['id']

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'

    def get_user_active(self,obj):
        return obj.user.is_active
    get_user_active.short_description = 'User Active'

class CounsellorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_user_email', 'get_user_active']
    search_fields = ['name', 'get_user_email']
    list_filter = ['id']

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'

    def get_user_active(self,obj):
        return obj.user.is_active
    get_user_active.short_description = 'User Active'

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'counsellor', 'appointment_date', 'is_active']
    search_fields = ['patient__name', 'counsellor__name', 'appointment_date']
    list_filter = ['is_active']

admin.site.register(Patient, PatientAdmin)
admin.site.register(Counsellor, CounsellorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(User)
