import factory
from django.test import Client, TestCase
from django.utils.timezone import now
from moneyed import Money

from .choices import Month, TravelClass
from .factories import OfferFactory, TripFactory


class DestinationListTestCase(TestCase):
    def test_destination_list(self):
        trip1 = TripFactory(fetched_on=now().date())
        trip2 = TripFactory(fetched_on=now().date(), destination=trip1.destination)
        prices = [100, 200, 300, 400, 500]
        OfferFactory.create_batch(
            len(prices),
            trip=factory.Iterator([trip1, trip2]),
            price_in_eur=factory.Iterator(prices),
            month=Month.AUGUST,
            is_archived=True,
        )
        OfferFactory.create(
            trip=TripFactory(fetched_on=now().date(), destination=trip1.destination, travel_class=TravelClass.FIRST),
            price_in_eur=100,
            month=Month.AUGUST,
            is_archived=True,
        )
        offers_for_different_month = OfferFactory.create_batch(
            2,
            trip=factory.Iterator([trip1, trip2]),
            price_in_eur=factory.Iterator([800, 900]),
            month=Month.MAY,
        )
        offers = OfferFactory.create_batch(
            2,
            trip=factory.Iterator([trip1, trip2]),
            price_in_eur=factory.Iterator([600, 700]),
            month=Month.AUGUST,
        )

        c = Client()
        response = c.get(f"/list/destinations/{trip1.destination.code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "destination_list.html")

        offer_list = response.context_data["offer_list"]
        self.assertEqual(response.context_data["destination"], trip1.destination)
        self.assertQuerySetEqual(offer_list, [*offers, *offers_for_different_month], ordered=False)

        for offer in offer_list:
            self.assertEqual(offer.median, Money(400, "EUR") if offer.month == Month.AUGUST else Money(850, "EUR"))


class TripListTestCase(TestCase):
    def test_trip_list(self):
        my_trip = TripFactory(fetched_on=now().date())
        prices = [100, 200, 300, 400]
        offers = OfferFactory.create_batch(len(prices), trip=my_trip, price_in_eur=factory.Iterator(prices))
        OfferFactory.create(trip=my_trip, price_in_eur=150, is_archived=True)

        c = Client()
        response = c.get("/list/trips/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trip_list.html")

        trip_list = response.context_data["trip_list"]
        self.assertQuerySetEqual(trip_list, [my_trip])

        best_price_offers = trip_list.first().best_price_offers
        self.assertEqual(len(best_price_offers), 1)
        self.assertEqual(best_price_offers[0], offers[0])
        self.assertEqual(best_price_offers[0].median.amount, 200)
