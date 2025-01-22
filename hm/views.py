from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from .models import Patient
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Doctor
from django.contrib.auth.hashers import make_password, check_password

def hms(request):
    return render(request,'home.html')
    #return HttpResponse("<h1>Welcome hms</h1>")

def doctor_page(request):
    
    return render(request, 'doctor.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        symptoms = request.POST.get('symptoms')
        previous_medications = request.POST.get('previous_medications')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        emergency_contact = request.POST.get('emergency_contact')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        # Save to database
        try:
            patient = Patient(
                name=name,
                dob=dob,
                symptoms=symptoms,
                previous_medications=previous_medications,
                phone=phone,
                email=email,
                emergency_contact=emergency_contact,
                password=password  # In production, use password hashing
            )
            patient.save()
            messages.success(request, "Registration successful!")
            return redirect('/')  # Redirect to home page after registration
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')


def patient(request):
    if 'loggedIn' in request.session:  # Check if the session contains logged-in patient data
        patient = request.session.get('loggedIn')  # Retrieve patient data from the session
        return render(request, 'patient.html', {'patient': patient})  # Render patient information
    else:
        return redirect('login')  # Redirect to login if not logged in

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Get the data from the request
        patient_data = data.get('patient')  # Extract the patient data
        
        # Store the patient data in the session
        request.session['loggedIn'] = patient_data
        
        # Return a success message
        return JsonResponse({'message': 'Login successful'}, status=200)

    # If GET request, render the login page
    return render(request, 'login.html')

def logout_view(request):
    try:
        del request.session['loggedIn']  # Clear the logged-in user from the session
    except KeyError:
        pass
    return redirect('login')  # Redirect to login page after logout


# Doctor Registration View
def doc_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        dob = request.POST.get('dob')
        specialization = request.POST.get('specialization')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'doc_register.html')

        password = make_password(password)

        Doctor.objects.create(
            name=name,
            email=email,
            password=password,
            dob=dob,
            specialization=specialization
        )

        messages.success(request, "Doctor registered successfully!")
        return redirect('doc_login')

    return render(request, 'doc_register.html')

# Doctor Login View
def doc_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            doctor = Doctor.objects.get(email=email)
            if check_password(password, doctor.password):
                request.session['doctor_logged_in'] = doctor.id
                return redirect('doc_profile')
            else:
                messages.error(request, "Invalid email or password.")
        except Doctor.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, 'doc_login.html')

# Doctor Profile View
def doc_profile(request):
    if 'doctor_logged_in' not in request.session:
        return redirect('doc_login')

    doctor_id = request.session['doctor_logged_in']
    doctor = Doctor.objects.get(id=doctor_id)

    return render(request, 'doc_profile.html', {'doctor': doctor})

# Doctor Logout View
def logout(request):
    if 'doctor_logged_in' in request.session:
        del request.session['doctor_logged_in']
    return redirect('home')