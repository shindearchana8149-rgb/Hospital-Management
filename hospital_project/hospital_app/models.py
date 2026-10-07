from django.db import models

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# Doctor Model
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='doctor_photos/')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    qualification = models.CharField(max_length=200)
    experience = models.IntegerField()

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
      
      
class Patient(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='patient_photos/')
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
      
      
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return self.patient.name
      


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medicine = models.TextField()
    notes = models.TextField()
    next_visit = models.DateField()

    def __str__(self):
        return self.appointment.patient.name

class Message(models.Model):

    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)

    sender = models.CharField(max_length=20) # doctor / patient
    message = models.TextField()

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message