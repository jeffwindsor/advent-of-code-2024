def evaluate_expression(nums, operators):
    """
    Evaluates an expression based on numbers and operators.

    Args:
        nums (list): List of numbers.
        operators (list): List of operators corresponding to the numbers.

    Returns:
        int: Result of the evaluated expression.
    """
    result = nums[0]
    for i, operator in enumerate(operators):
        if operator == "+":
            result += nums[i + 1]
        elif operator == "*":
            result *= nums[i + 1]
        elif operator == "||":
            result = int(str(result) + str(nums[i + 1]))
    return result


def modular_arithmetic(base, exp, mod):
    """
    Performs modular arithmetic (base^exp % mod).

    Args:
        base (int): The base number.
        exp (int): The exponent.
        mod (int): The modulus.

    Returns:
        int: Result of the modular operation.
    """
    return pow(base, exp, mod)
