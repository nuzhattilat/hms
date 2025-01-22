from django.db import models

# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    symptoms = models.TextField()
    previous_medications = models.TextField(blank=True, null=True)  # Optional
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    emergency_contact = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.name




class Doctor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return self.name
