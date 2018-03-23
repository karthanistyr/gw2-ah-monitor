from ...rest.client import Client
from ...rest.datasource import RequestsDatasource
from ...helpers.exception import ClientError, DatasourceError
from ...helpers.asserts import Assert
from ..fixture import TestClassBase, testmethod
from ..mock import Mock, MockMode
from requests.exceptions import HTTPError

class StaticJsonData:
    invalid_json = "{""this is invalid_json"": ""an invalid json value"""
    valid_json = "{""this is valid_json"": ""an valid json value""}"

class ClientTests(TestClassBase):

    def test_method_init(self):
        self.mock_datasource = Mock(RequestsDatasource, MockMode.Strict)
        self.mock_response = Mock(RequestsDatasource.Response, MockMode.Strict)

    @testmethod
    def T_ctor_DefaultDatasourceType(self):
        # act
        client = Client()
        # assert
        assert isinstance(client.datasource, RequestsDatasource)

    @testmethod
    def T_ctor_CustomDatasourceType(self):
        class CustomDataSource:
            pass
        # act
        client = Client(CustomDataSource())
        # assert
        assert isinstance(client.datasource, CustomDataSource)

    @testmethod
    def T_get_json_HappyDay(self):
        # arrange
        self.mock_response.setup("as_json").returns(StaticJsonData.valid_json)
        self.mock_datasource.setup("get").returns(self.mock_response.object())
        client = Client(self.mock_datasource.object())
        # act
        json = client.get_json("some path", None, None)
        # assert
        assert json == StaticJsonData.valid_json

    @testmethod
    @Assert.expectexceptiontype(ClientError)
    def T_get_json_WhenResponseThrowsDatasourceError_WrapException(self):
        # arrange
        self.mock_response.setup("as_json").throws(DatasourceError("invalid"))
        self.mock_datasource.setup("get").returns(self.mock_response.object())
        client = Client(self.mock_datasource.object())
        # act
        json = client.get_json("some path", None, None)

    @testmethod
    @Assert.expectexceptiontype(ClientError)
    def T_get_json_WhenDatasourceThrowsDatasourceError_ExceptionWrapped(self):
        # arrange
        self.mock_datasource.setup("get").throws(DatasourceError("Src Error."))
        client = Client(self.mock_datasource.object())
        # act
        client.get_json("some path", None, None)

    @testmethod
    @Assert.expectexceptiontype(ConnectionError)
    def T_get_json_WhenDataSourceThrowsUnhandled_ExceptionBubbles(self):
        # arrange
        self.mock_datasource.setup("get").throws(ConnectionError)
        client = Client(self.mock_datasource.object())
        # act
        client.get_json("some path", None, None)

    @testmethod
    def T_get_json_WhenNoArguments_NoApiKey_CorrectArgumentsToBackend(self):
        # arrange
        self.mock_response.setup("as_json").returns(StaticJsonData.valid_json)
        self.mock_datasource.setup("get").returns(self.mock_response.object())
        client = Client(self.mock_datasource.object())
        endpoint_path = "some path"
        expected_url = "{}/{}".format(
            Client.base_api_endpoint_address.strip("/"),
            endpoint_path
            )
        # act
        json = client.get_json(endpoint_path)
        # assert
        assert self.mock_datasource.verify("get").was_called(
            arguments={
                "address": expected_url,
                "params": None,
                "headers": None
                },
            times=1
            )

    @testmethod
    def T_get_json_WhenArguments_NoApiKey_CorrectArgumentsToBackend(self):
        # arrange
        self.mock_response.setup("as_json").returns(StaticJsonData.valid_json)
        self.mock_datasource.setup("get").returns(self.mock_response.object())
        client = Client(self.mock_datasource.object())
        endpoint_path = "some path"
        expected_url = "{}/{}".format(
            Client.base_api_endpoint_address.strip("/"),
            endpoint_path
            )
        call_arguments = {"arg1": "value1", "arg2": "value2"}
        # act
        json = client.get_json(endpoint_path, call_arguments)
        # assert
        assert self.mock_datasource.verify("get").was_called(
            arguments={
                "address": expected_url,
                "params": call_arguments,
                "headers": None
                },
            times=1
            )

    @testmethod
    def T_get_json_WhenArguments_PassApiKey_CorrectArgumentsToBackend(self):
        # arrange
        self.mock_response.setup("as_json").returns(StaticJsonData.valid_json)
        self.mock_datasource.setup("get").returns(self.mock_response.object())
        client = Client(self.mock_datasource.object())
        endpoint_path = "some path"
        expected_url = "{}/{}".format(
            Client.base_api_endpoint_address.strip("/"),
            endpoint_path
            )
        call_arguments = {"arg1": "value1", "arg2": "value2"}
        api_key = "123456APIKEYAPIKEY"
        expected_headers = {"Authorization": "Bearer {}".format(api_key)}
        # act
        json = client.get_json(endpoint_path, call_arguments, api_key)
        # assert
        assert self.mock_datasource.verify("get").was_called(
            arguments={
                "address": expected_url,
                "params": call_arguments,
                "headers": expected_headers
                },
            times=1
            )
