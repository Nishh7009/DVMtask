from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_bus, name='book_bus'),
]
