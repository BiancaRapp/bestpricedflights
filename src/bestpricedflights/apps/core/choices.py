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
    JANUARY = 1, "January"
    FEBRUARY = 2, "February"
    MARCH = 3, "March"
    APRIL = 4, "April"
    MAY = 5, "May"
    JUNE = 6, "June"
    JULY = 7, "July"
    AUGUST = 8, "August"
    SEPTEMBER = 9, "September"
    OCTOBER = 10, "October"
    NOVEMBER = 11, "November"
    DECEMBER = 12, "December"
