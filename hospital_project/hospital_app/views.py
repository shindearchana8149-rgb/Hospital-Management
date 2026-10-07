from django.shortcuts import render,redirect
from .models import *
from django.shortcuts import render

def home(request):
    return render(request, 'doctor/home.html')
def patient_dashboard(request):

    if 'patient_id' not in request.session:
        return redirect('patient_login')

    patient = Patient.objects.get(id=request.session['patient_id'])

    return render(request,'patient/dashboard.html',{'patient':patient})


def patient_register(request):

    if request.method == "POST":

        name = request.POST.get('name')
        photo = request.FILES.get('photo')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        username = request.POST.get('username')
        password = request.POST.get('password')

        Patient.objects.create(
            name=name,
            photo=photo,
            age=age,
            gender=gender,
            phone=phone,
            address=address,
            username=username,
            password=password
        )

        return redirect('patient_login')

    return render(request,'patient/register.html')
  
  
def patient_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            patient = Patient.objects.get(username=username,password=password)

            request.session['patient_id'] = patient.id

            return redirect('patient_dashboard')

        except:
            return render(request,'patient/login.html',{'error':'Invalid Login'})

    return render(request,'patient/login.html')
  
  
def patient_logout(request):
    request.session.flush()
    return redirect('patient_login')
  
  
def book_appointment(request):

    if 'patient_id' not in request.session:
        return redirect('patient_login')

    doctors = Doctor.objects.all()

    if request.method == "POST":

        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')

        patient = Patient.objects.get(id=request.session['patient_id'])
        doctor = Doctor.objects.get(id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time,
            status="Pending"
        )

        return redirect('patient_dashboard')

    return render(request,'patient/book_appointment.html',{'doctors':doctors})
  
  
def my_appointments(request):

    if 'patient_id' not in request.session:
        return redirect('patient_login')

    patient = Patient.objects.get(id=request.session['patient_id'])

    appointments = Appointment.objects.filter(patient=patient)

    return render(request,'patient/my_appointments.html',
    {'appointments':appointments})
    
    
def doctor_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            doctor = Doctor.objects.get(username=username,password=password)

            request.session['doctor_id'] = doctor.id

            return redirect('doctor_dashboard')

        except:
            return render(request,'doctor/login.html',
            {'error':'Invalid Username or Password'})

    return render(request,'doctor/login.html')
  
def doctor_logout(request):
    request.session.flush()
    return redirect('doctor_login')
  
  
def doctor_dashboard(request):

    if 'doctor_id' not in request.session:
        return redirect('doctor_login')

    doctor = Doctor.objects.get(id=request.session['doctor_id'])

    return render(request,'doctor/dashboard.html',{'doctor':doctor})

def doctor_appointments(request):

    if 'doctor_id' not in request.session:
        return redirect('doctor_login')

    doctor = Doctor.objects.get(id=request.session['doctor_id'])

    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request,'doctor/appointments.html',
    {'appointments':appointments})
    
    
def add_prescription(request, id):

    if 'doctor_id' not in request.session:
        return redirect('doctor_login')

    appointment = Appointment.objects.get(id=id)

    if request.method == "POST":

        diagnosis = request.POST.get('diagnosis')
        medicine = request.POST.get('medicine')
        notes = request.POST.get('notes')
        next_visit = request.POST.get('next_visit')

        Prescription.objects.create(
            appointment=appointment,
            diagnosis=diagnosis,
            medicine=medicine,
            notes=notes,
            next_visit=next_visit
        )

        appointment.status = "Completed"
        appointment.save()

        return redirect('doctor_appointments')

    return render(request,'doctor/add_prescription.html')
  
  
def patient_prescriptions(request):

    if 'patient_id' not in request.session:
        return redirect('patient_login')

    patient = Patient.objects.get(id=request.session['patient_id'])

    prescriptions = Prescription.objects.filter(
        appointment__patient=patient
    )

    return render(request,'patient/prescriptions.html',
    {'prescriptions':prescriptions})
    
    
from django.shortcuts import render
from hospital_app.models import Appointment

def doctor_patients(request):

    doctor = request.session['doctor_id']

    patients = Appointment.objects.filter(
        doctor_id=doctor
    ).select_related('patient')

    return render(request,'doctor/patients.html',{'patients':patients})

from hospital_app.models import Prescription

def doctor_prescriptions(request):

    doctor = request.session['doctor_id']

    prescriptions = Prescription.objects.filter(
        appointment__doctor_id=doctor
    )

    return render(request,'doctor/prescriptions.html',{
        'prescriptions':prescriptions
    })
    
def doctor_profile(request):

    doctor = Doctor.objects.get(
        id=request.session['doctor_id']
    )

    if request.method == "POST":

        doctor.name = request.POST['name']
        doctor.department = request.POST['department']

        if request.FILES.get('photo'):
            doctor.photo = request.FILES['photo']

        doctor.save()

    return render(request,'doctor/profile.html',{
        'doctor':doctor
    })
    
def doctor_dashboard(request):

    doctor = Doctor.objects.get(
        id=request.session['doctor_id']
    )

    total_patients = Appointment.objects.filter(
        doctor=doctor
    ).count()

    pending = Appointment.objects.filter(
        doctor=doctor,
        status="Pending"
    ).count()

    approved = Appointment.objects.filter(
        doctor=doctor,
        status="Approved"
    ).count()

    completed = Appointment.objects.filter(
        doctor=doctor,
        status="Completed"
    ).count()

    return render(request,'doctor/dashboard.html',{
        'doctor':doctor,
        'total_patients':total_patients,
        'pending':pending,
        'approved':approved,
        'completed':completed
    })
    
def doctor_chat(request,patient_id):

    doctor = Doctor.objects.get(id=request.session['doctor_id'])
    patient = Patient.objects.get(id=patient_id)

    messages = Message.objects.filter(
        doctor=doctor,
        patient=patient
    ).order_by('date')

    if request.method == "POST":

        msg = request.POST.get('message')

        Message.objects.create(
            doctor=doctor,
            patient=patient,
            sender="doctor",
            message=msg
        )

        return redirect(f'/doctor/chat/{patient_id}/')

    return render(request,'doctor/chat.html',{
        'messages':messages,
        'patient':patient
    })
    
def patient_chat(request,doctor_id):

    patient = Patient.objects.get(id=request.session['patient_id'])
    doctor = Doctor.objects.get(id=doctor_id)

    messages = Message.objects.filter(
        doctor=doctor,
        patient=patient
    ).order_by('date')

    if request.method == "POST":

        msg = request.POST.get('message')

        Message.objects.create(
            doctor=doctor,
            patient=patient,
            sender="patient",
            message=msg
        )

        return redirect(f'/patient/chat/{doctor_id}/')

    return render(request,'patient/chat.html',{
        'messages':messages,
        'doctor':doctor
    })