import factory

from bestpricedflights.apps.core.tests.factories import CityFactory
from bestpricedflights.apps.user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    preferred_origin_city = factory.SubFactory(CityFactory, is_origin=True)
    password = factory.django.Password(factory.Faker("password", length=16))
