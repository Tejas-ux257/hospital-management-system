from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from accounts.models import User
from doctors.models import AvailabilitySlot, DoctorProfile
from appointments.models import Appointment
from .models import PatientProfile


@login_required
def patient_dashboard(request):
    """Patient dashboard"""
    if not request.user.is_patient():
        messages.error(request, 'Access denied. Patient access required.')
        return redirect('accounts:home')
    
    # Get or create patient profile
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        patient=request.user,
        appointment_date__gte=timezone.now().date()
    ).order_by('appointment_date', 'appointment_time')[:10]
    
    # Get past appointments
    past_appointments = Appointment.objects.filter(
        patient=request.user,
        appointment_date__lt=timezone.now().date()
    ).order_by('-appointment_date', '-appointment_time')[:10]
    
    context = {
        'profile': profile,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
    }
    return render(request, 'patients/dashboard.html', context)


@login_required
def doctor_list(request):
    """List all doctors"""
    if not request.user.is_patient():
        messages.error(request, 'Access denied.')
        return redirect('accounts:home')
    
    doctors = User.objects.filter(role='doctor').select_related('doctor_profile')
    return render(request, 'patients/doctor_list.html', {'doctors': doctors})


@login_required
def doctor_availability(request, doctor_id):
    """View doctor availability"""
    if not request.user.is_patient():
        messages.error(request, 'Access denied.')
        return redirect('accounts:home')
    
    doctor = User.objects.filter(id=doctor_id, role='doctor').first()
    if not doctor:
        messages.error(request, 'Doctor not found.')
        return redirect('patients:doctor_list')
    
    # Get available slots (future and not booked)
    now = timezone.now()
    available_slots = AvailabilitySlot.objects.filter(
        doctor=doctor,
        is_available=True,
        date__gte=now.date()
    ).order_by('date', 'start_time')
    
    # Filter out past slots
    available_slots = [
        slot for slot in available_slots 
        if slot.is_future()
    ]
    
    context = {
        'doctor': doctor,
        'available_slots': available_slots,
    }
    return render(request, 'patients/doctor_availability.html', context)


@login_required
def view_appointments(request):
    """View patient appointments"""
    if not request.user.is_patient():
        messages.error(request, 'Access denied.')
        return redirect('accounts:home')
    
    appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date', '-appointment_time')
    return render(request, 'patients/view_appointments.html', {'appointments': appointments})

