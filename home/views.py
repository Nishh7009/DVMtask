from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import HomeForm
from booking_system.models import Schedule, Route, Bus


def home(request):

    entries = None

    if request.method == "POST":
        form = HomeForm(request.POST)
        if form.is_valid():
            arrival = form.cleaned_data.get("arrival")
            destination = form.cleaned_data.get("destination")
            date = form.cleaned_data.get("date")

            try:
                route_id = Route.objects.get(
                    arrival=arrival, destination=destination).pk

                schedule_entry = Schedule.objects.filter(
                    route=route_id, arrival_time__date=date)

                total_records = len(list(schedule_entry))

                bus_ids = list(schedule_entry.values_list('bus', flat=True))

                schedule_ids = list(
                    schedule_entry.values_list('pk', flat=True))

                departure_times = list(
                    schedule_entry.values_list('departure_time', flat=True))

                arrival_times = list(
                    schedule_entry.values_list('arrival_time', flat=True))

                trip_duration = [arrival_times[i] - departure_times[i]
                                 for i in range(total_records)]

                buses = [list(Bus.objects.filter(pk=i).values_list('bus_name', flat=True))[0]
                         for i in bus_ids]

                entries = list(zip(buses, trip_duration, schedule_ids))

            except Route.DoesNotExist or Schedule.DoesNotExist:
                entries = []

    else:
        form = HomeForm()

    return render(request, 'home/home.html', {"form": form,
                                              "entries": entries, })
