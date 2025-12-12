from django.urls import path
from . import views


app_name = 'doctors'

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='dashboard'),
    path('profile/', views.manage_profile, name='manage_profile'),
    path('availability/', views.availability_list, name='availability_list'),
    path('availability/create/', views.create_availability, name='create_availability'),
    path('availability/<int:slot_id>/delete/', views.delete_availability, name='delete_availability'),
    path('bookings/', views.view_bookings, name='view_bookings'),
]

