from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/<int:slot_id>/', views.create_booking, name='create_booking'),
]

