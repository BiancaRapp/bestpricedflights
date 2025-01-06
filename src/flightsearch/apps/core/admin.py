from django.contrib import admin

from .models import City, Country, Offer, Trip


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ("code", "name")
    list_display = ("code", "name")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ("code", "name")
    list_display = ("code", "name", "country", "region")
    list_filter = ("country", "region", "is_origin", "is_destination")


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("origin", "destination", "travel_class", "trip_type", "fetched_on", "is_archived")
    list_filter = (
        ("origin", admin.RelatedOnlyFieldListFilter),
        ("destination", admin.RelatedOnlyFieldListFilter),
        "is_archived",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "origin":
            kwargs["queryset"] = City.objects.filter(is_origin=True)
        elif db_field.name == "destination":
            kwargs["queryset"] = City.objects.filter(is_destination=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("trip", "price", "price_in_eur", "stopovers", "month", "is_archived")
    list_filter = (
        ("trip__origin", admin.RelatedOnlyFieldListFilter),
        ("trip__destination", admin.RelatedOnlyFieldListFilter),
        "stopovers",
        "month",
        "is_archived",
    )
