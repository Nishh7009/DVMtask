from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class AddMoney(forms.Form):

    money = forms.IntegerField(max_value=5000)
