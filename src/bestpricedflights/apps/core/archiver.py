from django.db.models import Q

from bestpricedflights.apps.core.models import Offer, Trip


def archive_unavailable_offers(origin_code, travel_class, trip_type):
    latest_fetched_on = Trip.objects.order_by("-fetched_on").first().fetched_on
    unavailable_trips = Trip.objects.exclude(
        Q(fetched_on=latest_fetched_on) | ~Q(origin__code=origin_code, travel_class=travel_class, trip_type=trip_type)
    )
    Offer.objects.filter(trip__in=unavailable_trips).update(is_archived=True)
