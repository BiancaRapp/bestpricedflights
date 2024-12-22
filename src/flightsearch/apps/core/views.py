from django.http import JsonResponse

from .tasks import fetch_and_store_destinations_task
from .utils import TravelClass, TripType, find_destinations


def search_flights(request, origin, travel_class=TravelClass.BUSINESS, trip_type=TripType.RETURN):  # noqa: ARG001
    response = find_destinations(origin, travel_class, trip_type)
    response.raise_for_status()

    fetch_and_store_destinations_task.delay(origin_codes=(origin,))
    return JsonResponse(response.json())
