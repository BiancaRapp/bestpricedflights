from django.db import models


class TravelClass(models.TextChoices):
    ECONOMY = "E", "Economy"
    PREMIUM_ECONOMY = "N", "Premium Economy"
    BUSINESS = "B", "Business"
    FIRST = "F", "First"


class TripType(models.TextChoices):
    RETURN = "RETURN"
    ONEWAY = "ONEWAY"


class Month(models.IntegerChoices):
    JANUARY = 1, "Januar"
    FEBRUARY = 2, "Februar"
    MARCH = 3, "März"
    APRIL = 4, "April"
    MAY = 5, "Mai"
    JUNE = 6, "Juni"
    JULY = 7, "Juli"
    AUGUST = 8, "August"
    SEPTEMBER = 9, "September"
    OCTOBER = 10, "Oktober"
    NOVEMBER = 11, "November"
    DECEMBER = 12, "Dezember"
