import structlog
from django.db.models import F, Min, Prefetch
from django.http import JsonResponse
from django.views.generic import ListView
from tailslide import Median

from .models import MoneyOutputField, Offer, Trip
from .tasks import fetch_and_store_destinations_task
from .utils import TravelClass, TripType, find_destinations

logger = structlog.get_logger(__name__)


def search_flights(request, origin, travel_class=TravelClass.BUSINESS, trip_type=TripType.RETURN):  # noqa: ARG001
    response = find_destinations(origin, travel_class, trip_type)
    response.raise_for_status()

    fetch_and_store_destinations_task.delay(origin_code=origin)
    return JsonResponse(response.json())


class DestinationListView(ListView):
    template_name = "destination_list.html"
    model = Offer

    def get_queryset(self):
        offers = Offer.objects.filter(trip__is_archived=False)
        destination_code = self.kwargs.get("destination")
        if destination_code:
            logger.debug("Filter list for destination", destination=destination_code)
            offers = offers.filter(trip__destination__code=destination_code)
        return offers.select_related("trip").prefetch_related("trip__origin", "trip__destination")


class TripListView(ListView):
    template_name = "trip_list.html"
    model = Trip

    def get_queryset(self):
        trips = Trip.objects.filter(is_archived=False)

        best_price_offers = (
            Offer.objects.annotate(median=Median("trip__offers__price_in_eur", output_field=MoneyOutputField()))
            .filter(is_archived=False)
            .annotate(min_price=Min("trip__offers__price_in_eur"))
            .filter(price_in_eur=F("min_price"), price_in_eur__lte=F("median"))
        )

        return trips.select_related("origin", "destination").prefetch_related(
            Prefetch("offers", queryset=best_price_offers, to_attr="best_price_offers"),
        )
