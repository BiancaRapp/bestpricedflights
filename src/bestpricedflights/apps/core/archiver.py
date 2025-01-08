import structlog
from django.db.models import Exists, OuterRef, Q

from bestpricedflights.apps.core.models import Offer, Trip

logger = structlog.get_logger(__name__)


def archive_unavailable_offers(origin_code, travel_class, trip_type):
    logger.debug(
        "Archiving unavailable offers",
        origin_code=origin_code,
        travel_class=travel_class,
        trip_type=trip_type,
    )
    latest_fetched_on = Trip.objects.order_by("-fetched_on").first().fetched_on
    unavailable_trips = Trip.objects.exclude(
        Q(fetched_on=latest_fetched_on) | ~Q(origin__code=origin_code, travel_class=travel_class, trip_type=trip_type)
    )

    duplicated_offers = Offer.objects.filter(
        trip=OuterRef("trip"),
        month=OuterRef("month"),
        is_archived=False,
        created_at__gt=OuterRef("created_at"),
    ).exclude(id=OuterRef("id"))

    offers_to_archive = Offer.objects.filter(Q(trip__in=unavailable_trips) | Q(Exists(duplicated_offers)))
    offers_to_archive.update(is_archived=True)
