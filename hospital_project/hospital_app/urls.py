from django.urls import path
from . import views

urlpatterns = [
path('', views.home, name='home'),  # Home page
path('patient/register/',views.patient_register,name="patient_register"),
path('patient/login/',views.patient_login,name="patient_login"),
path('patient/dashboard/',views.patient_dashboard,name="patient_dashboard"),
path('patient/logout/',views.patient_logout,name="patient_logout"),
path('patient/book-appointment/',views.book_appointment,name="book_appointment"),
path('patient/my-appointments/',views.my_appointments,name="my_appointments"),
path('patient/prescriptions/',views.patient_prescriptions,name="patient_prescriptions"),
path('doctor/login/',views.doctor_login,name="doctor_login"),
path('doctor/dashboard/',views.doctor_dashboard,name="doctor_dashboard"),
path('doctor/logout/',views.doctor_logout,name="doctor_logout"),
path('doctor/appointments/',views.doctor_appointments,name="doctor_appointments"),
path('doctor/add-prescription/<int:id>/',views.add_prescription,name="add_prescription"),
path('doctor/patients/',views.doctor_patients),
path('doctor/prescriptions/',views.doctor_prescriptions),
path('doctor/profile/',views.doctor_profile),
path('doctor/chat/<int:patient_id>/',views.doctor_chat),
path('patient/chat/<int:doctor_id>/',views.patient_chat),
]