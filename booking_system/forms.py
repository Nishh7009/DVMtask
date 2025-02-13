from django import forms
from .models import Schedule


class BookingForm(forms.Form):

    ticket_count = forms.IntegerField(
        min_value=1, max_value=5, label="Number of tickets to book")
    # schedule_id = 0

    # def clean(self):
    #     cleaned_data = super().clean()
    #     schedule_id = self.schedule_id
    #     ticket_count = cleaned_data.get('ticket_count')
    #
    #     print(schedule_id)
    #     print(ticket_count)
    #
    #     available_capacity = list(Schedule.objects.filter(
    #         pk=schedule_id).values_list('available_capacity', flat=True))[0]
    #
    #     print(available_capacity)
    #
    #     if available_capacity < ticket_count:
    #         return forms.ValidationError("Not enough seats available.")
    #
    #     return cleaned_data

    # def __init__(self, schedule_id, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.schedule_id = schedule_id


class PassengerDetailForm(forms.Form):

    name = forms.CharField(max_length=200)
