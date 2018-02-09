from ...rest.client import Client
from ...rest.datasource import RequestsDatasource
from ...rest.exceptions import ClientError, DatasourceError
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
    def T_get_json_HappyDay(self):
        # arrange
        self.mock_response.setup("as_json").returns(StaticJsonData.valid_json)
        self.mock_datasource.setup("get").returns(self.mock_response.object())
        client = Client(self.mock_datasource.object())

        #act
        json = client.get_json("some path", None, None)

        #assert
        assert json == StaticJsonData.valid_json

    @testmethod
    @Assert.expectexceptiontype(ConnectionError)
    def T_get_json_WhenDataSourceRaisesUnhandled_ExceptionBubbles(self):
        # arrange
        self.mock_datasource.setup("get").throws(ConnectionError)
        client = Client(self.mock_datasource.object())

        # act
        client.get_json("some path", None, None)

    @testmethod
    @Assert.expectexceptiontype(ClientError)
    def T_get_json_WhenDatasourceRaisesHandled_ExceptionWrapped(self):
        # arrange
        self.mock_datasource.setup("get").throws(DatasourceError("Src Error."))
        client = Client(self.mock_datasource.object())

        # act
        client.get_json("some path", None, None)
