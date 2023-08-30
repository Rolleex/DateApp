import os
import time
import uuid

from PIL import Image
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from users_profile.models import Profile


@shared_task
def mail_send(me_profile_id, you_profile_id):
    me_profile = Profile.objects.get(id=me_profile_id)
    you_profile = Profile.objects.get(id=you_profile_id)

    send_mail(
        f"Вы понравились {me_profile.first_name}!",
        f"Вы понравились {me_profile.first_name}! Почта участника: {me_profile.email}",
        me_profile.email,
        [you_profile.email],
        fail_silently=False,
    )
    send_mail(
        f"Вы понравились {you_profile.first_name}!",
        f"Вы понравились {you_profile.first_name}! Почта участника: {you_profile.email}",
        you_profile.email,
        [me_profile.email],
        fail_silently=False,
    )
