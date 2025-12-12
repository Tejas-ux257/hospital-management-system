# Complete Setup Guide for Hospital Management System

This guide will walk you through setting up and running the Hospital Management System in VS Code.

## Prerequisites

Before starting, ensure you have the following installed:

1. **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
2. **PostgreSQL** - [Download PostgreSQL](https://www.postgresql.org/download/)
3. **Node.js 16+** - [Download Node.js](https://nodejs.org/)
4. **VS Code** - [Download VS Code](https://code.visualstudio.com/)

## Step 1: Database Setup

### Install PostgreSQL

1. Download and install PostgreSQL from the official website
2. During installation, remember the password you set for the `postgres` user
3. Verify installation by opening Command Prompt/PowerShell and running:
   ```bash
   psql --version
   ```

### Create Database

1. Open PostgreSQL command line or pgAdmin
2. Run the following SQL commands:

```sql
CREATE DATABASE hms_db;
CREATE USER hms_user WITH PASSWORD 'hms_password';
ALTER ROLE hms_user SET client_encoding TO 'utf8';
ALTER ROLE hms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE hms_db TO hms_user;
```

## Step 2: Backend Setup

### Open Project in VS Code

1. Open VS Code
2. File → Open Folder → Select `hospital-management-system` folder

### Create Virtual Environment

1. Open VS Code integrated terminal (Ctrl + ` or View → Terminal)
2. Navigate to backend directory:
   ```bash
   cd backend
   ```

3. Create virtual environment:
   ```bash
   # Windows
   python -m venv venv
   
   # Mac/Linux
   python3 -m venv venv
   ```

4. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

   You should see `(venv)` in your terminal prompt.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

1. In VS Code, create a `.env` file in the `backend` directory
2. Copy contents from `.env.example`:
   ```bash
   # In VS Code terminal
   copy .env.example .env
   ```

3. Edit `.env` file with your actual values:
   ```env
   SECRET_KEY=your-secret-key-change-this-in-production
   DEBUG=True
   DB_NAME=hms_db
   DB_USER=hms_user
   DB_PASSWORD=hms_password
   DB_HOST=localhost
   DB_PORT=5432
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/accounts/google/callback/
   EMAIL_SERVICE_URL=http://localhost:3000/dev/send-email
   ```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

## Step 3: Email Service Setup

### Install Serverless Framework

```bash
npm install -g serverless
npm install -g serverless-offline
```

### Setup Email Service

1. Open a new terminal in VS Code (Terminal → New Terminal)
2. Navigate to email-service directory:
   ```bash
   cd email-service
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Configure SMTP (for Gmail):
   - Create `.env` file in `email-service` directory
   - Add your Gmail credentials:
     ```env
     SMTP_HOST=smtp.gmail.com
     SMTP_PORT=587
     SMTP_USER=your-email@gmail.com
     SMTP_PASSWORD=your-app-password
     ```

   **To get Gmail App Password:**
   1. Enable 2-Step Verification on your Google account
   2. Go to Google Account → Security → 2-Step Verification → App passwords
   3. Generate a password for "Mail"
   4. Use this password in `.env`

## Step 4: Google Calendar API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Calendar API:
   - APIs & Services → Library
   - Search for "Google Calendar API"
   - Click Enable
4. Create OAuth 2.0 credentials:
   - APIs & Services → Credentials
   - Create Credentials → OAuth client ID
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/accounts/google/callback/`
5. Copy Client ID and Client Secret to backend `.env` file

## Step 5: Running the Application

### Terminal 1: Start Email Service

```bash
cd email-service
npm start
```

The email service will run on `http://localhost:3000`

### Terminal 2: Start Django Backend

```bash
cd backend
# Activate venv if not already activated
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

python manage.py runserver
```

The backend will run on `http://localhost:8000`

### Access the Application

1. Open browser and go to: `http://localhost:8000`
2. You should see the home page
3. Sign up as a doctor or patient
4. Start using the system!

## Step 6: VS Code Configuration (Optional)

### Python Interpreter

1. Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
2. Type "Python: Select Interpreter"
3. Choose the virtual environment: `./backend/venv`

### Recommended VS Code Extensions

- Python
- Django
- PostgreSQL
- ESLint (for email service)

## Testing the Application

### Test Doctor Flow

1. Sign up as a doctor
2. Login
3. Go to "Manage Profile" and add specialization
4. Go to "Add Availability" and create time slots
5. View your bookings

### Test Patient Flow

1. Sign up as a patient (in a different browser/incognito)
2. Login
3. Browse doctors
4. View doctor availability
5. Book an appointment
6. Check your appointments

### Test Email Service

The email service should automatically send:
- Welcome email on signup
- Booking confirmation email when appointment is booked

## Troubleshooting

### Database Connection Error

- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists: `psql -U hms_user -d hms_db`

### Port Already in Use

- Change port in `manage.py runserver 8001` or kill the process using port 8000

### Email Service Not Working

- Ensure serverless-offline is running
- Check SMTP credentials in email-service `.env`
- Verify EMAIL_SERVICE_URL in backend `.env` matches

### Google Calendar Not Working

- Verify OAuth credentials are correct
- Check redirect URI matches exactly
- Ensure Google Calendar API is enabled

## Project Structure

```
hospital-management-system/
├── backend/                 # Django backend
│   ├── accounts/           # Authentication app
│   ├── doctors/            # Doctor management
│   ├── patients/           # Patient management
│   ├── appointments/       # Appointment booking
│   ├── hms/                # Project settings
│   ├── templates/          # HTML templates
│   ├── manage.py
│   └── requirements.txt
├── email-service/          # Serverless email service
│   ├── handler.py
│   ├── serverless.yml
│   └── package.json
└── README.md
```

## Next Steps

1. Test all features
2. Customize templates and styling
3. Add more features as needed
4. Deploy to production when ready

## Support

If you encounter any issues, check:
1. All services are running
2. Environment variables are set correctly
3. Database is accessible
4. Ports are not blocked

Happy coding! 🏥

