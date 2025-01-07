import structlog
from django.utils.timezone import now
from djmoney.money import Money

from bestpricedflights.apps.core.business.currency_converter import get_price_in_eur
from bestpricedflights.apps.core.models import City, Country, Offer, Trip

logger = structlog.get_logger()


def parse_response_and_store_offers(destination_offers_response, origin_code, travel_class, trip_type):
    destination_finder_offers = destination_offers_response.get("destinationFinderOffers")
    if len(destination_finder_offers) == 0:
        logger.warning(
            "No destination offers found", origin_code=origin_code, travel_class=travel_class, trip_type=trip_type
        )
        return

    origin_data = destination_offers_response.get("origin")
    origin, _ = City.objects.update_or_create(
        code=origin_code,
        defaults={
            "name": origin_data.get("cityName"),
            "longitude": origin_data.get("cityLongitude"),
            "latitude": origin_data.get("cityLatitude"),
            "is_origin": True,
        },
    )

    fetched_on = now().date()
    currency = destination_offers_response.get("currencyInfo", {}).get("currency")
    for destination_data in destination_finder_offers:
        country, _ = Country.objects.update_or_create(
            code=destination_data.get("countryCode"),
            defaults={"name": destination_data.get("countryName")},
        )
        destination, _ = City.objects.update_or_create(
            code=destination_data.get("city"),
            defaults={
                "name": destination_data.get("cityName"),
                "region": destination_data.get("cityRegion"),
                "country": country,
                "longitude": destination_data.get("cityLongitude"),
                "latitude": destination_data.get("cityLatitude"),
                "is_destination": True,
            },
        )
        trip, _ = Trip.objects.update_or_create(
            origin=origin,
            destination=destination,
            travel_class=travel_class,
            trip_type=trip_type,
            defaults={"fetched_on": fetched_on},
        )
        trip.offers.update(is_archived=True)
        for offer_data in destination_data.get("monthOffers"):
            price = Money(offer_data.get("price"), currency=currency)
            price_in_eur = get_price_in_eur(price)
            Offer.objects.create(
                trip=trip,
                month=int(offer_data.get("month")),
                price=price,
                stopovers=offer_data.get("numberOfStopovers", 0),
                price_in_eur=price_in_eur,
            )
