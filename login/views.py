from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.contrib import messages
from .forms import RegistrationForm, LoginForm

User = get_user_model()


def Login(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            next_url = request.GET.get('next', '/home/')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect(next_url)

            else:
                messages.error(request, "Invalid Username/Password.")
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/home/")


def Register(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            fname = form.cleaned_data["fname"]
            lname = form.cleaned_data["lname"]
            password = form.cleaned_data["password"]

            User.objects.create_user(username=username,
                                     email=email,
                                     first_name=fname,
                                     last_name=lname,
                                     password=password,)

            messages.success(request, "Registration Successful!")
            return redirect("home")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        form = RegistrationForm()

    return render(request, "login/register.html", {"form": form})
