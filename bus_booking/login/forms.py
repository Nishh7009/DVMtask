from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150, required=True, label="Username")
    email = forms.EmailField()
    fname = forms.CharField(label="First Name")
    lname = forms.CharField(label="Last Name")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        errors = {}

        if password and len(password) < 8:
            errors["password"] = "Password length must be at least 8 characters long."

        if password and confirm_password and password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "The username \"%(username)s\" is already taken.",
                params={"username": username})

        return username

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered. Please log in instead.")

        return email


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    password = forms.CharField(
        widget=forms.PasswordInput, label="Password", required=True)

    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    # def clean_password(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #
    #     if len(password) < 8:
    #         raise forms.ValidationError(
    #             "Password length must be at least 8 characters long.")
    #
    #     return password
