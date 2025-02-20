from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import HomeForm
from .utils import find_buses


def home(request):

    entries = None

    if request.method == "POST":
        form = HomeForm(request.POST)
        if request.POST.get('book_bus'):
            price = int(request.POST.get('book_bus').split('-')[-1])
            schedule_ids = [int(i) for i in request.POST.get(
                'book_bus').split('-')[0][1:-1].split(",")]
            booking_data = {"price": price, "schedule_ids": schedule_ids}
            request.session['booking_data'] = booking_data
            return redirect('/book_bus/')
        if form.is_valid():
            start_stop = form.cleaned_data.get("start_stop")
            end_stop = form.cleaned_data.get("end_stop")
            date = form.cleaned_data.get("date")

            entries = find_buses(start_stop, end_stop, date)

            # try:
            #     route_id = Route.objects.get(
            #         arrival=arrival, destination=destination).pk
            #
            #     schedule_entry = Schedule.objects.filter(
            #         route=route_id, arrival_time__date=date)
            #
            #     total_records = len(list(schedule_entry))
            #
            #     bus_ids = list(schedule_entry.values_list('bus', flat=True))
            #
            #     schedule_ids = list(
            #         schedule_entry.values_list('pk', flat=True))
            #
            #     departure_times = list(
            #         schedule_entry.values_list('departure_time', flat=True))
            #
            #     arrival_times = list(
            #         schedule_entry.values_list('arrival_time', flat=True))
            #
            #     trip_duration = [arrival_times[i] - departure_times[i]
            #                      for i in range(total_records)]
            #
            #     buses = [list(Bus.objects.filter(pk=i).values_list('bus_name', flat=True))[0]
            #              for i in bus_ids]
            #
            #     entries = list(zip(buses, trip_duration, schedule_ids))
            #
            # except Route.DoesNotExist or Schedule.DoesNotExist:
            #     entries = []

    else:
        form = HomeForm()

    return render(request, 'home/home.html', {"form": form,
                                              "entries": entries, })
