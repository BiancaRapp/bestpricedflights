from django.urls import path

from flightsearch.apps.core.views import search_flights

from .views import DestinationListView, TripListView

urlpatterns = [
    path("search/<str:origin>/<str:travel_class>/<str:trip_type>", search_flights),
    path("search/<str:origin>/<str:travel_class>/", search_flights),
    path("search/<str:origin>/", search_flights),
    path("list/destinations/<str:destination>", DestinationListView.as_view()),
    path("list/destinations/", DestinationListView.as_view()),
    path("list/trips/", TripListView.as_view()),
]
