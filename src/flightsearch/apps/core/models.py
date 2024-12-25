import uuid

import structlog
from django.db import models
from djmoney.contrib.exchange.exceptions import MissingRate
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField

from .choices import Month, TravelClass, TripType

logger = structlog.getLogger(__name__)


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    is_origin = models.BooleanField(default=False)
    is_destination = models.BooleanField(default=False)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fetched_on = models.DateField()
    origin = models.ForeignKey(City, related_name="flights_from", on_delete=models.CASCADE)
    destination = models.ForeignKey(City, related_name="flights_to", on_delete=models.CASCADE)
    travel_class = models.CharField(choices=TravelClass, default=TravelClass.BUSINESS)
    trip_type = models.CharField(choices=TripType, default=TripType.RETURN)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["origin", "destination", "travel_class", "trip_type"], name="unique_flight"
            ),
        )
        ordering = ("destination", "origin", "travel_class", "trip_type")

    def __str__(self):
        return f"{self.origin.code} – {self.destination.code} ({self.get_travel_class_display()})"  # noqa: RUF001


class Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    month = models.IntegerField(choices=Month)
    price = MoneyField(max_digits=12, decimal_places=2, default_currency="EUR")
    stopovers = models.IntegerField(default=0)
    trip = models.ForeignKey(Trip, related_name="offers", on_delete=models.CASCADE)

    class Meta:
        constraints = (models.UniqueConstraint(fields=["trip", "month"], name="unique_offer"),)
        ordering = ("trip", "price", "month")

    def __str__(self):
        return f"{self.trip}: {self.price} ({self.get_month_display()})"

    def get_price_eur(self):
        if self.price_currency != "EUR":
            try:
                usd = convert_money(self.price, "USD")
                return convert_money(usd, "EUR")
            except MissingRate as e:
                logger.exception("Failed to convert price", extra={"exception": e, "object": self})
        return self.price
