from django.urls import path
from . import views

urlpatterns = [
    path('', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('logout/', views.logout_view, name='logout')
]
