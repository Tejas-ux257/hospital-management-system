from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils import timezone
from accounts.models import User
from doctors.models import AvailabilitySlot
from .models import Appointment
from .forms import BookingForm
from .services import create_google_calendar_event
from accounts.services import send_booking_confirmation_email


@login_required
@require_http_methods(["GET", "POST"])
def create_booking(request, slot_id):
    """Create appointment booking"""
    if not request.user.is_patient():
        messages.error(request, 'Access denied. Patient access required.')
        return redirect('accounts:home')
    
    slot = get_object_or_404(AvailabilitySlot, id=slot_id)
    
    # Verify slot is available
    if not slot.is_available:
        messages.error(request, 'This slot is already booked.')
        return redirect('patients:doctor_availability', doctor_id=slot.doctor.id)
    
    if not slot.is_future():
        messages.error(request, 'Cannot book past time slots.')
        return redirect('patients:doctor_availability', doctor_id=slot.doctor.id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            slot_id = form.cleaned_data['slot_id']
            notes = form.cleaned_data.get('notes', '')
            
            # Use database transaction to prevent race conditions
            try:
                with transaction.atomic():
                    # Lock the slot row for update
                    slot = AvailabilitySlot.objects.select_for_update().get(id=slot_id)
                    
                    # Double-check availability
                    if not slot.is_available:
                        messages.error(request, 'This slot was just booked by another patient.')
                        return redirect('patients:doctor_availability', doctor_id=slot.doctor.id)
                    
                    # Create appointment
                    appointment = Appointment.objects.create(
                        doctor=slot.doctor,
                        patient=request.user,
                        availability_slot=slot,
                        appointment_date=slot.date,
                        appointment_time=slot.start_time,
                        notes=notes
                    )
                    
                    # Mark slot as unavailable
                    slot.is_available = False
                    slot.save()
                    
                    # Create Google Calendar events
                    try:
                        doctor_event_id = create_google_calendar_event(
                            slot.doctor,
                            f"Appointment with {request.user.get_full_name()}",
                            slot.date,
                            slot.start_time,
                            slot.end_time,
                            notes
                        )
                        if doctor_event_id:
                            appointment.google_calendar_event_id_doctor = doctor_event_id
                        
                        patient_event_id = create_google_calendar_event(
                            request.user,
                            f"Appointment with Dr. {slot.doctor.get_full_name()}",
                            slot.date,
                            slot.start_time,
                            slot.end_time,
                            notes
                        )
                        if patient_event_id:
                            appointment.google_calendar_event_id_patient = patient_event_id
                        
                        appointment.save()
                    except Exception as e:
                        print(f"Google Calendar integration failed: {e}")
                        messages.warning(request, 'Appointment created but calendar event failed. Please check your Google Calendar settings.')
                    
                    # Send confirmation emails
                    try:
                        send_booking_confirmation_email(
                            patient_email=request.user.email,
                            doctor_email=slot.doctor.email,
                            patient_name=request.user.get_full_name(),
                            doctor_name=slot.doctor.get_full_name(),
                            appointment_date=str(slot.date),
                            appointment_time=str(slot.start_time)
                        )
                    except Exception as e:
                        print(f"Email sending failed: {e}")
                    
                    messages.success(request, 'Appointment booked successfully!')
                    return redirect('patients:dashboard')
                    
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('patients:doctor_availability', doctor_id=slot.doctor.id)
    else:
        form = BookingForm(initial={'slot_id': slot_id})
    
    context = {
        'form': form,
        'slot': slot,
        'doctor': slot.doctor,
    }
    return render(request, 'appointments/create_booking.html', context)

