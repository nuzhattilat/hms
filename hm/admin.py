from django.contrib import admin

# Register your models here.
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'dob')
    search_fields = ('name', 'email', 'phone')
