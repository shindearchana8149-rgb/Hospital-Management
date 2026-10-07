from django.contrib import admin
from .models import *
from django.utils.html import format_html


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name','department','phone','email','experience','doctor_photo')
    search_fields = ('name','department__name')
    list_filter = ('department',)

    def doctor_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.photo.url))
        return "No Image"


class PatientAdmin(admin.ModelAdmin):
    list_display = ('name','age','gender','phone','patient_photo')
    search_fields = ('name','phone')
    list_filter = ('gender',)

    def patient_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.photo.url))
        return "No Image"


admin.site.register(Department)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment)
admin.site.register(Prescription)