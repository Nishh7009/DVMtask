from django import forms
from django.contrib.auth import get_user_model
from booking_system.models import Stop
import datetime

User = get_user_model()


class HomeForm(forms.Form):

    start_stop = forms.ModelChoiceField(
        queryset=Stop.objects.all(),
        empty_label='None',)

    end_stop = forms.ModelChoiceField(
        queryset=Stop.objects.all(),
        empty_label='None',)

    date = forms.DateField(widget=forms.SelectDateWidget(),
                           initial=datetime.date.today(),)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')

        if date < datetime.date.today():
            raise forms.ValidationError("Cannot book bus for past dates.")

        return cleaned_data
