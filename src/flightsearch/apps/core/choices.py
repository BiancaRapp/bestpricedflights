from django.db import models


class TravelClass(models.TextChoices):
    ECONOMY = "E"
    PREMIUM_ECONOMY = "N"
    BUSINESS = "B"
    FIRST = "F"


class TripType(models.TextChoices):
    RETURN = "RETURN"
    ONEWAY = "ONEWAY"
