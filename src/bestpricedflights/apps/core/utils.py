import requests
import structlog

from .choices import TravelClass, TripType

logger = structlog.get_logger(__name__)


def find_destinations(origin: str, travel_class=TravelClass.BUSINESS.value, trip_type=TripType.RETURN.value):
    logger.debug(
        "Fetching destinations from lufthansa API",
        origin=origin,
        travel_class=travel_class,
        trip_type=trip_type,
    )
    url = f"https://www.lufthansa.com/service/secured/api/bestprice/destination/finder/{origin}/{travel_class}?tripType={trip_type}"

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
    return requests.get(url, headers=headers, timeout=60)
