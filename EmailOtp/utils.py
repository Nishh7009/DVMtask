import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings


def generate_otp(user):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    user.otp = totp.now()
    user.save()
    send_mail('Email Verification OTP', f'Your OTP for email verification is {
              user.otp}', settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify_otp(otp, user_otp):
    return otp == user_otp
