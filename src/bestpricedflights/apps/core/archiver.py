from django.db.models import Q

from bestpricedflights.apps.core.models import Offer, Trip


def archive_offers_of_unavailable_trips(origin_code, today, travel_class, trip_type):
    unavailable_trips = Trip.objects.exclude(
        Q(fetched_on=today) | ~Q(origin__code=origin_code, travel_class=travel_class, trip_type=trip_type)
    )
    Offer.objects.filter(trip__in=unavailable_trips).update(is_archived=True)
