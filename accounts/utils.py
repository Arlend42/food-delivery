from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from .models import User


def determine_user(user):
    if user.role == User.RESTAURANT:
        redirectUrl = "restaurant_profile"
        return redirectUrl
    elif user.role == User.CUSTOMER:
        redirectUrl = "customer_profile"
        return redirectUrl
    elif user.role is None and user.is_superadmin:
        redirectUrl = "/admin"
        return redirectUrl


def verification_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = "To activate this account please follow the link sent to your email!"
    message = render_to_string(
        "accounts/emails/account_verification_email.html",
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
