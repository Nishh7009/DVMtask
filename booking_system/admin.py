from django.contrib import admin
from .models import Booking, Bus, Schedule, Payment, Route

admin.site.register(Booking)
admin.site.register(Route)
admin.site.register(Payment)
admin.site.register(Schedule)
admin.site.register(Bus)
