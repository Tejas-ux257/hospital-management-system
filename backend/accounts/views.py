from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import DoctorSignUpForm, PatientSignUpForm, LoginForm
from .services import send_welcome_email


def home(request):
    """Home page"""
    if request.user.is_authenticated:
        if request.user.is_doctor():
            return redirect('doctors:dashboard')
        elif request.user.is_patient():
            return redirect('patients:dashboard')
    return render(request, 'accounts/home.html')


@require_http_methods(["GET", "POST"])
def doctor_signup(request):
    """Doctor registration"""
    if request.user.is_authenticated:
        return redirect('doctors:dashboard')
    
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            # Send welcome email
            try:
                send_welcome_email(user.email, user.first_name, 'doctor')
            except Exception as e:
                print(f"Email sending failed: {e}")
            return redirect('accounts:login')
    else:
        form = DoctorSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'role': 'doctor'})


@require_http_methods(["GET", "POST"])
def patient_signup(request):
    """Patient registration"""
    if request.user.is_authenticated:
        return redirect('patients:dashboard')
    
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            # Send welcome email
            try:
                send_welcome_email(user.email, user.first_name, 'patient')
            except Exception as e:
                print(f"Email sending failed: {e}")
            return redirect('accounts:login')
    else:
        form = PatientSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'role': 'patient'})


@require_http_methods(["GET", "POST"])
def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        if request.user.is_doctor():
            return redirect('doctors:dashboard')
        elif request.user.is_patient():
            return redirect('patients:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_doctor():
                    return redirect('doctors:dashboard')
                elif user.is_patient():
                    return redirect('patients:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """User logout"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

