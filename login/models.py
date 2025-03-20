from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps


class CustomUser(AbstractUser):
    wallet = models.IntegerField(default=0)
    admin_of = models.ForeignKey(
        "booking_system.Bus", on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(blank=True)
