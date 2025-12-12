# How to Run the Project in VS Code

## Step-by-Step Instructions

### 1. Open Project in VS Code

1. Open Visual Studio Code
2. Click **File** → **Open Folder**
3. Navigate to and select the `hospital-management-system` folder
4. Click **Select Folder**

### 2. Setup Python Environment

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to open command palette
2. Type "Python: Select Interpreter"
3. If you see the venv, select it. Otherwise:
   - Click "Enter interpreter path..."
   - Navigate to `backend/venv/Scripts/python.exe` (Windows) or `backend/venv/bin/python` (Mac/Linux)

### 3. Install Python Dependencies

1. Open integrated terminal: `Ctrl+` ` (backtick) or View → Terminal
2. Navigate to backend:
   ```bash
   cd backend
   ```
3. Create virtual environment (if not exists):
   ```bash
   python -m venv venv
   ```
4. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```
5. Install packages:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Setup Database

1. Ensure PostgreSQL is installed and running
2. Create database (see SETUP_GUIDE.md for details)
3. Create `.env` file in `backend` directory:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=hms_db
   DB_USER=hms_user
   DB_PASSWORD=hms_password
   DB_HOST=localhost
   DB_PORT=5432
   EMAIL_SERVICE_URL=http://localhost:3000/dev/send-email
   ```

### 5. Run Database Migrations

In the VS Code terminal (with venv activated):
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 6. Setup Email Service

1. Open a **new terminal** in VS Code: Terminal → New Terminal
2. Navigate to email-service:
   ```bash
   cd email-service
   ```
3. Install Node.js dependencies:
   ```bash
   npm install
   ```
4. Create `.env` file in `email-service` directory:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

### 7. Run Both Services

You need **two terminals** running simultaneously:

#### Terminal 1: Email Service
```bash
cd email-service
npm start
```
You should see: `Serverless: Starting Offline: dev/us-east-1`

#### Terminal 2: Django Backend
```bash
cd backend
venv\Scripts\activate  # Windows (or source venv/bin/activate on Mac/Linux)
python manage.py runserver
```
You should see: `Starting development server at http://127.0.0.1:8000/`

### 8. Access the Application

1. Open your web browser
2. Navigate to: `http://localhost:8000`
3. You should see the Hospital Management System home page

## Using VS Code Debugger

### Debug Django Server

1. Go to Run and Debug panel (Ctrl+Shift+D)
2. Select "Django: Run Server" from dropdown
3. Click the green play button or press F5
4. Set breakpoints in your Python files
5. The debugger will pause at breakpoints

## VS Code Tips

### Multiple Terminals

- Click the **+** button in terminal panel to open new terminal
- Use dropdown to switch between terminals
- Right-click terminal tab to rename (e.g., "Email Service", "Django")

### Python Extension

Install the Python extension for:
- Syntax highlighting
- IntelliSense
- Debugging
- Linting

### Recommended Extensions

1. **Python** (by Microsoft)
2. **Django** (by Baptiste Darthenay)
3. **PostgreSQL** (by Chris Kolkman)
4. **ESLint** (for email service)

## Troubleshooting

### Port Already in Use

If port 8000 is busy:
```bash
python manage.py runserver 8001
```

### Database Connection Error

- Check PostgreSQL is running
- Verify `.env` credentials
- Test connection: `psql -U hms_user -d hms_db`

### Module Not Found

- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

### Email Service Not Starting

- Check Node.js is installed: `node --version`
- Reinstall dependencies: `npm install`
- Check port 3000 is available

## Quick Commands Reference

```bash
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Django
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Email Service
cd email-service
npm start
```

## Project Structure in VS Code

```
hospital-management-system/
├── backend/
│   ├── accounts/          ← Authentication
│   ├── doctors/           ← Doctor features
│   ├── patients/          ← Patient features
│   ├── appointments/      ← Booking system
│   ├── templates/          ← HTML templates
│   └── manage.py
├── email-service/
│   ├── handler.py         ← Lambda function
│   └── serverless.yml     ← Serverless config
└── README.md
```

Happy coding! 🚀

