import requests

from .choices import TravelClass, TripType


def find_destinations(origin: str, travel_class=TravelClass.BUSINESS, trip_type=TripType.RETURN):
    url = f"https://www.lufthansa.com/service/secured/api/bestprice/destination/finder/{origin}/{travel_class.value}?tripType={trip_type.value}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 "
            "Safari/605.1.15"
        ),
        "Sec-Fetch-Dest": "empty",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Portal-Site": "DE",
        "X-Portal-Language": "de",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()
