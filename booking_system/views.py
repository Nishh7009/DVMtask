from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import BookingForm, PassengerDetailForm
from django.forms import formset_factory


@login_required(login_url="/login/")
def book_bus(request, schedule_id):

    if request.method == "POST":
        form = BookingForm(request.POST, schedule_id)
        if form.is_valid():
            ticket_count = form.cleaned_data["ticket_count"]
            print(ticket_count)
            passenger_form = formset_factory(
                PassengerDetailForm, extra=ticket_count)
            formset = passenger_form(request.POST)

            if formset.is_valid():
                passengers = [
                    field.cleaned_data for field in formset if field.cleaned_data]
                return HttpResponse(f"{passengers}")

    else:
        form = BookingForm(schedule_id)
        formset = None

    return render(request, 'booking_system/book_bus.html', {"form": form, "formset": formset})
