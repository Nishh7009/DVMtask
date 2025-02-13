from django.urls import path
from . import views

urlpatterns = [
    path('<int:schedule_id>/', views.book_bus, name='book_bus'),
]
