from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from accounts.models import User


class DoctorProfile(models.Model):
    """Doctor profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    years_of_experience = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"
    
    def get_full_name(self):
        return self.user.get_full_name()


class AvailabilitySlot(models.Model):
    """Doctor availability time slots"""
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['doctor', 'date', 'start_time', 'end_time']
    
    def __str__(self):
        return f"{self.doctor.username} - {self.date} {self.start_time} to {self.end_time}"
    
    def is_future(self):
        """Check if slot is in the future"""
        now = timezone.now()
        slot_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.start_time)
        )
        return slot_datetime > now
    
    def is_booked(self):
        """Check if slot is booked"""
        return not self.is_available

