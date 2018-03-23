from ..fixture import TestClassBase, testmethod
from ...helpers.exception import *

class ExceptionTests(TestClassBase):

    @testmethod
    def T_format_exception_FormatsAsString(self):
        # arrange
        exception_object = Exception("An exception message")
        # act
        formatted = format_exception(exception_object)
        # assert
        assert isinstance(formatted, str)

    @testmethod
    def T_ApplicationError_ContainsMessage(self):
        # arrange
        error_message = "An error occurred"
        exception_object = ApplicationError(error_message)
        # assert
        assert str(exception_object) == error_message

    @testmethod
    def T_ClientError_ContainsMessage(self):
        # arrange
        error_message = "An error occurred"
        exception_object = ClientError(error_message)
        # assert
        assert str(exception_object) == error_message

    @testmethod
    def T_DatasourceError_ContainsMessage(self):
        # arrange
        error_message = "An error occurred"
        exception_object = DatasourceError(error_message)
        # assert
        assert str(exception_object) == error_message

    @testmethod
    def T_ArgumentValidationError_ContainsMessage(self):
        # arrange
        error_message = "An error occurred"
        exception_object = ArgumentValidationError(error_message, None)
        # assert
        assert str(exception_object) == error_message

    @testmethod
    def T_ArgumentValidationError_ArgumentNameCorrect(self):
        # arrange
        error_message = "An error occurred"
        argument_name = "arg"
        exception_object = ArgumentValidationError(error_message, argument_name)
        # assert
        assert exception_object.argument_name == argument_name
