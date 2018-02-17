import math

def mod(dividend, divisor):
    """
    Returns both the result of the integer division of dividend by divisor
    as well as the result of the modulo operation

    Arguments:
    dividend -- the dividend of the mod operation
    divisor -- the divisor of the mod operation
    """

    integer_division_result = math.floor(dividend/divisor)
    mod_result = dividend % divisor

    return (integer_division_result, mod_result)
