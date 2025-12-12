import requests
import os
from django.conf import settings


def send_welcome_email(email, name, role):
    """Send welcome email via serverless service"""
    email_service_url = settings.EMAIL_SERVICE_URL
    
    payload = {
        'action': 'SIGNUP_WELCOME',
        'to': email,
        'name': name,
        'role': role
    }
    
    try:
        response = requests.post(email_service_url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send welcome email: {e}")
        raise


def send_booking_confirmation_email(patient_email, doctor_email, patient_name, doctor_name, appointment_date, appointment_time):
    """Send booking confirmation email via serverless service"""
    email_service_url = settings.EMAIL_SERVICE_URL
    
    # Send to patient
    patient_payload = {
        'action': 'BOOKING_CONFIRMATION',
        'to': patient_email,
        'patient_name': patient_name,
        'doctor_name': doctor_name,
        'appointment_date': appointment_date,
        'appointment_time': appointment_time,
        'recipient_type': 'patient'
    }
    
    # Send to doctor
    doctor_payload = {
        'action': 'BOOKING_CONFIRMATION',
        'to': doctor_email,
        'patient_name': patient_name,
        'doctor_name': doctor_name,
        'appointment_date': appointment_date,
        'appointment_time': appointment_time,
        'recipient_type': 'doctor'
    }
    
    try:
        # Send to patient
        response1 = requests.post(email_service_url, json=patient_payload, timeout=5)
        response1.raise_for_status()
        
        # Send to doctor
        response2 = requests.post(email_service_url, json=doctor_payload, timeout=5)
        response2.raise_for_status()
        
        return {'patient': response1.json(), 'doctor': response2.json()}
    except requests.exceptions.RequestException as e:
        print(f"Failed to send booking confirmation email: {e}")
        raise

