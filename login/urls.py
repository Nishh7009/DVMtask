from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='index'),
    path('signup/', views.signup, name='signup'),
]
