import os
from datetime import timedelta

import structlog
from celery import Celery
from django.conf import settings
from django.utils.module_loading import import_string
from django_structlog.celery.steps import DjangoStructLogInitStep

logger = structlog.get_logger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flightsearch.settings")

app = Celery("flightsearch")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.steps["worker"].add(DjangoStructLogInitStep)

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):  # noqa: ARG001
    sender.add_periodic_task(
        timedelta(days=1), collect_destinations_for_multiple_origins_task.s(), name="fetch destinations every day"
    )
    sender.add_periodic_task(timedelta(days=1), update_rates.s(), name="update exchange rates every day")


@app.task
def collect_destinations_for_multiple_origins_task():
    from flightsearch.apps.core.tasks import collect_destinations_for_multiple_origins_task

    collect_destinations_for_multiple_origins_task()


@app.task
def update_rates(backend=settings.EXCHANGE_BACKEND, **kwargs):
    backend = import_string(backend)()
    try:
        backend.update_rates(**kwargs)
        logger.debug("Rates updated successfully!")
    except Exception as e:
        logger.exception("Failed to update rates", extra={"exception": e})
