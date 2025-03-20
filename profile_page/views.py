from django.shortcuts import render, redirect
from .forms import AddMoney
from django.contrib.auth import get_user_model
from django.db.models import F
from booking_system.models import Booking
from datetime import datetime
from django.urls import reverse
from booking_system.forms import PassengerDetailForm
from django.forms import modelformset_factory
from booking_system.models import Passenger

User = get_user_model()


def profile(request):
    return render(request, 'profile_page/profile.html')


def wallet(request):

    if request.method == "POST":
        form = AddMoney(request.POST)
        if form.is_valid():
            money = form.cleaned_data.get("money")
            user = request.user
            user.wallet = F('wallet') + money
            user.save()
            user.refresh_from_db()
    else:
        form = AddMoney()

    return render(request, 'profile_page/wallet.html', {'form': form})


def bookings(request):
    Booking.objects.filter(
        user=request.user, departure_time__lte=datetime.now(), arrival_time__gte=datetime.now()).update(status='ongoing')
    Booking.objects.filter(
        user=request.user, arrival_time__lte=datetime.now()).update(status='completed')
    bookings = []
    booking_objects = Booking.objects.filter(user=request.user)
    for booking in booking_objects:
        data = {}
        data['id'] = booking.id
        data['start_stop'] = booking.start_stop
        data['end_stop'] = booking.end_stop
        data['departure_time'] = booking.departure_time
        data['arrival_time'] = booking.arrival_time
        data['status'] = booking.status
        data['price'] = booking.total_price
        data['booking_time'] = booking.booking_time
        data['tickets'] = booking.passengers.count()
        bookings.append(data)

    if request.method == "POST":
        return redirect(reverse('booking_details', args=[int(request.POST.get("booking_id"))]))
    return render(request, 'profile_page/booking.html', {"bookings": bookings})


def booking_details(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    if request.user == booking.user:
        details = {}
        details['booking_time'] = booking.booking_time
        details['user'] = booking.user
        details['start_stop'] = booking.start_stop
        details['end_stop'] = booking.end_stop
        details['departure_time'] = booking.departure_time
        details['arrival_time'] = booking.arrival_time
        details['status'] = booking.status
        details['passengers'] = booking.passengers.all()
        details['price'] = booking.total_price
        details['id'] = booking_id

        if request.method == "POST":
            if request.POST.get("cancel"):
                booking.cancel()
                return redirect(reverse('user_bookings'))

        return render(request, 'profile_page/view_details.html', details)


def edit_passenger_details(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    passengers = booking.passengers.all()

    passenger_formset = modelformset_factory(
        Passenger, form=PassengerDetailForm, extra=0)

    if request.method == "POST":
        formset = passenger_formset(request.POST, queryset=passengers)
        if formset.is_valid():
            formset.save()
            return redirect('booking_details', booking_id=booking_id)
    else:
        formset = passenger_formset(queryset=passengers)

    return render(request, 'profile_page/edit_passenger_details.html', {'formset': formset, 'booking_id': booking_id})
