# best price search

## Project description

### Current State

The program fetches destination offers from lufthansa for different origins in europe for business class return flights. 
The user can list the best price offers over all months and is able to filter the offers for a destination or country on <http://localhost:8000/list/trips/>.
When visiting `http://localhost:8000/list/destinations/<CODE>`, it displays a list of all offers for a specific destination <CODE>.


### Motivation

When searching for cheap flights, it is best to be flexible. That counts for travel dates as well as destination.
For instance if you want to travel to Australia, you better not limit your search to Sydney as destination 
but as well to Melbourne, Perth, Brisbane,...

This proof-of-concept is going one step further:
Sometimes there are offers from within other european cities for the same destination that are significantly cheaper.
Why is that? Airlines such as Lufthansa give out offers to countries, where competing airlines are operating.
So it could be that starting from Amsterdam, you get a much lower price than starting your trip from Frankfurt.

Here and there prices differ by several hundred euros up to thousands of euros on business class flights.
Reaching those price savings may be worth to travel to another city first to start off there.

### Process
The program should find out, when flights from a different origin are cheaper than my main city.

Starting off with just Lufthansa for now, it is using the "Destination Finder" which lists cheap offers to any destination from a given origin airport. 
The API behind can be used to query all destinations from several airports.

Therefore I'm regularly fetching the results from [Lufthansa](https://www.lufthansa.com/de/de/fluege) for different origins:
Stuttgart, Frankfurt, Munich, Amsterdam, Paris, Copenhagen, Oslo, Budapest, Istanbul and Sofia.

### Output
The webpage lists prices based on the destination rather than origin.
Here you could see instantly whenever a flight is cheaper from another city than yours.
It will list the suggested travel date and compared prices from all other cities.

### Next steps
- Add user accounts with preferred main city setting
- Collect offers from different airlines
- Alerting when best prices are found

## How to start the server locally

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