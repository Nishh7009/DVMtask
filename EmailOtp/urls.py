from django.urls import path
from . import views

urlpatterns = [
    path('verify/', views.verify_otp_view, name='verify_otp')
]
