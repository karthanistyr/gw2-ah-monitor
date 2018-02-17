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

    def store_price_points(self, price_points):
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
