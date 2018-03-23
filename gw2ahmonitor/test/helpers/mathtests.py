from ..fixture import TestClassBase, testmethod
from ...helpers.asserts import Assert
from ...helpers.math import *

class MathTests(TestClassBase):

    @testmethod
    def T_mod_12by3_Returns_4_0(self):
        # arrange
        expected_result = 4
        expected_rest = 0
        divisor = 3
        dividend = 12
        # act
        res = mod(dividend, divisor)
        # assert
        assert res[0] == expected_result and res[1] == expected_rest

    @testmethod
    def T_mod_10by3_Returns_3_1(self):
        # arrange
        expected_result = 3
        expected_rest = 1
        divisor = 3
        dividend = 10
        # act
        res = mod(dividend, divisor)
        # assert
        assert res[0] == expected_result and res[1] == expected_rest

    @testmethod
    def T_mod_2by3_Returns_0_2(self):
        # arrange
        expected_result = 0
        expected_rest = 2
        divisor = 3
        dividend = 2
        # act
        res = mod(dividend, divisor)
        # assert
        assert res[0] == expected_result and res[1] == expected_rest

    @testmethod
    def T_mod_0by3_Returns_0_0(self):
        # arrange
        expected_result = 0
        expected_rest = 0
        divisor = 3
        dividend = 0
        # act
        res = mod(dividend, divisor)
        # assert
        assert res[0] == expected_result and res[1] == expected_rest

    @testmethod
    @Assert.expectexceptiontype(ValueError)
    def T_mod_Min1by3_Throws(self):
        # arrange
        divisor = 3
        dividend = -1
        # act
        res = mod(dividend, divisor)

    @testmethod
    @Assert.expectexceptiontype(ValueError)
    def T_mod_1byMin3_Throws(self):
        # arrange
        divisor = -3
        dividend = 1
        # act
        res = mod(dividend, divisor)

    @testmethod
    @Assert.expectexceptiontype(ValueError)
    def T_mod_Min1byMin3_Throws(self):
        # arrange
        divisor = -3
        dividend = -1
        # act
        res = mod(dividend, divisor)

    @testmethod
    @Assert.expectexceptiontype(ZeroDivisionError)
    def T_mod_1by0_Throws(self):
        # arrange
        divisor = 0
        dividend = 1
        # act
        res = mod(dividend, divisor)
