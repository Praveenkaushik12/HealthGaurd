from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm, DoctorForm, PatientForm,MedicalReport
from django.contrib.auth.models import Group
from PyPDF2 import PdfReader
from .models import MedicalData,Doctor
from django.contrib import messages
#new-Praveen
from django.shortcuts import render, redirect, get_object_or_404
from .models import Request
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest,HttpRequest,HttpResponse




def register_doctor(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            doctor_group = Group.objects.get(name='Doctors')
            doctor_group.user_set.add(user)
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect('login')
    else:
        user_form = UserForm()
        doctor_form = DoctorForm()
    return render(request, 'myapp/register_doctor.html', {'user_form': user_form, 'doctor_form': doctor_form})

def register_patient(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        patient_form = PatientForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            patient_group = Group.objects.get(name='Patients')
            patient_group.user_set.add(user)
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('login')
    else:
        user_form = UserForm()
        patient_form = PatientForm()
    return render(request, 'myapp/register_patient.html', {'user_form': user_form, 'patient_form': patient_form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if hasattr(user, 'doctor'):
                    return redirect('doctor_dashboard')  # URL to doctor's dashboard
                elif hasattr(user, 'patient'):
                    return redirect('patient_dashboard')  # URL to patient's dashboard
            else:
                return render(request, 'myapp/login.html', {'form': form, 'invalid_creds': True})
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})


def home(request):
    return render(request,'myapp/home.html')

def register(request):
    return render(request,'myapp/register.html')

def about(request):
    return render(request,'myapp/about.html')

def contact(request):
    return render(request,'myapp/contact.html')

def submission(request):
    return render(request,'myapp/submission.html')


def doctor_dashboard(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            # Get all accepted requests
            accepted_requests = Request.objects.filter(receiver=request.user.doctor, status='Accepted')
            # Now create a dictionary where each patient is associated with their medical data
            patient_data = {}
            for req in accepted_requests:
                # Assuming that each patient has associated MedicalData
                medical_data = MedicalData.objects.filter(patient=req.sender)
                patient_data[req.sender] = medical_data
            return render(request, 'myapp/doctor_dashboard.html', {
                'patient_data': patient_data
            })
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


#patient_dashboard
def patient_dashboard(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MedicalReport(request.POST, request.FILES)
            if form.is_valid():
                form.instance.patient = request.user.patient
                uploaded_file = form.save()
                pdf_file = uploaded_file.report.path
                try:
                    parsed_text = parse_pdf(pdf_file)
                    save_to_txt(parsed_text)
                    messages.success(request, "Medical report uploaded successfully!")
                    # Redirect to the same view to clear the form
                    return redirect('patient_dashboard')
                   
                except Exception as e:
                    # Handle parsing or saving error
                    error_message = "An error occurred while processing the report."
                    return render(request, 'myapp/patient_dashboard.html', {'form': form, 'error_message': error_message})
        else:
            form = MedicalReport()  # Create a new empty form on GET request
        history = MedicalData.objects.filter(patient=request.user.patient)  # Fetch all medical data
        return render(request, 'myapp/patient_dashboard.html', {'form': form, 'history': history})
    else:
        return redirect('/login/')
  
#patient's panel  
def get_medical_data(request: HttpRequest, id: int) -> HttpResponse:
    med = get_object_or_404(MedicalData, pk=id)
    return render(request, 'myapp/patient_data.html', {'med_data': med})

#delete patient_medical_data
def delete_patient_medical_data(request, id):
    print("called delete_patient_medical_data")
    med = get_object_or_404(MedicalData, pk=id)
    med.delete()
    return redirect('/patient/dashboard/')

#doctor's panel
def show_report(request, username):
    # Retrieve the medical records for the specified user
    username=username
    records = MedicalData.objects.filter(patient__user__username=username)
    return render(request, 'myapp/data_show.html', {'records': records,'user':username})

def parse_pdf(pdf_file):
    with open(pdf_file,'rb') as file:
        reader=PdfReader(file)
        text=''
        for page in reader.pages:
            text+=page.extract_text()
    return text

def save_to_txt(text):
    with open('parsed_text.txt','w') as file:
        file.write(text)


#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')



#---------------------------------------------------------------------------------------------

#new
@login_required
def send_request(request, doctor_id):
    if request.method == 'POST':
        message = request.POST.get('message')
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        if message:
            # Check if the user is a patient
            if hasattr(request.user, 'patient'):
                sender = request.user.patient
                receiver = doctor
                # Create the request object but don't assign it to any variable
                Request.objects.create(sender=sender, receiver=receiver, message=message)
                return redirect('patient_dashboard')  # Redirect to patient dashboard
            else:
                return HttpResponseBadRequest("User is not registered as a patient.")
    return redirect('home')  # Redirect to home page if request fails

def search_doctors(request):
    error_message = None
    doctors = None
    query = None
    
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            doctors = Doctor.objects.filter(specialization__icontains=query)
            if not doctors.exists():
                error_message = 'Doctor not available for this specialization.'
                
    return render(request, 'myapp/search_doctors.html', {'doctors': doctors, 'error_message': error_message, 'query': query})



# def search_doctors(request):
#     if request.method == 'GET':
#         query = request.GET.get('q')
#         if query:
#             doctors = Doctor.objects.filter(specialization__icontains=query)
#             return render(request, 'myapp/search_doctors.html', {'doctors': doctors})
#     return render(request, 'myapp/search_doctors.html', {})



def view_requests(request):
    if request.user.is_authenticated and hasattr(request.user, 'doctor'):
        requests = Request.objects.filter(receiver=request.user.doctor)
        return render(request, 'myapp/view_requests.html', {'requests': requests})
    else:
        return redirect('home')  # Redirect if not authenticated or not a doctor

def manage_request(request, request_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        request_obj = get_object_or_404(Request, pk=request_id)
        if action == 'accept':
            request_obj.status = 'Accepted'
            patient_username = request_obj.sender.user.username  # Get patient's username
            request_obj.patient_username = patient_username  # Update request with patient's username
            # Add any additional actions you want to perform when accepting a request
        elif action == 'reject':
            request_obj.status = 'Rejected'
            # Add any additional actions you want to perform when rejecting a request
        request_obj.save()
        return redirect('doctor_dashboard')  # Redirect to doctor dashboard
    return redirect('home')  # Redirect if method is not POST

def doctor_already_requested(patient, doctor):
    return Request.objects.filter(sender=patient, receiver=doctor).exists()

