# from django.urls import path
# from . import views
# # from . import google_auth

# app_name = 'accounts'

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('signup/doctor/', views.doctor_signup, name='doctor_signup'),
#     path('signup/patient/', views.patient_signup, name='patient_signup'),
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout, name='logout'),
#     # path('google/authorize/', google_auth.google_calendar_authorize, name='google_authorize'),
#     # path('google/callback/', google_auth.google_calendar_callback, name='google_callback'),
# ]

from django.urls import path
from . import views
from . import google_calendar


app_name = 'accounts'

urlpatterns = [
    
    path('', views.home, name='home'),
    path('signup/doctor/', views.doctor_signup, name='doctor_signup'),
    path('signup/patient/', views.patient_signup, name='patient_signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
urlpatterns += [
    path("calendar/authorize/", google_calendar.calendar_authorize, name="calendar_authorize"),
    path("calendar/callback/", google_calendar.calendar_callback, name="calendar_callback"),
]
