from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="profile_page"),
    path('wallet/', views.wallet, name="wallet"),
    path('bookings/', views.bookings, name="user_bookings")
]
