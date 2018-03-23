import asyncio
import time
from ..helpers.logging import LoggingHelper
from ..helpers.exception import format_exception
from ..helpers.math import mod
from ..helpers.time import to_iso8601
from ..helpers.session import SessionHelper
from ..rest.endpoints import PricesEndpoint, ItemsEndpoint, ListingsEndpoint
from ..storage.storage import Storage

class DataRefresher:
    def __init__(
            self, batch_size=200,
            endpoint=None,
            storage=None):
        self.batch_size = batch_size
        self.endpoint = endpoint
        self.storage = storage

    async def insert_calls_in_loop(self, event_loop, calls):
        if(calls is None or not any(calls)):
            raise ValueError("There should be at least one call passed here.")

        with SessionHelper():
            futures = [event_loop.run_in_executor(executor=None, func=call.execute)
                for call in calls]
            # this is a 2-level nested for loop to flatten a list of lists
            elems = [element for future in futures for element in (await future)]

        return elems

    def get_items_count(self):
        return len(self.endpoint.prepare_call().execute())

    def get_data(self, additional_arguments = None):
        items_count = self.get_items_count()

        LoggingHelper.info("There are %s listed item types." % items_count)

        nb_calls_variables = mod(items_count, self.batch_size)
        nb_calls = nb_calls_variables[0] if nb_calls_variables[1] == 0 \
            else nb_calls_variables[0] + 1

        LoggingHelper.info("There will be %s API calls to fetch prices."
            % nb_calls)

        calls = []
        for i in range(0, nb_calls):
            args = { "page_size": self.batch_size, "page": i }
            if(additional_arguments is not None):
                args.update(additional_arguments)
            calls.append(self.endpoint.prepare_call(args))

        el = asyncio.new_event_loop()
        data_points = el.run_until_complete(
            self.insert_calls_in_loop(el, calls)
            )

        return data_points

class PriceMonitor(DataRefresher):
    def __init__(
            self, batch_size=200,
            endpoint=PricesEndpoint(),
            storage=Storage()):
        super().__init__(batch_size=batch_size,
            endpoint=endpoint, storage=storage)

    def get_prices(self):
        utc_start_time = to_iso8601(time.gmtime())

        prices = self.get_data()

        # timestamp the retrieved prices - it doesn't have to be very precise
        for price in prices:
            price.update({"time": utc_start_time})
        return prices

    def refresh_and_store(self):
        try:
            prices = self.get_prices()
            self.storage.store_price_points(prices)
        except Exception as e:
            LoggingHelper.error(format_exception(e))
            raise

class ItemListMaintainer(DataRefresher):
    def __init__(
            self, batch_size=200,
            endpoint=ItemsEndpoint(),
            storage=Storage(),
            supported_lang=("fr", "en")):
        super().__init__(batch_size=batch_size,
            endpoint=endpoint, storage=storage)
        self.supported_lang = supported_lang

    def get_items(self):
        raw_data = {}
        for lang in self.supported_lang:
            raw_data[lang] = self.get_data(additional_arguments={"lang": lang})

        items_list = {}
        for lang in raw_data:
            for item in raw_data[lang]:
                if(item["id"] not in items_list):
                    items_list[item["id"]] = {lang: item["name"]}
                else:
                    items_list[item["id"]][lang] = item["name"]

        return [{"id": item, "name": items_list[item]} for item in items_list]

    def refresh_and_store(self):
        try:
            items = self.get_items()
            print(time.perf_counter())
            self.storage.maintain_items_list(items)
            print(time.perf_counter())
        except Exception as e:
            LoggingHelper.error(format_exception(e))
            raise

class ListingsMonitor(DataRefresher):
    def __init__(
            self, batch_size=200,
            endpoint=ListingsEndpoint(),
            storage=Storage()):
        super().__init__(batch_size=batch_size,
            endpoint=endpoint, storage=storage)

    def get_listings(self):
        utc_start_time = to_iso8601(time.gmtime())

        listings = self.get_data()

        # timestamp the retrieved prices - it doesn't have to be very precise
        for listing in listings:
            listing.update({"time": utc_start_time})
        return listings

    def refresh_and_store(self):
        try:
            listings = self.get_listings()
            self.storage.store_listings(listings)
        except Exception as e:
            LoggingHelper.error(format_exception(e))
            raise
