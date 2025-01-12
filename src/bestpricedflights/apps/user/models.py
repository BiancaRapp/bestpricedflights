import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from bestpricedflights.apps.core.models import City


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"))
    preferred_origin_city = models.ForeignKey(
        City, related_name="preferred_by_users", on_delete=models.SET_NULL, null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse("edit_profile")
