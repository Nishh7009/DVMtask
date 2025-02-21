from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

User = get_user_model()


class Bus(models.Model):

    bus_name = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f"{self.bus_name} Number: {self.bus_number}"


class Stop(models.Model):
    stop_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.stop_name} in {self.city}"


class RouteSegment(models.Model):
    # route = models.ForeignKey(
    #     'Route', on_delete=models.CASCADE, related_name='segment_route')
    start_stop = models.ForeignKey(
        'Stop', on_delete=models.CASCADE, related_name='start_of_segment')
    end_stop = models.ForeignKey(
        'Stop', on_delete=models.CASCADE, related_name='end_of_segment')
    # order = models.PositiveIntegerField()

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['route', 'order'], name="unique order per route."),
    #         models.UniqueConstraint(fields=[
    #                                 'route', 'start_stop'], name="unique start stop for every segment in a route."),
    #         models.UniqueConstraint(
    #             fields=['route', 'end_stop'], name="unique end stop for every segment in a route."),
    #     ]

    def __str__(self):
        return f"{self.start_stop} to {self.end_stop}."


# class Route(models.Model):
#     route_name = models.CharField(max_length=250)
#
#     def __str__(self):
#         return f"{self.route_name}"
#

class Schedule(models.Model):
    bus = models.ForeignKey(
        'Bus', on_delete=models.CASCADE, related_name='schedule_bus')
    route_segment = models.ForeignKey(
        'RouteSegment', on_delete=models.CASCADE, related_name='schedule_segments')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    available_capacity = models.PositiveIntegerField(blank=True)
    price = models.PositiveIntegerField(blank=True, default=500)
    next_schedule = models.ForeignKey(
        'self', null=True, on_delete=models.SET_NULL, blank=True)

    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(check=models.Q(
    #             next_schedule=None) | models.Q(bus=models.F('next_schedule__bus')), name="same_bus"),
    #         models.CheckConstraint(check=models.Q(next_schedule=None) | models.Q(
    #             route_segment__end_stop=models.F('next_schedule__route_segment__start_stop')), name="stop_consistency"),
    #     ]

    def clean(self):
        if self.next_schedule:
            if self.bus != self.next_schedule.bus:
                raise ValidationError(
                    {'next_schedule': "Next Schedule must have the same bus."})
            if self.route_segment.end_stop != self.next_schedule.route_segment.start_stop:
                raise ValidationError(
                    {'next_schedule': "Next Schedule's start stop must be same as this Schedule's end stop."})
            if self.arrival_time.date() != self.next_schedule.departure_time.date():
                raise ValidationError(
                    {"next_schedule": "Next Schedule's deparure date is not the same as current schedule's arrival date."})

    def __str__(self):
        return f"{self.bus.bus_name} on {self.route_segment} at {self.departure_time}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_capacity = self.bus.capacity
        super().save(*args, **kwargs)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_stop = models.ForeignKey(
        Stop, on_delete=models.CASCADE, related_name='start_stop')
    end_stop = models.ForeignKey(
        Stop, on_delete=models.CASCADE, related_name='end_stop')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    schedules = models.ManyToManyField(
        'Schedule', related_name='bookings_schedule')
    passengers = models.ManyToManyField(
        'Passenger', related_name='bookings_passengers')
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[(
        'confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('pending', 'Pending')], default="pending")
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return f"Booking by {self.user} Staus: {self.status}"

    def save(self, *args, **kwargs):
        new = self.pk is None
        super().save(*args, **kwargs)
        if new:
            for schedule in self.schedules.all():
                schedule.available_capacity -= self.passengers.count()
                schedule.save()
            self.user.wallet -= self.total_price
            self.user.save()

    def cancel(self):
        if self.status != "cancelled":
            self.status = "cancelled"
            self.save()

            self.user.wallet += self.total_price
            self.user.save()

            for schedule in self.schedules.all():
                schedule.available_capacity += self.passengers.count()
                schedule.save()


class Passenger(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MaxValueValidator(99)], blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='payments_user')
    booking = models.ForeignKey(
        'Booking', on_delete=models.CASCADE, related_name='payments_bookings')
    amount = models.PositiveIntegerField()
    refunded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.refunded:
            self.user.wallet -= self.amount
            self.user.save()
        super(self, *args, **kwargs)

    def refund(self):
        if not self.refunded:
            self.refunded = True
            self.save()

            self.user.wallet += self.amount
            self.user.save()
