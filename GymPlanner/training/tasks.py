from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from training.models import Reminder


@shared_task
def send_email_reminder(reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id, sent=False)
        user = reminder.user
        training = reminder.training
        send_mail(
            subject=f'Напоминание о тренировке: {training.title}',
            message=f"Здравствуйте, {user.username}!\n\n"
                    f"Это напоминание о вашей тренировке '{training.title}', которая начнется "
                    f"уже скоро. Не забудьте подготовиться!",
            from_email='vadim.raidiyk@mail.ru',
            recipient_list=[user.email],
        )
        reminder.sent = True
        reminder.save()
        return f'Напоминание для {user.username} отправлено'
    except Reminder.DoesNotExist:
        return "Напоминание не найдено или уже отправлено."

@shared_task
def schedule_reminder():
    one_hour_before = now() + timedelta(hours=1)
    reminders = Reminder.objects.filter(sent=False, remind_at__lte=one_hour_before)
    for reminder in reminders:
        send_email_reminder.delay(reminder.id)