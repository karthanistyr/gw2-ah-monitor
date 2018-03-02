from abc import ABCMeta, abstractmethod
import urllib.parse
from .client import Client
from .exceptions import ArgumentValidationError

class GW2ApiEndpointAddresses:
    Prices = "commerce/prices"
    Items = "items"
    Listings = "commerce/listings"

class EndpointCall:
    def __init__(
            self, endpoint_address,
            arguments, api_key=None,
            client=Client()):
        self.endpoint_address = endpoint_address
        self.arguments = arguments
        self.api_key = api_key
        self.client = client

    def execute(self):
        response = self.client.get_json(self.endpoint_address,
            arguments=self.arguments,
            api_key=self.api_key)
        return response

class BaseEndpoint(metaclass=ABCMeta):
    """Base class for endpoint sub-types"""

    def __init__(self, address, valid_arguments):
        self.address = address.strip("/") # remove leading and trailing slashes

        if(valid_arguments is not None):
            assert type(valid_arguments) is list
        self.valid_arguments = valid_arguments

    @abstractmethod
    def _validate_arguments_specific(self, argument_list):
        pass

    def _validate_arguments(self, argument_list):
        for arg in argument_list:
            if(arg not in self.valid_arguments):
                raise ArgumentValidationError("An unknown argument name for "+
                "this endpoint was passed.", arg)
        self._validate_arguments_specific(argument_list)

    def prepare_call(self, argument_list=None, api_key=None):
        if(argument_list is not None):
            self._validate_arguments(argument_list)
        return EndpointCall(self.address, argument_list, api_key)

class PaginatedEndpoint(BaseEndpoint):
    def __init__(self, address, valid_arguments):
        super().__init__(address, valid_arguments)

    def _validate_arguments_specific(self, argument_list):
        if(not (("page_size" in argument_list
                  and "page" in argument_list)
            or  ("page_size" not in argument_list
                  and "page" not in argument_list))):
                  raise ArgumentValidationError("'page_size' and 'page' must "+
                  "be passed together or not at all.", "page_size")

class PricesEndpoint(PaginatedEndpoint):
    def __init__(self):
        super().__init__(GW2ApiEndpointAddresses.Prices,
            ["ids", "page_size", "page"])

class ItemsEndpoint(PaginatedEndpoint):
    def __init__(self):
        super().__init__(GW2ApiEndpointAddresses.Items,
            ["ids", "lang", "page_size", "page"])

class ListingsEndpoint(PaginatedEndpoint):
    def __init__(self):
        super().__init__(GW2ApiEndpointAddresses.Listings,
            ["ids", "page_size", "page"])
