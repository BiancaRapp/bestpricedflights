import json
from pathlib import Path

from django.test import TestCase
from django.utils.timezone import now
from djmoney.money import Money

from bestpricedflights.apps.core.choices import TravelClass, TripType
from bestpricedflights.apps.core.lufthansa.offers_parser import parse_response_and_store_offers
from bestpricedflights.apps.core.models import City, Country, Offer, Trip


class LufthansaTestCase(TestCase):
    def test_parse_and_store_lufthansa_response(self):
        file_path = Path(__file__).parent / "example_data" / "lufthansa" / "STR_B_RETURN.json"

        with file_path.open() as file:
            destination_offers_response = json.load(file)

        today = now().date()
        parse_response_and_store_offers(
            destination_offers_response, "STR", today, TravelClass.BUSINESS, TripType.RETURN
        )
        self.assertEqual(City.objects.count(), 5)
        self.assertEqual(Country.objects.count(), 4)
        self.assertEqual(Trip.objects.count(), 4)
        self.assertEqual(Offer.objects.count(), 48)

        origin = City.objects.filter(
            code="STR",
            name="Stuttgart",
            region="",
            longitude=9.221964,
            latitude=48.689878,
            is_origin=True,
            is_destination=False,
            country=None,
        )
        self.assertTrue(origin.exists())
        self.assertEqual(origin.count(), 1)

        destination = City.objects.filter(
            code="LAS",
            name="Las Vegas",
            region="NA",
            longitude=-115.143242,
            latitude=36.080608,
            is_origin=False,
            is_destination=True,
            country__code="US",
            country__name="USA",
        )
        self.assertTrue(destination.exists())
        self.assertEqual(destination.count(), 1)

        trip = Trip.objects.filter(
            origin=origin.first(),
            destination=destination.first(),
            travel_class=TravelClass.BUSINESS,
            trip_type=TripType.RETURN,
            fetched_on=today,
        )
        self.assertTrue(trip.exists())
        self.assertEqual(trip.count(), 1)

        january_offer = Offer.objects.filter(
            trip=trip.first(), month=1, is_archived=False, price=Money(3344.46, "EUR"), stopovers=1
        )
        self.assertTrue(january_offer.exists())
        self.assertEqual(january_offer.count(), 1)
