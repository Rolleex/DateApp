# import os
# import time
#
# from celery import Celery
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Date.settings')
# app = Celery("Date")
# app.config_from_object('django.conf:settings', namespace="CELERY")
# app.autodiscover_tasks()
#
# @app.task()
# def debug_task():
#     time.sleep(10)
#     print('hello from debug_task celery app')
#
#
