import os

from celery import Celery
from django_structlog.celery.steps import DjangoStructLogInitStep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flightsearch.settings")

app = Celery("flightsearch")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.steps["worker"].add(DjangoStructLogInitStep)

app.autodiscover_tasks()
