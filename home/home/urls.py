from django.urls import path
from . import views
from booking_system.views import book_bus

urlpatterns = [
    path('', views.home, name='home'),
]
