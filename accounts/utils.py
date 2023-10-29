from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import verification_token
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()

def send_email_to_user(user: User):
    subject = 'Activate your Account'
    body = render_to_string(
        'email_verification.html',
        {
        'domain': 'http://localhost:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': verification_token.make_token(user)
        }
    )
    from_email = 'notify@nino-shop.io'
    to_email = [user.email]
    send_mail(
        subject,
        "",
        from_email,
        to_email,
        html_message=body
    )

def check_is_manager(user):
    try:
        group = Group.objects.get(name='Manager')
    except Group.DoesNotExist:
        return False
    if group in user.groups.all():
        return True
    return False
