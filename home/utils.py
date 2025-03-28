from booking_system.models import Schedule
from datetime import datetime


def find_buses(start_stop, end_stop, date):
    start_schedules = Schedule.objects.filter(
        route_segment__start_stop=start_stop, departure_time__date=date, is_running=True, departure_time__gte=datetime.now(), available_capacity__gte=1)

    buses = []

    for schedule in start_schedules:
        current_schedule = schedule
        departure_time = current_schedule.departure_time
        all_schedules = []
        valid_schedule = False
        price = 0
        arrival_time = None

        while current_schedule is not None and current_schedule.available_capacity > 0:
            all_schedules.append(current_schedule.id)
            price += current_schedule.price
            arrival_time = current_schedule.arrival_time
            if current_schedule.route_segment.end_stop == end_stop:
                valid_schedule = True
                break
            current_schedule = current_schedule.next_schedule

        if valid_schedule:
            buses.append((current_schedule.bus,
                          all_schedules,
                          departure_time,
                          arrival_time,
                          price
                          ))

    return buses
