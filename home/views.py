from django.shortcuts import render, redirect
from .forms import HomeForm
from booking_system.models import Schedule


def home(request):

    if request.method == "POST":
        form = HomeForm(request.POST)
        if form.is_valid():
            arrival = form.cleaned_data.get("arrival")
            destination = form.cleaned_data.get("destination")

            return redirect('bus_search', arrival=arrival, destination=destination)
    else:
        form = HomeForm()

    return render(request, 'home/home.html', {"form": form})
