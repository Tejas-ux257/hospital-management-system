from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils import timezone
from accounts.models import User
from .models import DoctorProfile, AvailabilitySlot
from .forms import DoctorProfileForm, AvailabilitySlotForm
from appointments.models import Appointment


@login_required
def google_authorize(request):
    return redirect('/accounts/google/login/')


@login_required
def doctor_dashboard(request):
    """Doctor dashboard"""
    if not request.user.is_doctor():
        messages.error(request, 'Access denied. Doctor access required.')
        return redirect('accounts:home')
    
    # Get or create doctor profile
    profile, created = DoctorProfile.objects.get_or_create(user=request.user)
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        doctor=request.user,
        appointment_date__gte=timezone.now().date()
    ).order_by('appointment_date', 'appointment_time')[:10]
    
    # Get availability slots
    availability_slots = AvailabilitySlot.objects.filter(
        doctor=request.user,
        date__gte=timezone.now().date()
    ).order_by('date', 'start_time')[:20]
    
    context = {
        'profile': profile,
        'upcoming_appointments': upcoming_appointments,
        'availability_slots': availability_slots,
    }
    return render(request, 'doctors/dashboard.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def manage_profile(request):
    """Manage doctor profile"""
    if not request.user.is_doctor():
        messages.error(request, 'Access denied.')
        return redirect('accounts:home')
    
    profile, created = DoctorProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('doctors:dashboard')
    else:
        form = DoctorProfileForm(instance=profile)
    
    return render(request, 'doctors/manage_profile.html', {'form': form})


@login_required
def availability_list(request):
    """List doctor availability slots"""
    if not request.user.is_doctor():
        messages.error(request, 'Access denied.')
        return redirect('accounts:home')
    
    slots = AvailabilitySlot.objects.filter(doctor=request.user).order_by('-date', '-start_time')
    return render(request, 'doctors/availability_list.html', {'slots': slots})


@login_required
@require_http_methods(["GET", "POST"])
def create_availability(request):
    """Create availability slot"""
    if not request.user.is_doctor():
        messages.error(request, 'Access denied.')
        return redirect('accounts:home')
    
    if request.method == 'POST':
        form = AvailabilitySlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user
            slot.save()
            messages.success(request, 'Availability slot created successfully!')
            return redirect('doctors:availability_list')
    else:
        form = AvailabilitySlotForm()
    
    return render(request, 'doctors/create_availability.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def delete_availability(request, slot_id):
    """Delete availability slot"""
    if not request.user.is_doctor():
        messages.error(request, 'Access denied.')
        return redirect('accounts:home')
    
    slot = get_object_or_404(AvailabilitySlot, id=slot_id, doctor=request.user)
    
    # Check if slot is booked
    if not slot.is_available:
        messages.error(request, 'Cannot delete a booked slot.')
        return redirect('doctors:availability_list')
    
    slot.delete()
    messages.success(request, 'Availability slot deleted successfully!')
    return redirect('doctors:availability_list')


@login_required
def view_bookings(request):
    """View doctor bookings"""
    if not request.user.is_doctor():
        messages.error(request, 'Access denied.')
        return redirect('accounts:home')
    
    appointments = Appointment.objects.filter(doctor=request.user).order_by('-appointment_date', '-appointment_time')
    return render(request, 'doctors/view_bookings.html', {'appointments': appointments})

