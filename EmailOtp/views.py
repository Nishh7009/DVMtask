from django.shortcuts import render
from .utils import generate_otp, verify_otp
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.


def verify_otp_view(request):
    if request.method == "GET":
        generate_otp(request.user)
    next = request.GET.get('next')
    if not next:
        next = '/home/'
    if request.method == "POST":
        user_otp = request.POST.get("otp")
        if verify_otp(request.user.otp, user_otp):
            request.user.is_verified = True
            request.user.save()
            return redirect(next)
        else:
            messages.error(request, "OTP is incorrect, Please try again.")
            return redirect(request.path)

    return render(request, 'EmailOtp/verify_otp_view.html')
