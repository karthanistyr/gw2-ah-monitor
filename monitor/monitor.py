import asyncio
import time
from ..helpers.math import mod
from ..rest.endpoints import PricesEndpoint
from ..storage.storage import Storage

class Monitor:
    def __init__(
            self, batch_size=200,
            prices_endpoint=PricesEndpoint(),
            storage=Storage()):
        self.batch_size = batch_size
        self.prices_endpoint = prices_endpoint
        self.storage = storage

    def get_items_count(self):
        return len(self.prices_endpoint.prepare_call().execute())

    async def insert_calls_in_loop(self, event_loop, calls):
        if(calls is None or len(calls) == 0):
            raise ValueError("There should be at least one call passed here.")

        futures = [event_loop.run_in_executor(executor=None, func=call.execute)
            for call in calls]

        return [await future for future in futures]

    def get_prices(self):
        el = asyncio.get_event_loop()

        items_count = self.get_items_count()
        nb_calls_variables = mod(items_count, self.batch_size)

        nb_calls = nb_calls_variables[0] if nb_calls_variables[1] == 0 \
            else nb_calls_variables[0] + 1

        calls = [self.prices_endpoint.prepare_call(
            {
                "page_size": self.batch_size,
                "page": i
            }) for i in range(0, nb_calls)]

        rslt = el.run_until_complete(self.insert_calls_in_loop(el, calls))

        return rslt

    def refresh_and_store(self):
        fragmented_prices = None
        try:
            fragmented_prices = self.get_prices()
            self.storage.store_price_points(
                [price for fragment in fragmented_prices for price in fragment]
                )
        except:
            # TODO log exception
            raise
