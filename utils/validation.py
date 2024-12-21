def is_monotonic(lst):
    """
    Checks if a list is monotonic (either entirely non-increasing or non-decreasing).

    Args:
        lst (list): List of comparable elements.

    Returns:
        bool: True if monotonic, False otherwise.
    """
    return all(x <= y for x, y in zip(lst, lst[1:])) or all(
        x >= y for x, y in zip(lst, lst[1:])
    )


def within_bounds(lst, lower, upper):
    """
    Checks if all elements in a list are within given bounds.

    Args:
        lst (list): List of elements to check.
        lower (int/float): Lower bound.
        upper (int/float): Upper bound.

    Returns:
        bool: True if all elements are within bounds, False otherwise.
    """
    return all(lower <= abs(x) <= upper for x in lst)


def validate_sequence(report, lower_bound, upper_bound):
    """
    Validates if a report sequence is within bounds and monotonic.

    Args:
        report (list): Sequence of numbers.
        lower_bound (int): Lower bound for differences.
        upper_bound (int): Upper bound for differences.

    Returns:
        bool: True if valid, False otherwise.
    """
    diffs = [x - y for x, y in zip(report, report[1:])]
    return within_bounds(diffs, lower_bound, upper_bound) and is_monotonic(diffs)
