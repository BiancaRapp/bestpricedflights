from django.http import JsonResponse

from .utils import TravelClass, TripType, find_destinations


def search_flights(request, origin, travel_class=TravelClass.BUSINESS, trip_type=TripType.RETURN):  # noqa: ARG001
    destinations = find_destinations(origin, travel_class, trip_type)

    return JsonResponse(destinations)
