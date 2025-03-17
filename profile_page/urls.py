from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="profile_page"),
    path('wallet/', views.wallet, name="wallet"),
    path('bookings/', views.bookings, name="user_bookings"),
    path('view_details/<int:booking_id>',
         views.booking_details, name="booking_details"),
    path('edit_passengers/<int:booking_id>',
         views.edit_passenger_details, name='edit_passengers')
]
