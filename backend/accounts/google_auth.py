from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import json


@login_required
def google_calendar_authorize(request):
    """Initiate Google Calendar OAuth flow"""
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    # Store state in session
    request.session['google_oauth_state'] = state
    
    return redirect(authorization_url)


@login_required
def google_calendar_callback(request):
    """Handle Google Calendar OAuth callback"""
    state = request.session.get('google_oauth_state')
    if not state or state != request.GET.get('state'):
        return redirect('accounts:home')
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
        state=state
    )
    
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    
    # Store credentials in user model
    request.user.google_calendar_token = credentials.token
    request.user.google_calendar_refresh_token = credentials.refresh_token
    request.user.save()
    
    # Clear state from session
    del request.session['google_oauth_state']
    
    from django.contrib import messages
    messages.success(request, 'Google Calendar connected successfully!')
    
    if request.user.is_doctor():
        return redirect('doctors:dashboard')
    else:
        return redirect('patients:dashboard')

