from django import forms
from booking_system.models import Schedule
from booking_system.utils import convert_to_weekly


class AddSchedule(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['route_segment', 'departure_time', 'arrival_time',
                  'price', 'available_capacity', 'next_schedule']


class ChangeSchedule(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['available_capacity', 'departure_time',
                  'arrival_time', 'price', 'next_schedule', 'is_running', 'is_weekly']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.is_running:
            convert_to_weekly(instance)

        if not instance.is_running:
            instance.cancel()
        if commit:
            instance.save()
        return instance
