from django.shortcuts import render, HttpResponse
from booking_system.models import Schedule, Passenger, Booking
# Create your views here.


def payment(request):
    booking_data = request.session['booking_data']
    schedule_ids = booking_data['schedule_ids']

    start_schedule = Schedule.objects.get(pk=schedule_ids[0])
    end_schedule = Schedule.objects.get(pk=schedule_ids[-1])

    start_stop = start_schedule.route_segment.start_stop
    end_stop = end_schedule.route_segment.end_stop
    bus_name = start_schedule.bus.bus_name
    bus_number = start_schedule.bus.bus_number
    departure_time = start_schedule.departure_time
    arrival_time = end_schedule.arrival_time
    passengers = booking_data['passengers']
    total_price = len(passengers)*booking_data['price']

    context = {'start_stop': start_stop,
               'end_stop': end_stop,
               'bus_name': bus_name,
               'bus_number': bus_number,
               'departure_time': departure_time,
               'arrival_time': arrival_time,
               'passengers': passengers,
               'total_price': total_price,
               'booking_confirmed': False}

    if request.method == "POST":
        passenger_objects = []
        schedule_objects = list(Schedule.objects.filter(pk__in=schedule_ids))

        for passenger in passengers:
            passenger_object = Passenger.objects.create(**passenger)
            passenger_objects.append(passenger_object)

        booking = Booking.objects.create(
            user=request.user, start_stop=start_stop, end_stop=end_stop, departure_time=departure_time, arrival_time=arrival_time, status="confirmed", total_price=total_price)

        booking.save()

        booking.schedules.set(schedule_objects)
        booking.passengers.set(passenger_objects)

        booking.save()
        context['booking_confirmed'] = True

    return render(request, 'payments/payment_gateway.html', context)
