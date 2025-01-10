import structlog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import F, Min, OuterRef, Prefetch, Q, Subquery
from django.http import JsonResponse
from django.views.generic import ListView, TemplateView
from tailslide import Median

from .lufthansa.destination_finder import TravelClass, TripType, find_destinations
from .models import City, Country, MoneyOutputField, Offer, Trip
from .tasks import fetch_and_store_destinations_task

logger = structlog.get_logger(__name__)


@login_required
def search_flights(request, origin, travel_class=TravelClass.BUSINESS.value, trip_type=TripType.RETURN.value):
    if not request.user.is_superuser:
        raise PermissionDenied

    response = find_destinations(origin, travel_class, trip_type)
    response.raise_for_status()

    fetch_and_store_destinations_task.delay(origin_code=origin)
    return JsonResponse(response.json())


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "destinations": City.objects.filter(is_destination=True).order_by("region", "country").distinct(),
            }
        )
        return context


class DestinationListView(LoginRequiredMixin, ListView):
    template_name = "destination_list.html"
    model = Offer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        destination_code = self.kwargs.get("destination")
        destination_country_code = self.kwargs.get("destination_country")
        destination = (
            City.objects.filter(code=destination_code).first()
            if destination_code
            else Country.objects.filter(code=destination_country_code).first()
            if destination_country_code
            else None
        )
        context.update({"destination": destination})
        return context

    def get_queryset(self):
        destination_code = self.kwargs.get("destination")
        destination_country_code = self.kwargs.get("destination_country")
        offer_filter = Q(is_archived=False)
        if destination_country_code:
            offer_filter &= Q(trip__destination__country__code=destination_country_code)
        elif destination_code:
            offer_filter &= Q(trip__destination__code=destination_code)

        # calculate median price over all entries with same destination in same month
        offers_by_destination_and_month = (
            Offer.objects.filter(
                month=OuterRef("month"),
                trip__destination__code=OuterRef("trip__destination__code"),
                trip__trip_type=OuterRef("trip__trip_type"),
                trip__travel_class=OuterRef("trip__travel_class"),
                price_in_eur__isnull=False,
            )
            .values("month", "trip__destination__code")
            .annotate(median_price=Median("price_in_eur", output_field=MoneyOutputField()))
        )

        return (
            Offer.objects.filter(offer_filter)
            .select_related("trip")
            .prefetch_related("trip__origin", "trip__destination", "trip__destination__country")
            .annotate(
                median=Subquery(offers_by_destination_and_month.values("median_price")[:1]),
            )
        )


class TripListView(LoginRequiredMixin, ListView):
    template_name = "trip_list.html"
    model = Trip

    def get_queryset(self):
        trips = Trip.objects.filter(offers__is_archived=False).distinct()

        best_price_offers = (
            Offer.objects.annotate(median=Median("trip__offers__price_in_eur", output_field=MoneyOutputField()))
            .filter(is_archived=False)
            .annotate(min_price=Min("trip__offers__price_in_eur"))
            .filter(price_in_eur=F("min_price"), price_in_eur__lte=F("median"))
        )

        return trips.select_related("origin", "destination", "destination__country").prefetch_related(
            Prefetch("offers", queryset=best_price_offers, to_attr="best_price_offers"),
        )
