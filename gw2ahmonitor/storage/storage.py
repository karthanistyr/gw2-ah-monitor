from .backend import BackendBase, MongoDbBackend

class Storage:
    def __init__(self, backend: BackendBase=MongoDbBackend()):
        self.backend = backend

    def _validate_price_point(self, price_point):
        required_toplevel_keys = ("id", "whitelisted", "buys", "sells")
        required_buys_keys = ("unit_price", "quantity")
        required_sells_keys = ("unit_price", "quantity")

        # each key must exist AND yield a value - no null allowed
        for key in required_toplevel_keys:
            if(price_point.get(key, None) is None):
                return False

        for key in required_buys_keys:
            if(price_point["buys"].get(key, None) is None):
                return False

        for key in required_sells_keys:
            if(price_point["sells"].get(key, None) is None):
                return False

        return True

    def _validate_listing(self, listing):
        required_toplevel_keys = ("id", "buys", "sells")
        required_buys_keys = ("listings", "unit_price", "quantity")
        required_sells_keys = ("listings", "unit_price", "quantity")

        # each key must exist AND yield a value - no null allowed
        for key in required_toplevel_keys:
            if(listing.get(key, None) is None):
                return False

        for buy_listing in listing["buys"]:
            for key in required_buys_keys:
                if(buy_listing.get(key, None) is None):
                    return False

        for sell_listing in listing["sells"]:
            for key in required_sells_keys:
                if(sell_listing.get(key, None) is None):
                    return False

        return True

    def _validate_item(self, item):
        required_toplevel_keys = ("id", "name")

        for key in required_toplevel_keys:
            if(item.get(key, None) is None):
                return False

        return True

    def store_price_points(self, price_points):
        """Insert new price_points into storage"""
        error_price_points = []
        valid_price_points = []
        for pp in price_points:
            if(not self._validate_price_point(pp)):
                error_price_points.append(pp)
            else:
                valid_price_points.append(pp)

        if(len(valid_price_points) > 0):
            self.backend.insert("price_point", valid_price_points)
        if(len(error_price_points) > 0):
            # dump the erroneous price points in here for now
            self.backend.insert("price_point_error", error_price_points)

    def store_listings(self, listings):
        """Insert new listings into storage"""
        error_listings = []
        valid_listings = []
        for li in listings:
            if(not self._validate_listing(li)):
                error_listings.append(li)
            else:
                valid_listings.append(li)

        if(len(valid_listings) > 0):
            self.backend.insert("listing", valid_listings)
        if(len(error_listings) > 0):
            # dump the erroneous price points in here for now
            self.backend.insert("listing_error", error_listings)

    def maintain_items_list(self, items):
        """Upsert item information into storage"""
        error_items = []
        valid_items = []
        for item in items:
            if(not self._validate_item(item)):
                error_items.append(item)
            else:
                valid_items.append(item)

        if(len(valid_items) > 0):
            self.backend.upsert("item", valid_items)
        if(len(error_items) > 0):
            # dump the erroneous items in here for now
            self.backend.upsert("item_error", error_items)
