import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(event, context):
    """
    AWS Lambda function to send emails
    Supports SIGNUP_WELCOME and BOOKING_CONFIRMATION actions
    """
    try:
        # Parse request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        action = body.get('action')
        to_email = body.get('to')
        
        if not action or not to_email:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Missing required fields: action and to'
                })
            }
        
        # Get SMTP configuration
        smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_user = os.environ.get('SMTP_USER', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        
        if not smtp_user or not smtp_password:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'SMTP credentials not configured'
                })
            }
        
        # Create email based on action
        if action == 'SIGNUP_WELCOME':
            subject, html_content, text_content = create_welcome_email(
                body.get('name', 'User'),
                body.get('role', 'user')
            )
        elif action == 'BOOKING_CONFIRMATION':
            subject, html_content, text_content = create_booking_confirmation_email(
                body.get('patient_name', ''),
                body.get('doctor_name', ''),
                body.get('appointment_date', ''),
                body.get('appointment_time', ''),
                body.get('recipient_type', 'patient')
            )
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': f'Unknown action: {action}'
                })
            }
        
        # Send email
        send_smtp_email(
            smtp_host,
            smtp_port,
            smtp_user,
            smtp_password,
            to_email,
            subject,
            html_content,
            text_content
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Email sent successfully',
                'to': to_email,
                'action': action
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }


def create_welcome_email(name, role):
    """Create welcome email content"""
    role_display = role.title()
    subject = f'Welcome to Hospital Management System - {role_display}'
    
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #667eea;">Welcome to Hospital Management System!</h2>
                <p>Hello {name},</p>
                <p>Thank you for signing up as a {role_display} on our Hospital Management System.</p>
                <p>You can now:</p>
                <ul>
                    {'<li>Set your availability time slots</li><li>Manage your appointments</li><li>View patient bookings</li>' if role == 'doctor' else '<li>Browse available doctors</li><li>Book appointments</li><li>Manage your appointments</li>'}
                </ul>
                <p>If you have any questions, please don't hesitate to contact us.</p>
                <p>Best regards,<br>HMS Team</p>
            </div>
        </body>
    </html>
    """
    
    text_content = f"""
    Welcome to Hospital Management System!
    
    Hello {name},
    
    Thank you for signing up as a {role_display} on our Hospital Management System.
    
    You can now:
    {'- Set your availability time slots\n- Manage your appointments\n- View patient bookings' if role == 'doctor' else '- Browse available doctors\n- Book appointments\n- Manage your appointments'}
    
    If you have any questions, please don't hesitate to contact us.
    
    Best regards,
    HMS Team
    """
    
    return subject, html_content, text_content


def create_booking_confirmation_email(patient_name, doctor_name, appointment_date, appointment_time, recipient_type):
    """Create booking confirmation email content"""
    if recipient_type == 'patient':
        subject = f'Appointment Confirmed with Dr. {doctor_name}'
        greeting = f'Hello {patient_name},'
        main_text = f'Your appointment with Dr. {doctor_name} has been confirmed.'
    else:
        subject = f'New Appointment Booking - {patient_name}'
        greeting = f'Hello Dr. {doctor_name},'
        main_text = f'You have a new appointment booking with {patient_name}.'
    
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #667eea;">Appointment Confirmation</h2>
                <p>{greeting}</p>
                <p>{main_text}</p>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Date:</strong> {appointment_date}</p>
                    <p><strong>Time:</strong> {appointment_time}</p>
                    {'<p><strong>Patient:</strong> ' + patient_name + '</p>' if recipient_type == 'doctor' else '<p><strong>Doctor:</strong> Dr. ' + doctor_name + '</p>'}
                </div>
                <p>Please make sure to be available at the scheduled time.</p>
                <p>Best regards,<br>HMS Team</p>
            </div>
        </body>
    </html>
    """
    
    text_content = f"""
    Appointment Confirmation
    
    {greeting}
    
    {main_text}
    
    Date: {appointment_date}
    Time: {appointment_time}
    {'Patient: ' + patient_name if recipient_type == 'doctor' else 'Doctor: Dr. ' + doctor_name}
    
    Please make sure to be available at the scheduled time.
    
    Best regards,
    HMS Team
    """
    
    return subject, html_content, text_content


def send_smtp_email(smtp_host, smtp_port, smtp_user, smtp_password, to_email, subject, html_content, text_content):
    """Send email via SMTP"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email
    
    # Add both plain text and HTML versions
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')
    
    msg.attach(part1)
    msg.attach(part2)
    
    # Send email
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

