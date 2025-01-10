import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from bestpricedflights.apps.core.models import City


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    preferred_origin_city = models.ForeignKey(
        City, related_name="preferred_by_users", on_delete=models.SET_NULL, null=True, blank=True
    )

