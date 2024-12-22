import os
from datetime import timedelta

from celery import Celery
from django_structlog.celery.steps import DjangoStructLogInitStep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flightsearch.settings")

app = Celery("flightsearch")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.steps["worker"].add(DjangoStructLogInitStep)

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(days=1), collect_destinations_for_multiple_origins_task.s(), name="fetch destinations every day"
    )


@app.task
def collect_destinations_for_multiple_origins_task():
    from flightsearch.apps.core.tasks import collect_destinations_for_multiple_origins_task

    collect_destinations_for_multiple_origins_task()
