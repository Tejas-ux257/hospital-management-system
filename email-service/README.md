# HMS Email Service

Serverless email service for Hospital Management System using AWS Lambda and Serverless Framework.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure SMTP settings:
   - Copy `.env.example` to `.env`
   - Update SMTP credentials (for Gmail, use App Password)

3. Run locally:
```bash
npm start
# or
serverless offline
```

The service will run on `http://localhost:3000`

## API Endpoint

### POST /dev/send-email

Send an email via the serverless function.

**Request Body:**
```json
{
  "action": "SIGNUP_WELCOME" | "BOOKING_CONFIRMATION",
  "to": "recipient@example.com",
  "name": "User Name",
  "role": "doctor" | "patient",
  "patient_name": "Patient Name",
  "doctor_name": "Doctor Name",
  "appointment_date": "2024-01-15",
  "appointment_time": "10:00:00",
  "recipient_type": "patient" | "doctor"
}
```

**Response:**
```json
{
  "message": "Email sent successfully",
  "to": "recipient@example.com",
  "action": "SIGNUP_WELCOME"
}
```

## Gmail Setup

To use Gmail SMTP:

1. Enable 2-Step Verification on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the generated password in `.env` file

## Deployment

To deploy to AWS:

```bash
serverless deploy
```

Make sure AWS credentials are configured:
```bash
aws configure
```

