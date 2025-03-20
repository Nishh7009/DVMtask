from django.db import transaction
from .models import Schedule
from datetime import timedelta, datetime
from django.utils import timezone


@transaction.atomic
def toggle_weekly(schedule, weekly):
    schedule_to_convert = schedule
    while len(list(Schedule.objects.filter(next_schedule=schedule_to_convert))) > 0:
        schedule_to_convert = list(Schedule.objects.filter(
            next_schedule=schedule_to_convert))[0]
    schedule_to_convert.is_weekly = weekly
    schedule_to_convert.save()


@transaction.atomic
def create_weekly_schedules(bus):
    schedules = Schedule.objects.filter(
        bus=bus, next_schedule=None, departure_time__lte=timezone.make_aware(datetime.now()))
    paired_schedules = []
    for schedule in schedules:
        schedule_group = [schedule]
        while len(list(Schedule.objects.filter(next_schedule=schedule))) > 0:
            schedule = list(Schedule.objects.filter(
                next_schedule=schedule))[0]
            schedule_group.append(schedule)
        paired_schedules.append(schedule_group)
    created_schedules = []
    number_of_schedules_created = 0
    for schedule_group in paired_schedules:
        new_schedule_group = []
        for index in range(len(schedule_group)):
            print(schedule_group[index].departure_time.tzinfo)
            if index == 0:
                schedule, created = Schedule.objects.get_or_create(bus=bus,
                                                                   route_segment=schedule_group[index].route_segment,
                                                                   departure_time=timezone.localtime(schedule_group[index].departure_time +
                                                                                                     timedelta(weeks=1)),
                                                                   arrival_time=timezone.localtime(schedule_group[index].arrival_time +
                                                                                                   timedelta(weeks=1)),
                                                                   is_weekly=True, price=schedule_group[index].price)
                new_schedule_group.append(schedule)
                if created:
                    number_of_schedules_created += 1
            else:
                schedule, created = Schedule.objects.get_or_create(bus=bus,
                                                                   route_segment=schedule_group[index].route_segment,
                                                                   departure_time=timezone.localtime(schedule_group[index].departure_time +
                                                                                                     timedelta(weeks=1)),
                                                                   arrival_time=timezone.localtime(schedule_group[index].arrival_time +
                                                                                                   timedelta(weeks=1)),
                                                                   is_weekly=True, price=schedule_group[index].price,
                                                                   next_schedule=new_schedule_group[index-1])
                new_schedule_group.append(schedule)
                if created:
                    number_of_schedules_created += 1
        created_schedules.append(new_schedule_group)

    return number_of_schedules_created
