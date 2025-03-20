from django import forms
from .models import Schedule, Passenger


class BookingForm(forms.Form):

    ticket_count = forms.IntegerField(
        min_value=1, max_value=5, label="Number of tickets to book")

    def clean(self):
        cleaned_data = super().clean()
        ticket_count = cleaned_data.get('ticket_count', 1)

        available_capacity = min(list(Schedule.objects.filter(
            pk__in=self.request.session['booking_data']['schedule_ids']).values_list('available_capacity', flat=True)))

        if available_capacity < ticket_count:
            raise forms.ValidationError("Not enough seats available.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


class PassengerDetailForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name', 'age']
