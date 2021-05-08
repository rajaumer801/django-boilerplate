import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      '{{cookiecutter.main_module}}.settings.production')

app = Celery('{{cookiecutter.main_module}}')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
