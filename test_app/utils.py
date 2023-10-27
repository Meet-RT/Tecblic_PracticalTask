from django.core.mail import send_mail
from django.conf import settings
import random
import string


def generate_otp(length=4):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_email_otp(email, otp):
    subject = 'One time password for Login'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def send_forgot_password_email(email, reset_link):
    subject = 'Forgot Password Email'
    message = f'link for reset your password: {reset_link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    fail_silently=False
    send_mail(subject, message, from_email, recipient_list, fail_silently)