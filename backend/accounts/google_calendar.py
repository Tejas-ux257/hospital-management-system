import requests
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from .models import GoogleCalendarToken

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

SCOPES = "https://www.googleapis.com/auth/calendar"

@login_required
def calendar_authorize(request):
    params = {
        "client_id": settings.GOOGLE_CALENDAR_CLIENT_ID,
        "response_type": "code",
        "scope": SCOPES,
        "redirect_uri": settings.GOOGLE_CALENDAR_REDIRECT_URI,
        "access_type": "offline",
        "prompt": "consent",
    }

    query = "&".join(f"{k}={v}" for k, v in params.items())
    return redirect(f"{AUTH_URL}?{query}")

@login_required
def calendar_callback(request):
    code = request.GET.get("code")

    data = {
        "client_id": settings.GOOGLE_CALENDAR_CLIENT_ID,
        "client_secret": settings.GOOGLE_CALENDAR_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_CALENDAR_REDIRECT_URI,
    }

    response = requests.post(TOKEN_URL, data=data).json()

    GoogleCalendarToken.objects.update_or_create(
        user=request.user,
        defaults={
            "access_token": response["access_token"],
            "refresh_token": response.get("refresh_token"),
            "token_expiry": now() + timedelta(seconds=response["expires_in"]),
        },
    )

    return redirect("patients:dashboard")
