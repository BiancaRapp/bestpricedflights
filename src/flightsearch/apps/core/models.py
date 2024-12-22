import uuid

from django.db import models

from .choices import Month, TravelClass, TripType


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=3, blank=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fetched_on = models.DateField()
    origin = models.ForeignKey(City, related_name="flights_from", on_delete=models.CASCADE)
    destination = models.ForeignKey(City, related_name="flights_to", on_delete=models.CASCADE)
    travel_class = models.CharField(choices=TravelClass, default=TravelClass.BUSINESS)
    trip_type = models.CharField(choices=TripType, default=TripType.RETURN)
    is_archived = models.BooleanField(default=False)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["origin", "destination", "travel_class", "trip_type"], name="unique_flight"
            ),
        )

    def __str__(self):
        return f"{self.origin.code} – {self.destination.code} ({self.travel_class})"  # noqa: RUF001


class Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    month = models.IntegerField(choices=Month)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stopovers = models.IntegerField(default=0)
    trip = models.ForeignKey(Trip, related_name="offers", on_delete=models.CASCADE)

    class Meta:
        constraints = (models.UniqueConstraint(fields=["trip", "month"], name="unique_offer"),)

    def __str__(self):
        return f"{self.trip}: {self.price} ({self.month})"
