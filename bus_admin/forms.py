from django import forms
from booking_system.models import Schedule
from booking_system.utils import toggle_weekly


class AddSchedule(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['route_segment', 'departure_time', 'arrival_time',
                  'price', 'available_capacity', 'next_schedule']

    def __init__(self, *args, bus=None, **kwargs):
        super().__init__(*args, **kwargs)

        if bus:
            self.fields['next_schedule'].queryset = Schedule.objects.filter(
                bus=bus)


class ChangeSchedule(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['available_capacity', 'departure_time',
                  'arrival_time', 'price', 'next_schedule', 'is_running', 'is_weekly']

    def save(self, commit=True):
        instance = super().save(commit=False)
        toggle_weekly(instance, instance.is_weekly)

        if not instance.is_running:
            instance.cancel()
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if instance:
            self.fields['next_schedule'].queryset = Schedule.objects.filter(
                bus=instance.bus, route_segment__start_stop=instance.route_segment.end_stop)
