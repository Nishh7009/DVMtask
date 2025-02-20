from django.contrib import admin
from .models import Booking, Bus, Schedule, Payment, Stop, RouteSegment

admin.site.register(Booking)
# admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(Payment)
admin.site.register(Schedule)
admin.site.register(Bus)
admin.site.register(RouteSegment)
