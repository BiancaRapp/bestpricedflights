from django.db.models import Q

from bestpricedflights.apps.core.models import Offer, Trip


def archive_unavailable_trips_and_offers(origin_code, today, travel_class, trip_type):
    trips_to_archive = Trip.objects.exclude(
        Q(fetched_on=today) | ~Q(origin__code=origin_code, travel_class=travel_class, trip_type=trip_type)
    )
    Offer.objects.filter(trip__in=trips_to_archive).update(is_archived=True)
    trips_to_archive.update(is_archived=True)
