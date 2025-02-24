from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_schedules, name='view_schedules'),
    path('edit/<int:schedule_id>', views.edit_schedule, name='edit_schedule'),
    path('add/', views.add_schedule, name='add_schedule'),
]
