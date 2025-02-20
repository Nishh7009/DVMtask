from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_bus, name='book_bus'),
    path('<int:schedule_id>/?count=<int:count>',
         views.passenger_details, name='passenger_details')
]
