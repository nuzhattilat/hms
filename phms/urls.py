from django.contrib import admin
from django.urls import path
from hm import views
from hm.views import hms
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',hms),
    #path('home/',hms)
    path('register/', views.register, name='register'),
    path('patient/', views.patient, name='patient'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('doc_register/', views.doc_register, name='doc_register'),
    path('doc_login/', views.doc_login, name='doc_login'),
    path('doc_profile/', views.doc_profile, name='doc_profile'),
    #path('doc_logout/', views.doc_logout, name='doc_logout'),
    path('doctor/', views.doctor_page, name='doctor'),

]
