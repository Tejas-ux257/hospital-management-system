# 10-Minute Demo Script

## Pre-Demo Setup (Before Recording)

1. Ensure PostgreSQL is running
2. Start email service: `cd email-service && npm start`
3. Start Django: `cd backend && python manage.py runserver`
4. Have Gmail credentials ready (for email service)
5. Have Google OAuth credentials ready (for Calendar)

## Demo Flow (10 Minutes)

### Minute 1: Introduction & Project Overview (0:00 - 1:00)

**Say:**
"Today I'll demonstrate a complete Hospital Management System built with Django and PostgreSQL. The system allows doctors to manage their availability and patients to book appointments, with email notifications and Google Calendar integration."

**Show:**
- Project structure in VS Code
- Key files: models.py, views.py, templates
- Database models diagram (if available)

### Minute 2: Doctor Signup & Dashboard (1:00 - 2:00)

**Actions:**
1. Navigate to `http://localhost:8000`
2. Click "Doctor Sign Up"
3. Fill form:
   - Username: `dr_smith`
   - Email: `dr.smith@example.com`
   - First Name: `John`
   - Last Name: `Smith`
   - Password: `securepass123`
4. Submit form
5. Show success message
6. Login as doctor
7. Show doctor dashboard

**Say:**
"Here we have the doctor dashboard where doctors can manage their profile, set availability, and view bookings."

### Minute 3: Doctor Profile & Availability (2:00 - 3:00)

**Actions:**
1. Click "Manage Profile"
2. Add:
   - Specialization: `Cardiology`
   - Bio: `Experienced cardiologist with 10 years of practice`
   - Years of Experience: `10`
3. Save profile
4. Go to "Add Availability"
5. Create 3-4 availability slots:
   - Tomorrow, 10:00 AM - 11:00 AM
   - Tomorrow, 2:00 PM - 3:00 PM
   - Day after tomorrow, 9:00 AM - 10:00 AM
6. Show availability list

**Say:**
"Doctors can set their availability slots. These slots are visible to patients and can be booked."

### Minute 4: Patient Signup & Browsing (3:00 - 4:00)

**Actions:**
1. Open new browser/incognito window
2. Navigate to `http://localhost:8000`
3. Click "Patient Sign Up"
4. Fill form:
   - Username: `patient_jane`
   - Email: `jane@example.com`
   - First Name: `Jane`
   - Last Name: `Doe`
   - Password: `securepass123`
5. Login as patient
6. Show patient dashboard
7. Click "Browse Doctors"
8. Show doctor list with Dr. Smith

**Say:**
"Patients can browse available doctors and see their specializations."

### Minute 5: Booking Appointment (4:00 - 5:00)

**Actions:**
1. Click "View Availability" for Dr. Smith
2. Show available slots
3. Click "Book Appointment" on a slot
4. Add notes: `Follow-up appointment for heart checkup`
5. Confirm booking
6. Show success message
7. Go back to doctor dashboard (first browser)
8. Show the booking appears in doctor's bookings

**Say:**
"When a patient books an appointment, the slot is immediately marked as unavailable, preventing double-booking. The system uses database transactions to handle race conditions."

### Minute 6: Email Notifications (5:00 - 6:00)

**Actions:**
1. Check email service terminal/logs
2. Show email was sent (if configured)
3. Explain email service structure:
   - Open `email-service/handler.py`
   - Show SIGNUP_WELCOME and BOOKING_CONFIRMATION actions
   - Show serverless.yml configuration

**Say:**
"The system uses a serverless email service that can be deployed to AWS Lambda. It sends welcome emails on signup and confirmation emails when appointments are booked."

### Minute 7: Google Calendar Integration (6:00 - 7:00)

**Actions:**
1. Show "Connect Google Calendar" button on dashboard
2. Click it (if credentials configured)
3. Show OAuth flow
4. Explain calendar event creation:
   - Open `appointments/services.py`
   - Show `create_google_calendar_event` function
   - Explain how events are created for both doctor and patient

**Say:**
"When Google Calendar is connected, appointments are automatically added to both the doctor's and patient's calendars."

### Minute 8: Code Walkthrough - Models (7:00 - 8:00)

**Show:**
1. `accounts/models.py` - Custom User model with roles
2. `doctors/models.py` - DoctorProfile and AvailabilitySlot
3. `appointments/models.py` - Appointment model with relationships

**Say:**
"The database models use proper relationships - one-to-one for profiles, foreign keys for appointments, and unique constraints to prevent double-booking."

### Minute 9: Code Walkthrough - Views & Race Conditions (8:00 - 9:00)

**Show:**
1. `appointments/views.py` - Booking creation view
2. Highlight database transaction:
   ```python
   with transaction.atomic():
       slot = AvailabilitySlot.objects.select_for_update().get(id=slot_id)
   ```
3. Explain race condition prevention

**Say:**
"The booking system uses database transactions with row-level locking to prevent race conditions when multiple users try to book the same slot simultaneously."

### Minute 10: Summary & Features (9:00 - 10:00)

**Summarize:**
1. Authentication with role-based access
2. Doctor availability management
3. Patient appointment booking
4. Email notifications via serverless service
5. Google Calendar integration
6. Race condition handling
7. Modern, responsive UI

**Show:**
- Project structure one more time
- Key features checklist
- How to run the project

**Say:**
"This Hospital Management System demonstrates a complete web application with authentication, database management, external API integration, and serverless services. All code is production-ready and follows Django best practices."

## Key Points to Emphasize

1. ✅ **Complete CRUD operations** for all entities
2. ✅ **Security**: Password hashing, CSRF protection, role-based access
3. ✅ **Race condition handling** with database transactions
4. ✅ **Email service** using serverless architecture
5. ✅ **Google Calendar integration** for convenience
6. ✅ **Clean code structure** following Django best practices
7. ✅ **Comprehensive documentation** for easy setup

## Tips for Recording

- **Speak clearly** and at a moderate pace
- **Show code** while explaining concepts
- **Demonstrate features** rather than just talking about them
- **Highlight key technical decisions** (transactions, serverless, etc.)
- **Keep it under 10 minutes** - edit if needed
- **Use screen annotations** if possible to highlight important parts

## Post-Demo

- Upload video to YouTube/Vimeo
- Share link in project README
- Include timestamp breakdown if helpful

---

**Good luck with your demo! 🎥**

