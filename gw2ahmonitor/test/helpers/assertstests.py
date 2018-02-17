from ...helpers.asserts import Assert
from ..fixture import TestClassBase, testmethod

class AssertTests(TestClassBase):

    class CustomError(Exception):
        """Provides a specific exception type to assert on throws"""

        def __init__(self, message):
            super().__init__(message)

    @testmethod
    def T_expectedexceptiontype_WhenExpectedTypeThrown_ReturnsGracefully(self):
        #arrange
        @Assert.expectexceptiontype(AssertTests.CustomError)
        def test_function(self):
            raise AssertTests.CustomError("Expected exception type")

        # act
        test_function(self) # should return gracefully

    @testmethod
    def T_expectedexceptiontype_WhenUnknownTypeThrown_ThrowsAssertError(self):
        #arrange
        @Assert.expectexceptiontype(AssertTests.CustomError)
        def test_function(self):
            raise TypeError("TypeError was unexpected")

        # act
        try:
            test_function(self)
        except AssertionError:
            pass # this is what we wanted

    @testmethod
    def T_expectedexceptiontype_WhenNoExceptionThrown_ThrowsAssertError(self):
        #arrange
        @Assert.expectexceptiontype(AssertTests.CustomError)
        def test_function(self):
            pass # no exception thrown here

        # act
        try:
            test_function(self)
        except AssertionError:
            pass # this is what we wanted
