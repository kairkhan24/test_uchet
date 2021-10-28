import redis
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def send_message(total):
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    emails = r.get('emails')
    if emails:
        send_mail(
            'Ту-тут',
            'Статус задачи изменен!',
            settings.DEFAULT_FROM_EMAIL,
            [emails[0]]
        )
        del emails[0]
        r.set('emails', emails)
