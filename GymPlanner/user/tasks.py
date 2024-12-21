from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_confirmation_email(email, confirm_url):
    send_mail(
        subject="Подтверждение электронной почты",
        message=f"Перейдите по ссылке, чтобы подтвердить вашу почту: {confirm_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
