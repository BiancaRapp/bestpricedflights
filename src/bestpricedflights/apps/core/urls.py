from django.urls import path

from bestpricedflights.apps.core.views import search_flights

from .views import DestinationListView, HomeView, TripListView

urlpatterns = [
    path("", HomeView.as_view()),
    path("search/<str:origin>/<str:travel_class>/<str:trip_type>", search_flights),
    path("search/<str:origin>/<str:travel_class>/", search_flights),
    path("search/<str:origin>/", search_flights),
    path("list/destinations/<str:destination>", DestinationListView.as_view(), name="offers_by_destination_city"),
    path(
        "list/destinations/country/<str:destination_country>",
        DestinationListView.as_view(),
        name="offers_by_destination_country",
    ),
    path("list/trips/", TripListView.as_view()),
]
