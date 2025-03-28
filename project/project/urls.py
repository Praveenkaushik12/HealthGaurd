"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('register/patient/', views.register_patient, name='register_patient'),
    # Assuming you have a login view set up:
    path('',views.home,name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.user_logout,name="logout"),
    path('register/', views.register, name='register'),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    
    path('doctor/dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('patient/dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('data/<int:id>',views.get_medical_data,name='get_medical_data'),
    path('delete/<int:id>',views.delete_patient_medical_data,name='delete_patient_medical_data'),
    path('show_report/<str:username>/',views.show_report, name='show_report'),
    
     #new-Praveen
     
    path('search/doctors/', views.search_doctors, name='search_doctors'),
    path('send/request/<int:doctor_id>/', views.send_request, name='send_request'),
    path('view/requests/', views.view_requests, name='view_requests'),
    path('manage/request/<int:request_id>/', views.manage_request, name='manage_request'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
