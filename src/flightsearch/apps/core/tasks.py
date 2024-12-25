import structlog
from celery import shared_task
from django.db.models import Q
from django.utils.timezone import now
from djmoney.money import Money

from flightsearch.celery import app

from .choices import TravelClass, TripType
from .models import City, Offer, Trip
from .utils import find_destinations

logger = structlog.get_logger(__name__)


@app.task
def collect_destinations_for_multiple_origins_task():
    origin_codes = ("STR", "FRA", "MUC", "AMS", "PAR", "COP", "OSL", "BUD", "IST", "SOF")
    for origin_code in origin_codes:
        fetch_and_store_destinations_task.delay(origin_code=origin_code)


@shared_task
def fetch_and_store_destinations_task(origin_code: str, travel_class=TravelClass.BUSINESS, trip_type=TripType.RETURN):
    today = now().date()

    response = find_destinations(origin_code, travel_class, trip_type)
    if not response.ok:
        logger.error(
            "Failed fetching destinations",
            extra={"origin_code": origin_code, "status_code": response.status_code, "text": response.text},
        )
        return
    json = response.json()

    logger.debug("Fetch destination offers", extra={"origin_code"})
    destination_finder_offers = json.get("destinationFinderOffers")
    if len(destination_finder_offers) == 0:
        logger.warning("No destination offers found", extra={"origin_code": origin_code})
        return

    origin_data = json.get("origin")
    origin, _ = City.objects.update_or_create(
        code=origin_code,
        defaults={
            "name": origin_data.get("cityName"),
            "longitude": origin_data.get("cityLongitude"),
            "latitude": origin_data.get("cityLatitude"),
            "is_origin": True,
        },
    )
    currency = json.get("currencyInfo", {}).get("currency")

    for destination_data in destination_finder_offers:
        destination, _ = City.objects.update_or_create(
            code=destination_data.get("city"),
            defaults={
                "name": destination_data.get("cityName"),
                "region": destination_data.get("cityRegion"),
                "longitude": destination_data.get("cityLongitude"),
                "latitude": destination_data.get("cityLatitude"),
                "is_destination": True,
            },
        )
        trip, _ = Trip.objects.update_or_create(
            origin=origin,
            destination=destination,
            travel_class=travel_class,
            trip_type=trip_type,
            defaults={"fetched_on": today},
        )
        trip.offers.update(is_archived=True)
        for offer_data in destination_data.get("monthOffers"):
            Offer.objects.create(
                trip=trip,
                month=int(offer_data.get("month")),
                price=Money(offer_data.get("price"), currency=currency),
                stopovers=offer_data.get("numberOfStopovers", 0),
            )

    # Archive trips and related offers with destinations not available anymore
    trips_to_archive = Trip.objects.exclude(
        Q(fetched_on=today) | ~Q(origin__code=origin_code, travel_class=travel_class, trip_type=trip_type)
    )

    Offer.objects.filter(trip__in=trips_to_archive).update(is_archived=True)
    trips_to_archive.update(is_archived=True)
