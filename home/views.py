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

    else:
        form = HomeForm()

    return render(request, 'home/home.html', {"form": form,
                                              "entries": entries, })
