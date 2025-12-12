from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_doctor(self):
        return self.role == 'doctor'

    def is_patient(self):
        return self.role == 'patient'


class GoogleCalendarToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="google_calendar"
    )
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expiry = models.DateTimeField()

    def __str__(self):
        return f"Google Calendar Token for {self.user.username}"
    # class Meta:
    #     verbose_name = "Google Calendar Token"
    #     verbose_name_plural = "Google Calendar Tokens"
    #     ordering = ['-user__username']
    #     indexes = [models.Index(fields=['user'])]
    #     constraints = [
    #         models.UniqueConstraint(fields=['user'], name='unique_google_calendar_token_per_user')
    #     ]
    # def is_token_valid(self):
    #     return self.token_expiry > timezone.now()
    # def refresh_access_token(self):
    #     # Logic to refresh the access token using the refresh token
    #     pass



