from django.urls import path

from flightsearch.apps.core.views import search_flights

urlpatterns = [
    path("search/<str:origin>/<str:travel_class>/<str:trip_type>", search_flights),
    path("search/<str:origin>/<str:travel_class>/", search_flights),
    path("search/<str:origin>/", search_flights),
]
