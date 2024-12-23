from django.contrib import admin

from .models import City, Offer, Trip


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "region")
    list_filter = ("region", "is_origin", "is_destination")


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("origin", "destination", "travel_class", "trip_type", "fetched_on")
    list_filter = ("origin", "destination")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("trip", "price", "stopovers", "month")
    list_filter = ("trip__origin", "trip__destination", "stopovers", "month")
