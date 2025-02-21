from booking_system.models import RouteSegment, Schedule

#
# def find_buses(start_stop, end_stop, date):
#     start_segments = RouteSegment.objects.filter(start_stop=start_stop)
#
#     buses = []
#
#     for start in start_segments:
#
#         end = RouteSegment.objects.filter(
#             route=start.route, end_stop=end_stop).first()
#
#         if end and start.order < end.order:
#             all_segments = RouteSegment.objects.filter(
#                 route=start.route, order__gte=start, order__lte=end).order_by('order')
#
#             starting_schedules = Schedule.objects.filter(
#                 route_segment=start, departure_time__date=date)
#
#             for schedule in starting_schedules:
#
#                 schedules = list(Schedule.objects.filter(
#                     route_segment__in=all_segments, bus=schedule.bus).order_by('departure_time'))
#
#                 if len(schedules) == len(all_segments):
#                     buses.append({
#                         'bus': schedule.bus,
#                         'schedules': schedules,
#                         'start_time': schedules[0].departure_time,
#                         'end_time': schedule[-1].arrival_time,
#                         'price': sum(schedule.price for schedule in schedules)
#                     })
#
#     return buses


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
