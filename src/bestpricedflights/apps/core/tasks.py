import structlog
from celery import shared_task
from django.conf import settings

from bestpricedflights.celery import app

from .archiver import archive_unavailable_offers
from .choices import TravelClass, TripType
from .lufthansa.destination_finder import find_destinations
from .lufthansa.offers_parser import parse_response_and_store_offers

logger = structlog.get_logger(__name__)


@app.task
def collect_destinations_for_multiple_origins_task():
    for origin_code in settings.ORIGIN_CODES:
        fetch_and_store_destinations_task(origin_code=origin_code, travel_class=TravelClass.BUSINESS)


@shared_task
def fetch_and_store_destinations_task(
    origin_code: str, travel_class=TravelClass.BUSINESS.value, trip_type=TripType.RETURN.value
):
    response = find_destinations(origin_code, travel_class, trip_type)
    if not response.ok:
        logger.error(
            "Failed fetching destinations",
            extra={"origin_code": origin_code, "status_code": response.status_code, "text": response.text},
        )
        return

    parse_response_and_store_offers(response.json(), origin_code, travel_class, trip_type)
    archive_unavailable_offers(origin_code, travel_class, trip_type)
