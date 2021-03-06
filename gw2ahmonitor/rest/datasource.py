import requests
from ..helpers.session import SessionHelper
from ..helpers.exception import DatasourceError

class RequestsDatasource:
    def get(self, address, params, headers):
        try:
            # activate for monitoring in ZAP or fiddler
            # proxies = {
            #     "https": "https://localhost:8080"
            # }

            session = SessionHelper.get_ambient_session()

            if(session is None):
                response = requests.get(address,
                    # activate for monitoring in ZAP or fiddler
                    # proxies=proxies,
                    # verify=False,
                    params=params,
                    headers=headers)
            else:
                response = session.get(address,
                    # activate for monitoring in ZAP or fiddler
                    # proxies=proxies,
                    # verify=False,
                    params=params,
                    headers=headers)
            # only throws when status is not 200 OK
            response.raise_for_status()
            return RequestsDatasource.Response(response)

        except requests.exceptions.HTTPError as httperr:
            try:
                api_error_json = httperr.response.json()
                api_error_code = httperr.response.status_code
                api_error_text = api_error_json.get("text",
                    api_error_json.get("error", "<no error text found.>"))
                raise DatasourceError(message="Code: {}; {}".format(
                    api_error_code, api_error_text)) from httperr
            except ValueError as jsonerr:
                raise DatasourceError("There was a problem extracting " +
                "the error message.") from jsonerr

    class Response:
        def __init__(self, requests_response):
            self.wrapped_response = requests_response

        def as_json(self):
            try:
                return self.wrapped_response.json()
            except ValueError as jsonerr:
                raise DatasourceError("The response body is not valid " +
                "json") from jsonerr
