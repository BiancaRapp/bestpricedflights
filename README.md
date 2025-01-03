# flightsearch

## Project description

I'd like to find out, if flights from a different origin are cheaper than my main city.

Therefore I'm regularly fetching the results from [Lufthansa](https://www.lufthansa.com/de/de/fluege) for different origins:
Stuttgart, Frankfurt, Munich, Amsterdam, Paris, Copenhagen, Oslo, Budapest, Istanbul and Sofia

## How to start server locally

```shell
docker compose up
```

To update vendor resources call:
```shell
docker compose exec app django-admin collectstatic --no-input
```

To run tests:
```shell
docker compose exec app django-admin test
```

To be able to run the program properly, you need to provide the env `OPEN_EXCHANGE_RATES_APP_ID`. 
You can get your own app id from <https://openexchangerates.org>.