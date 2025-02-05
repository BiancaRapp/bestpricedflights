import factory

from bestpricedflights.apps.core.models import City, Country, Offer, Trip


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country
        django_get_or_create = ("code",)

    code = factory.Faker("country_code")
    name = factory.Faker("country")


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
        django_get_or_create = ("code",)

    code = factory.Faker("lexify", text="???")
    name = factory.Faker("city")
    region = factory.Faker("lexify", text="??")
    country = factory.SubFactory(CountryFactory)


class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trip

    origin = factory.SubFactory(CityFactory, is_origin=True)
    destination = factory.SubFactory(CityFactory, is_destination=True)
    fetched_on = factory.Faker("date")


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Offer

    month = factory.Faker("random_int", min=1, max=12)
    trip = factory.SubFactory(TripFactory)
    price_in_eur = factory.Faker("pydecimal", min_value=100, max_value=10000, right_digits=2)
    price = factory.SelfAttribute("price_in_eur")
