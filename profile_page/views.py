from django.shortcuts import render
from .forms import UserDetails, AddMoney
from django.contrib.auth import get_user_model
from django.db.models import F
from booking_system.models import Booking

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
        id = request.POST.get('booking_id')
        print(id)
        booking = Booking.objects.get(pk=id)
        print(booking)
        booking.cancel()
    return render(request, 'profile_page/booking.html', {"bookings": bookings})
