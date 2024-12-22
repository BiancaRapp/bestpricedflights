import structlog
from celery import shared_task
from django.utils.timezone import now

from .choices import TravelClass, TripType
from .models import City, Offer, Trip
from .utils import find_destinations

logger = structlog.get_logger(__name__)


@shared_task
def fetch_and_store_destinations_task(
    origin_codes: [str], travel_class=TravelClass.BUSINESS, trip_type=TripType.RETURN
):
    for origin_code in origin_codes:
        response = find_destinations(origin_code, travel_class, trip_type)
        if not response.ok:
            logger.error("Failed fetching destinations", extra={"origin_code": origin_code})
            continue
        json = response.json()

        destination_finder_offers = json.get("destinationFinderOffers")
        if len(destination_finder_offers) == 0:
            logger.warning("No destination offers found", extra={"origin_code": origin_code})
            continue

        origin_data = json.get("origin")
        origin, _ = City.objects.update_or_create(
            code=origin_code,
            defaults={
                "name": origin_data.get("cityName"),
                "longitude": origin_data.get("cityLongitude"),
                "latitude": origin_data.get("cityLatitude"),
                "currency": json.get("currencyInfo").get("currency"),
            },
        )
        for destination_data in destination_finder_offers:
            destination, _ = City.objects.update_or_create(
                code=destination_data.get("city"),
                defaults={
                    "name": destination_data.get("cityName"),
                    "region": destination_data.get("cityRegion"),
                    "longitude": destination_data.get("cityLongitude"),
                    "latitude": destination_data.get("cityLatitude"),
                },
            )
            trip, _ = Trip.objects.update_or_create(
                origin=origin,
                destination=destination,
                travel_class=travel_class,
                trip_type=trip_type,
                defaults={"fetched_on": now()},
            )
            for offer_data in destination_data.get("monthOffers"):
                offer, _ = Offer.objects.update_or_create(
                    trip=trip,
                    month=int(offer_data.get("month")),
                    defaults={
                        "price": offer_data.get("price"),
                        "stopovers": offer_data.get("numberOfStopovers", 0),
                    },
                )
