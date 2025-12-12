import os
from datetime import datetime, timedelta
from django.conf import settings
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_google_calendar_service(user):
    """Get Google Calendar service for user"""
    if not user.google_calendar_token:
        return None
    
    try:
        token_dict = {
            'token': user.google_calendar_token,
            'refresh_token': user.google_calendar_refresh_token or '',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'scopes': ['https://www.googleapis.com/auth/calendar']
        }
        
        creds = Credentials.from_authorized_user_info(token_dict)
        
        # Refresh token if needed
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            user.google_calendar_token = creds.token
            if creds.refresh_token:
                user.google_calendar_refresh_token = creds.refresh_token
            user.save()
        
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(f"Error getting calendar service: {e}")
        return None


def create_google_calendar_event(user, title, date, start_time, end_time, description=''):
    """Create a Google Calendar event"""
    service = get_google_calendar_service(user)
    if not service:
        return None
    
    try:
        # Combine date and time
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        
        # Format for Google Calendar API (RFC3339)
        start_rfc3339 = start_datetime.isoformat() + 'Z'
        end_rfc3339 = end_datetime.isoformat() + 'Z'
        
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_rfc3339,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_rfc3339,
                'timeZone': 'UTC',
            },
        }
        
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event.get('id')
    except HttpError as e:
        print(f"Error creating calendar event: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def get_google_oauth_flow():
    """Get Google OAuth flow"""
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
        }
    }
    
    flow = Flow.from_client_config(
        client_config,
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    
    return flow

