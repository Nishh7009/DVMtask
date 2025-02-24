from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import BookingForm, PassengerDetailForm
from django.forms import formset_factory
from django.contrib import messages


@login_required(login_url="/login/")
def book_bus(request):

    ticket_count = request.session.get('ticket_count', 1)

    if request.method == "POST":

        form = BookingForm(request.POST, request=request)

        if 'submit_ticket_count' in request.POST and form.is_valid():
            ticket_count = form.cleaned_data.get(
                'ticket_count', ticket_count)
            request.session['ticket_count'] = ticket_count

        detail_formset = formset_factory(
            PassengerDetailForm, extra=ticket_count)
        formset = detail_formset()

        if 'submit_passenger_details' in request.POST:
            form = BookingForm(request=request)
            formset = detail_formset(request.POST)
            valid_formset = False
            for item in formset:
                if item.is_valid() and item.cleaned_data:
                    valid_formset = True
                else:
                    valid_formset = False
                    messages.error(
                        request, "Please fill in all passenger details.")
            if valid_formset:
                passengers = [item.cleaned_data for item in formset]
                booking_data = request.session['booking_data']
                booking_data['passengers'] = passengers
                request.session['booking_data'] = booking_data
                return redirect('/payments/')

    else:
        form = BookingForm(request=request)
        formset = None

    return render(request, 'booking_system/book_bus.html', {"form": form, "formset": formset})
