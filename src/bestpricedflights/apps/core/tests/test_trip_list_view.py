import factory
from django.test import Client, TestCase
from django.utils.timezone import now

from bestpricedflights.apps.core.tests.factories import OfferFactory, TripFactory
from bestpricedflights.apps.user.tests.factories import UserFactory


class TripListTestCase(TestCase):
    def test_trip_list(self):
        user = UserFactory()
        c = Client()
        c.force_login(user)

        my_trip = TripFactory(fetched_on=now().date())
        prices = [100, 200, 300, 400]
        offers = OfferFactory.create_batch(len(prices), trip=my_trip, price_in_eur=factory.Iterator(prices))
        OfferFactory.create(trip=my_trip, price_in_eur=150, is_archived=True)

        response = c.get("/list/trips/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trip_list.html")

        trip_list = response.context_data["trip_list"]
        self.assertQuerySetEqual(trip_list, [my_trip])

        best_price_offers = trip_list.first().best_price_offers
        self.assertEqual(len(best_price_offers), 1)
        self.assertEqual(best_price_offers[0], offers[0])
        self.assertEqual(best_price_offers[0].median.amount, 200)
