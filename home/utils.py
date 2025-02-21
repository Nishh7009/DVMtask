from booking_system.models import Schedule


def find_buses(start_stop, end_stop, date):
    start_schedules = Schedule.objects.filter(
        route_segment__start_stop=start_stop, departure_time__date=date)

    buses = []

    for schedule in start_schedules:
        current_schedule = schedule
        departure_time = current_schedule.departure_time
        all_schedules = []
        valid_schedule = False
        price = 0
        arrival_time = None
        available_capacity = current_schedule.available_capacity

        while current_schedule is not None:
            all_schedules.append(current_schedule.id)
            price += current_schedule.price
            available_capacity = min(
                available_capacity, current_schedule.available_capacity)
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
                          price,
                          available_capacity
                          ))

    return buses
