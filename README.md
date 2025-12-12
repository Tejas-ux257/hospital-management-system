# Mini Hospital Management System (HMS)

A comprehensive hospital management web application focused on doctor availability and patient appointment booking, with Google Calendar integration and serverless email notifications.

## Features

- **User Authentication**: Sign up and login for doctors and patients with role-based access
- **Doctor Dashboard**: Manage availability time slots
- **Patient Dashboard**: View doctors and book appointments
- **Appointment Booking**: Secure booking system with race condition handling
- **Google Calendar Integration**: Automatic calendar event creation for appointments
- **Email Notifications**: Serverless email service for welcome and booking confirmation emails

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL
- **Authentication**: Django session-based authentication
- **Email Service**: AWS Lambda (Serverless Framework)
- **Calendar Integration**: Google Calendar API

## Project Structure

```
hospital-management-system/
├── backend/                 # Django backend
│   ├── hms/               # Main project settings
│   ├── accounts/          # User authentication app
│   ├── doctors/           # Doctor management app
│   ├── patients/          # Patient management app
│   ├── appointments/      # Appointment booking app
│   └── manage.py
├── email-service/          # Serverless email service
│   ├── handler.py         # Lambda function handler
│   └── serverless.yml     # Serverless configuration
└── README.md
```

## Prerequisites

- Python 3.9+
- PostgreSQL (installed locally)
- Node.js 16+ (for Serverless Framework)
- Google Cloud Platform account (for Calendar API)
- AWS account (optional, for Lambda deployment)

## Installation & Setup

### 1. Clone and Navigate to Project

```bash
cd hospital-management-system
```

### 2. Set Up Python Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

1. Install PostgreSQL from https://www.postgresql.org/download/
2. Create a new database:

```sql
CREATE DATABASE hms_db;
CREATE USER hms_user WITH PASSWORD 'hms_password';
ALTER ROLE hms_user SET client_encoding TO 'utf8';
ALTER ROLE hms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE hms_db TO hms_user;
```

### 5. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
DATABASE_URL=postgresql://hms_user:hms_password@localhost:5432/hms_db
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
EMAIL_SERVICE_URL=http://localhost:3000/dev/send-email
```

### 6. Run Database Migrations

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional: create admin user
```

### 7. Set Up Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials
5. Add credentials to `.env` file

### 8. Set Up Email Service (Serverless)

```bash
# Install Serverless Framework globally
npm install -g serverless

# Install serverless-offline plugin
npm install -g serverless-offline

# Navigate to email-service directory
cd email-service

# Install dependencies
npm install

# For local development, run:
serverless offline
```

The email service will run on `http://localhost:3000`

### 9. Run the Django Development Server

```bash
cd backend
python manage.py runserver
```

The backend will run on `http://localhost:8000`

## Usage Guide

### Creating User Accounts

1. **Doctor Sign Up**:
   - Navigate to `http://localhost:8000/accounts/signup/doctor/`
   - Fill in the registration form
   - After signup, you'll be redirected to doctor dashboard

2. **Patient Sign Up**:
   - Navigate to `http://localhost:8000/accounts/signup/patient/`
   - Fill in the registration form
   - After signup, you'll be redirected to patient dashboard

### Doctor Workflow

1. **Login**: `http://localhost:8000/accounts/login/`
2. **Set Availability**:
   - Go to "Manage Availability" in dashboard
   - Select date and time slots
   - Save availability slots
3. **View Bookings**: See all appointments booked with you

### Patient Workflow

1. **Login**: `http://localhost:8000/accounts/login/`
2. **Browse Doctors**: View list of available doctors
3. **Book Appointment**:
   - Select a doctor
   - Choose date and available time slot
   - Confirm booking
4. **View Appointments**: See all your booked appointments

### Google Calendar Integration

1. When booking an appointment, both doctor and patient need to:
   - Authorize the app to access their Google Calendar
   - Grant necessary permissions
2. After authorization, appointments are automatically added to both calendars

## API Endpoints

### Authentication
- `POST /accounts/signup/doctor/` - Doctor registration
- `POST /accounts/signup/patient/` - Patient registration
- `POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout

### Doctor
- `GET /doctors/dashboard/` - Doctor dashboard
- `GET /doctors/availability/` - List availability slots
- `POST /doctors/availability/create/` - Create availability slot
- `DELETE /doctors/availability/<id>/delete/` - Delete availability slot
- `GET /doctors/bookings/` - View bookings

### Patient
- `GET /patients/dashboard/` - Patient dashboard
- `GET /patients/doctors/` - List all doctors
- `GET /patients/doctors/<id>/availability/` - View doctor availability
- `POST /patients/bookings/create/` - Create booking
- `GET /patients/bookings/` - View patient bookings

### Email Service
- `POST /dev/send-email` - Send email (serverless function)

## Testing

```bash
cd backend
python manage.py test
```

## Deployment

### Backend Deployment
- Use platforms like Heroku, AWS Elastic Beanstalk, or DigitalOcean
- Update `ALLOWED_HOSTS` in settings.py
- Set production environment variables

### Email Service Deployment
```bash
cd email-service
serverless deploy
```

## Demo Recording

Create a 10-minute screen recording showcasing:
1. Doctor signup and login
2. Setting availability slots
3. Patient signup and login
4. Browsing doctors and booking appointment
5. Google Calendar integration
6. Email notifications
7. Code walkthrough of key features

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

### Google Calendar API Issues
- Verify OAuth credentials are correct
- Check API is enabled in Google Cloud Console
- Ensure redirect URIs are configured

### Email Service Issues
- Ensure serverless-offline is running
- Check EMAIL_SERVICE_URL in backend `.env`
- Verify SMTP credentials (if using Gmail)

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please open an issue in the repository.

