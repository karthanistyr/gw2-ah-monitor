from ...rest.client import Client
from ...rest.endpoints import *
from ...helpers.asserts import Assert
from ..fixture import TestClassBase, testmethod
from ..mock import Mock, MockMode

class EndpointCallTests(TestClassBase):

    class CustomError(Exception):
        """Custom exception type to assert on throws
        when running unit tests
        """
        def __init__(self, message):
            super().__init__(message)

    @testmethod
    def T_ctor_WhenArgumentsPassedTheyAreStoredCorrectly(self):
        # arrange
        mock_client = Mock(Client, MockMode.Strict)

        test_ep_address = "some address"
        test_ep_arguments = {"arg1": "test1", "arg2": "test2"}
        test_ep_api_key = "a long api key"
        test_ep_client = mock_client.object()

        ep_call = EndpointCall(endpoint_address=test_ep_address,
            arguments=test_ep_arguments,
            api_key=test_ep_api_key,
            client=test_ep_client)

        # assert
        assert ep_call.endpoint_address == test_ep_address
        assert ep_call.arguments == test_ep_arguments
        assert ep_call.api_key == test_ep_api_key
        assert ep_call.client == test_ep_client

    # TODO: implement a means to track calls to a mocked call and its arguments
    # @testmethod
    # def T_execute_WhenCalledPassesArgumentsToClient(self):
    #     pass

    @testmethod
    def T_execute_WhenCalled_ReturnsJson(self):
        # arrange
        test_response_json = {"thisjsonkey": "thisjsonvalue"}
        mock_client = Mock(Client, MockMode.Strict)
        mock_client.setup("get_json").returns(test_response_json)
        test_ep_client = mock_client.object()

        ep_call = EndpointCall(endpoint_address=None,
            arguments=None,
            api_key=None,
            client=test_ep_client)

        # act
        response = ep_call.execute()

        # assert
        assert response == test_response_json

    @testmethod
    @Assert.expectexceptiontype(CustomError)
    def T_execute_WhenCalledAndExceptionOccurs_RaisesException(self):
        # arrange
        mock_client = Mock(Client, MockMode.Strict)
        mock_client.setup("get_json").throws(EndpointCallTests.CustomError("Failed"))
        test_ep_client = mock_client.object()

        ep_call = EndpointCall(endpoint_address=None,
            arguments=None,
            api_key=None,
            client=test_ep_client)

        # act
        ep_call.execute()

class PaginatedEndpointTests(TestClassBase):

    @testmethod
    def T_ctor_AddressHasLeadingSlash_AddressIsConcatenatedWithRoot(self):
        # arrange
        test_ep_address = "/some_endpoint"
        expected_ep_address = test_ep_address.strip("/")
        #act
        ep = PaginatedEndpoint(address=test_ep_address, valid_arguments=[])

        # assert
        assert ep.address == expected_ep_address

    @testmethod
    def T_ctor_AddressHasTrailingSlash_AddressIsConcatenatedWithRoot(self):
        # arrange
        test_ep_address = "some_endpoint/"
        expected_ep_address = test_ep_address.strip("/")

        #act
        ep = PaginatedEndpoint(address=test_ep_address+"/", valid_arguments=[])

        # assert
        assert ep.address == expected_ep_address

    @testmethod
    def T_ctor_AddressHasBothSlashes_AddressIsConcatenatedWithRoot(self):
        # arrange
        test_ep_address = "/some_endpoint/"
        expected_ep_address = test_ep_address.strip("/")

        #act
        ep = PaginatedEndpoint(address=test_ep_address, valid_arguments=[])

        # assert
        assert ep.address == expected_ep_address

    @testmethod
    def T_ctor_ValidArgsListStoredCorrectly(self):
        # arrange
        test_valid_args = ["arg1", "arg2", "arg3"]

        # act
        ep = PaginatedEndpoint(address="??", valid_arguments=test_valid_args)

        # assert
        assert ep.valid_arguments == test_valid_args

    @testmethod
    @Assert.expectexceptiontype(AssertionError)
    def T_ctor_ValidArgsMustBeList(self):
        # arrange
        test_valid_args = "this is not a list"

        # act
        ep = PaginatedEndpoint(address="??", valid_arguments=test_valid_args)

    @testmethod
    def T_prepare_call_WhenArgListNull_ValidArgsExist_ReturnEndpointCall(self):
        # arrange
        test_valid_args = ["arg1", "arg2"]
        ep = PaginatedEndpoint(address="??", valid_arguments=test_valid_args)

        # act
        ep_call = ep.prepare_call(argument_list=None)

        # assert
        assert type(ep_call) is EndpointCall

    @testmethod
    def T_prepare_call_WhenArgListNull_ValidArgsNotExist_ReturnEndpointCall(self):
        # arrange
        ep = PaginatedEndpoint(address="??", valid_arguments=None)

        # act
        ep_call = ep.prepare_call(argument_list=None)

        # assert
        assert type(ep_call) is EndpointCall

    @testmethod
    def T_prepare_call_WhenArgListExist_NoIllegalArg_ReturnEndpointCall(self):
        # arrange
        test_valid_args = ["arg1", "arg2"]
        passed_args = {"arg1": "arg1_value"}
        ep = PaginatedEndpoint(address="??", valid_arguments=test_valid_args)

        # act
        ep_call = ep.prepare_call(argument_list=passed_args)

        # assert
        assert type(ep_call) is EndpointCall

    @testmethod
    @Assert.expectexceptiontype(ArgumentValidationError)
    def T_prepare_call_WhenArgListIsExist_IllegalArgExist_RaiseException(self):
        # arrange
        test_valid_args = ["arg1", "arg2"]
        passed_args = {"illegal_arg": "arg_value"}
        ep = PaginatedEndpoint(address="??", valid_arguments=test_valid_args)

        # act
        ep_call = ep.prepare_call(argument_list=passed_args)

    @testmethod
    @Assert.expectexceptiontype(ArgumentValidationError)
    def T_prepare_call_WhenPageIsSpecifiedButNotPageSize_ExpectException(self):
        # arrange
        test_valid_args = ["page", "page_size"]
        passed_args = {"page": "arg_value"}
        ep = PaginatedEndpoint(address="??", valid_arguments=test_valid_args)

        # act
        ep_call = ep.prepare_call(argument_list=passed_args)

    @testmethod
    @Assert.expectexceptiontype(ArgumentValidationError)
    def T_prepare_call_WhenPageSizeIsSpecifiedButNotPage_ExpectException(self):
        # arrange
        test_valid_args = ["page", "page_size"]
        passed_args = {"page_size": "arg_value"}
        ep = PaginatedEndpoint(address="??", valid_arguments=test_valid_args)

        # act
        ep_call = ep.prepare_call(argument_list=passed_args)

    @testmethod
    def T_prepare_call_WhenPageAndPageSizeSpecified_ReturnEndpointCall(self):
        # arrange
        test_valid_args = ["page", "page_size"]
        passed_args = {"page": "arg_value", "page_size": "arg_value"}
        ep = PaginatedEndpoint(address="??", valid_arguments=test_valid_args)

        # act
        ep_call = ep.prepare_call(argument_list=passed_args)

        # assert
        assert type(ep_call) is EndpointCall

    @testmethod
    def T_prepare_call_WhenPageAndPageSizeNotSpecified_ReturnEndpointCall(self):
        # arrange
        test_valid_args = ["page", "page_size", "some_other_arg"]
        passed_args = {"some_other_arg": "arg_value"}
        ep = PaginatedEndpoint(address="??", valid_arguments=test_valid_args)

        # act
        ep_call = ep.prepare_call(argument_list=passed_args)

        # assert
        assert type(ep_call) is EndpointCall

class PricesEndpointTests(TestClassBase):

    @testmethod
    def T_ctor_EndpointAddressIsCorrect(self):
        # arrange
        ep = PricesEndpoint()
        expected_address = GW2ApiEndpointAddresses.Prices.strip("/")

        # assert
        assert ep.address == expected_address

    @testmethod
    def T_ctor_ValidArgsListIsCorrect(self):
        # arrange
        ep = PricesEndpoint()
        expected_valid_args = ["ids", "page_size", "page"]

        # assert
        assert ep.valid_arguments == expected_valid_args
