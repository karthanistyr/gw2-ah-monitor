import math

def mod(dividend, divisor):
    """
    Returns both the result of the integer division of dividend by divisor
    as well as the result of the modulo operation.

    Only supports positive values for both divisor and dividend.

    Arguments:
    dividend -- the dividend of the mod operation
    divisor -- the divisor of the mod operation
    """

    if(dividend < 0 or divisor < 0):
        raise ValueError("Both dividend and divisor must be positive values.")

    integer_division_result = math.floor(dividend/divisor)
    mod_result = dividend % divisor

    return (integer_division_result, mod_result)
