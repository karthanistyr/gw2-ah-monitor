import urllib.parse
from .exceptions import ClientError, DatasourceError
from .datasource import RequestsDatasource

class Client:

    base_api_endpoint_address = "https://api.guildwars2.com/v2/"

    def __init__(self, datasource=RequestsDatasource()):
        self.datasource = datasource

    def _get(self, endpoint_address, arguments=None, api_key=None):
        """Issues a get request to the specified endpoint"""

        fully_qualified_endpoint_address = urllib.parse.urljoin(
            Client.base_api_endpoint_address, endpoint_address)

        headers = None
        if(api_key is not None):
            headers = {"Authorization": "Bearer {}".format(api_key)}

        return self.datasource.get(fully_qualified_endpoint_address, arguments,
            headers)

    def get_json(self, endpoint_address, arguments=None, api_key=None):
        """Gets data from an endpoint and returns a json object
        from the data returned"""

        try:
            response = self._get(endpoint_address, arguments, api_key)
            return response.as_json()
        except DatasourceError as dserr:
            raise ClientError("The client failed to retrieve the " +
                "data.") from dserr
