import structlog
from djmoney.contrib.exchange.exceptions import MissingRate
from djmoney.contrib.exchange.models import convert_money

logger = structlog.get_logger(__name__)


def get_price_in_eur(price):
    if price.currency.code != "EUR":
        try:
            usd = convert_money(price, "USD")
            return convert_money(usd, "EUR")
        except MissingRate as e:
            logger.exception("Failed to convert price", price=price, extra={"exception": e})
            return None
    return price
