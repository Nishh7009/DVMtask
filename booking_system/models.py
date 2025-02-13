from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class Bus(models.Model):

    bus_name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.bus_name}"


class Route(models.Model):
    arrival = models.CharField(max_length=250)
    destination = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.arrival} to {self.destination}"


# class BusStops(models.Model):
#
#     stop_name = models.CharField(max_length=200)
#     city = models.CharField(max_length=200)
#
#     def __str__(self):
#         return f"{self.city} - {self.stop_name}"
#

class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    available_capacity = models.IntegerField(default=50)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.bus.id} - {self.route} - {self.departure_time}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    passenger_names = ArrayField(models.CharField())
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Confirmed")
    total_price = models.IntegerField()


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.IntegerField()
