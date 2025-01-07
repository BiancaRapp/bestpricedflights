import json
from datetime import timedelta
from pathlib import Path

from django.test import TestCase
from django.utils.timezone import now
from djmoney.money import Money

from bestpricedflights.apps.core.archiver import archive_unavailable_offers
from bestpricedflights.apps.core.choices import TravelClass, TripType
from bestpricedflights.apps.core.lufthansa.offers_parser import parse_response_and_store_offers
from bestpricedflights.apps.core.models import City, Country, Offer, Trip
from bestpricedflights.apps.core.tests.factories import OfferFactory, TripFactory


class LufthansaTestCase(TestCase):
    def test_parse_and_store_lufthansa_response(self):
        file_path = Path(__file__).parent / "example_data" / "lufthansa" / "STR_B_RETURN.json"

        with file_path.open() as file:
            destination_offers_response = json.load(file)

        parse_response_and_store_offers(destination_offers_response, "STR", TravelClass.BUSINESS, TripType.RETURN)
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
            fetched_on=now().date(),
        )
        self.assertTrue(trip.exists())
        self.assertEqual(trip.count(), 1)

        january_offer = Offer.objects.filter(
            trip=trip.first(), month=1, is_archived=False, price=Money(3344.46, "EUR"), stopovers=1
        )
        self.assertTrue(january_offer.exists())
        self.assertEqual(january_offer.count(), 1)

    def test_archive_unavailable_offers(self):
        unavailable_trip = TripFactory(
            origin__code="STR", destination__code="SYD", fetched_on=now().date() - timedelta(days=1)
        )
        unavailable_offer = OfferFactory(trip=unavailable_trip)

        available_trip = TripFactory(origin__code="STR", destination__code="NBO", fetched_on=now().date())
        previous_offer = OfferFactory(trip=available_trip)
        previous_offer.created_at = now() - timedelta(days=1)
        previous_offer.save()
        new_offer = OfferFactory(trip=available_trip)

        trip_with_different_travel_class = TripFactory(
            origin__code="STR",
            destination__code="NBO",
            travel_class=TravelClass.FIRST,
            fetched_on=now().date() - timedelta(days=1),
        )
        different_travel_class_offer = OfferFactory(trip=trip_with_different_travel_class)

        archive_unavailable_offers("STR", TravelClass.BUSINESS, TripType.RETURN)

        unavailable_offer.refresh_from_db()
        previous_offer.refresh_from_db()
        new_offer.refresh_from_db()
        different_travel_class_offer.refresh_from_db()

        self.assertTrue(unavailable_offer.is_archived)
        self.assertTrue(previous_offer.is_archived)
        self.assertFalse(new_offer.is_archived)
        self.assertFalse(different_travel_class_offer.is_archived)
