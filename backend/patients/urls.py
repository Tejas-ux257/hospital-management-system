from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='dashboard'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:doctor_id>/availability/', views.doctor_availability, name='doctor_availability'),
    path('appointments/', views.view_appointments, name='view_appointments'),
]

