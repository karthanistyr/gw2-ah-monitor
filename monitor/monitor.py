import asyncio
from ..helpers.math   import mod
from ..rest.endpoints import PricesEndpoint

class Monitor:
    def __init__(self, batch_size=200):
        self.batch_size = batch_size

    def get_items_count(self):
        return len(PricesEndpoint().prepare_call().execute())

    async def insert_calls_in_loop(self, event_loop, calls):
        if(calls is None or len(calls) == 0):
            raise ValueError("There should be at least one call passed here.")

        futures = [event_loop.run_in_executor(executor=None, func=call.execute)
            for call in calls]

        return [await future for future in futures]

    def refresh_prices(self):
        el = asyncio.get_event_loop()

        items_count = self.get_items_count()
        nb_calls_variables = mod(items_count, self.batch_size)

        nb_calls = nb_calls_variables[0] if nb_calls_variables[1] == 0 \
            else nb_calls_variables[0] + 1

        ep = PricesEndpoint()
        calls = [ep.prepare_call({"page_size": self.batch_size,
            "page": i})
            for i in range(0, nb_calls)]

        rslt = el.run_until_complete(self.insert_calls_in_loop(el, calls))

        print(len(rslt))
