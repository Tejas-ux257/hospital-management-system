from django.contrib import admin
from .models import DoctorProfile, AvailabilitySlot


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'years_of_experience')
    search_fields = ('user__username', 'user__email', 'specialization')


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('date', 'is_available', 'doctor')
    search_fields = ('doctor__username',)

