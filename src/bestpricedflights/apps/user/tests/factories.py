import factory

from bestpricedflights.apps.core.tests.factories import CityFactory
from bestpricedflights.apps.user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    preferred_origin_city = factory.SubFactory(CityFactory, is_origin=True)
