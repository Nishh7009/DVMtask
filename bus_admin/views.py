from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AddSchedule, ChangeSchedule
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from booking_system.models import Schedule
from django.urls import reverse
from datetime import datetime
from booking_system.utils import create_weekly_schedules
# Create your views here.


@user_passes_test(lambda user: user.is_staff, login_url="/login/")
def add_schedule(request):
    if request.method == "POST":
        form = AddSchedule(request.POST, bus=request.user.admin_of)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.bus = request.user.admin_of
            instance.save()
            messages.success(request, "Schedule added successfully!")
    else:
        form = AddSchedule(bus=request.user.admin_of)

    return render(request, 'bus_admin/add_schedule.html', {'form': form})


@user_passes_test(lambda user: user.is_staff, login_url="/login/")
def edit_schedule(request, schedule_id):
    schedule = Schedule.objects.get(pk=schedule_id)
    if request.user.admin_of == schedule.bus:
        if request.method == "POST":
            form = ChangeSchedule(
                request.POST, instance=schedule)
            if form.is_valid():
                form.save()
                messages.success(request, "Schedule updated successfully!")
        else:
            form = ChangeSchedule(instance=schedule)

        return render(request, 'bus_admin/edit_schedule.html', {'form': form})
    elif request.user.admin_of != schedule.bus and schedule.departure_time > datetime.now():
        return HttpResponse('You do not have permission to edit this schedule.')
    elif schedule.departure_time < datetime.now():
        return HttpResponse('Cannot edit past schedules.')


@user_passes_test(lambda user: user.is_staff, login_url="/login/")
def view_schedules(request):
    admin_of = request.user.admin_of
    schedules = Schedule.objects.filter(
        bus=admin_of, departure_time__gte=datetime.now()).order_by('pk')
    entries = []
    for schedule in schedules:
        schedule_id = schedule.pk
        start_stop = schedule.route_segment.start_stop
        end_stop = schedule.route_segment.end_stop
        departure_time = schedule.departure_time
        arrival_time = schedule.arrival_time
        available_capacity = schedule.available_capacity
        price = schedule.price

        entries.append((schedule_id, start_stop, end_stop,
                       departure_time, arrival_time, available_capacity, price))

    if request.method == "POST":
        if request.POST.get('edit_schedule'):
            return redirect(reverse('edit_schedule', args=[int(request.POST.get('edit_schedule'))]))
        if request.POST.get('add_schedule'):
            return redirect(reverse('add_schedule'))
        if request.POST.get('create_next_week_schedules'):
            schedules_created = create_weekly_schedules(admin_of)
            messages.success(
                request, f"{schedules_created} schedules created successfully!")

    return render(request, 'bus_admin/view_schedules.html', {'entries': entries})
