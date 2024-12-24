import structlog
from django.http import JsonResponse
from django.views.generic import ListView

from .models import Offer
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
        offers = Offer.objects.all()
        destination_code = self.kwargs.get("destination")
        if destination_code:
            logger.debug("Filter list for destination", destination=destination_code)
            offers = offers.filter(trip__destination__code=destination_code)
        return offers.select_related("trip")
