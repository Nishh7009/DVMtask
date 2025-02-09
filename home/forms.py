from django import forms
from django.contrib.auth import get_user_model
from booking_system.models import Route

User = get_user_model()


class HomeForm(forms.Form):
    arrival = forms.ModelChoiceField(
        queryset=Route.objects.values_list('arrival', flat=True))
    destination = forms.ModelChoiceField(
        queryset=Route.objects.values_list('destination', flat=True))
    date = forms.DateField(widget=forms.SelectDateWidget())

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        arrival = cleaned_data.get('arrival')
        destination = cleaned_data.get('destination')

        if not Route.objects.filter(arrival=arrival, destination=destination):
            raise forms.ValidationError(
                'Not a servicable route. Please try again.')

        return cleaned_data
