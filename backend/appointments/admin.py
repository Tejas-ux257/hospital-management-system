from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'appointment_date', 'appointment_time', 'created_at')
    list_filter = ('appointment_date', 'doctor', 'patient')
    search_fields = ('doctor__username', 'patient__username')
    readonly_fields = ('created_at', 'updated_at')

