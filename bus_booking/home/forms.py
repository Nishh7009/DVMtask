from django import forms
from django.contrib.auth import get_user_model
from booking_system.models import Stop

User = get_user_model()


class HomeForm(forms.Form):

    start_stop = forms.ModelChoiceField(
        queryset=Stop.objects.all(),
        empty_label='None',)

    end_stop = forms.ModelChoiceField(
        queryset=Stop.objects.all(),
        empty_label='None',)

    date = forms.DateField(widget=forms.SelectDateWidget())

    # def clean(self):
    #     cleaned_data = super().clean()
    #     arrival = cleaned_data.get('arrival')
    #     destination = cleaned_data.get('destination')
    #
    #     if not Route.objects.filter(arrival=arrival, destination=destination):
    #         raise forms.ValidationError(
    #             'Not a servicable route. Please try again.')
    #
    #     return cleaned_data
