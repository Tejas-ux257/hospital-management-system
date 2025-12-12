# Quick Start Guide - Hospital Management System

## 🚀 Quick Setup (5 Minutes)

### 1. Database Setup
```bash
# Create PostgreSQL database
createdb hms_db
# Or use psql:
psql -U postgres
CREATE DATABASE hms_db;
CREATE USER hms_user WITH PASSWORD 'hms_password';
GRANT ALL PRIVILEGES ON DATABASE hms_db TO hms_user;
\q
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
copy .env.example .env  # Windows
# or
cp .env.example .env  # Mac/Linux

# Edit .env with your database credentials
python manage.py migrate
python manage.py runserver
```

### 3. Email Service Setup
```bash
# In a new terminal
cd email-service
npm install
npm start
```

### 4. Access Application
Open browser: `http://localhost:8000`

## 📝 Minimal .env Configuration

**backend/.env:**
```env
SECRET_KEY=django-insecure-change-this
DEBUG=True
DB_NAME=hms_db
DB_USER=hms_user
DB_PASSWORD=hms_password
DB_HOST=localhost
DB_PORT=5432
EMAIL_SERVICE_URL=http://localhost:3000/dev/send-email
```

**email-service/.env:**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## ⚡ Running Both Services

**Terminal 1 (Email Service):**
```bash
cd email-service
npm start
```

**Terminal 2 (Django Backend):**
```bash
cd backend
venv\Scripts\activate  # Windows
python manage.py runserver
```

## 🎯 Test the Application

1. Go to `http://localhost:8000`
2. Sign up as a doctor
3. Add availability slots
4. Sign up as a patient (new browser/incognito)
5. Book an appointment

## 📚 Full Documentation

See `SETUP_GUIDE.md` for complete setup instructions including Google Calendar integration.

