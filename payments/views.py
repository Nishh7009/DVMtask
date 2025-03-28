from django.db import transaction
from django.contrib import messages
from django.shortcuts import render
from booking_system.models import Schedule, Passenger, Booking, Payment
# Create your views here.


@transaction.atomic
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
        try:
            passenger_objects = [Passenger(**passenger)
                                 for passenger in passengers]
            schedule_objects = list(
                Schedule.objects.filter(pk__in=schedule_ids))

            Passenger.objects.bulk_create(passenger_objects)

            booking = Booking.objects.create(
                user=request.user, start_stop=start_stop, end_stop=end_stop, departure_time=departure_time, arrival_time=arrival_time, status="confirmed", total_price=total_price)

            booking.schedules.set(schedule_objects)
            booking.passengers.set(passenger_objects)

            Payment.objects.create(
                user=request.user, booking=booking, amount=total_price)

            context['booking_confirmed'] = True
            messages.success(
                request, "Booking and payment completed successfully")
        except Exception as e:
            messages.error(request, f"An error occured: {str(e)}")
            raise

    return render(request, 'payments/payment_gateway.html', context)
