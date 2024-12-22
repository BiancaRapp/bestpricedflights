from django.contrib import admin

from .models import City, Offer, Trip


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "region")
    list_filter = ("region", "currency")


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("origin", "destination", "travel_class", "trip_type", "is_archived")
    list_filter = ("origin", "destination", "is_archived")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("trip", "price", "trip__origin__currency", "stopovers", "month")
    list_filter = ("trip__origin", "trip__destination", "stopovers", "month")
