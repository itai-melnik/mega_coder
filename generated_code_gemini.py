"""
This module provides a function to find two numbers in a list that sum to a target.
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Finds two indices in a list of numbers that add up to a target value.

    Args:
        nums: A list of integers.
        target: The target integer sum.

    Returns:
        A list containing the indices of the two numbers that sum to the
        target. Returns an empty list if no such pair is found.
    """
    num_map = {}  # Dictionary to store number: index pairs
    for index, num in enumerate(nums):
        complement = target - num
        # Check if the complement exists in the map
        if complement in num_map:
            # If found, return the indices of complement and current number
            return [num_map[complement], index]
        # Add the current number and its index to the map
        num_map[num] = index
    # Return an empty list if no solution is found
    return []


# Assertions for testing
assert two_sum([2, 7, 11, 15], 9) == [0, 1], "Test Case 1 Failed"
assert two_sum([3, 2, 4], 6) == [1, 2], "Test Case 2 Failed"
assert two_sum([3, 3], 6) == [0, 1], "Test Case 3 Failed"
assert two_sum([0, 4, 3, 0], 0) == [0, 3], "Test Case 4 Failed"
assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4], "Test Case 5 Failed"
assert two_sum([1, 5, 9, 13, 17], 22) == [2, 3], "Test Case 6 Failed"
assert not two_sum([1, 2, 3, 4, 5], 10), "Test Case 7 Failed: No solution"
assert not two_sum([], 5), "Test Case 8 Failed: Empty list"
assert not two_sum([1], 1), "Test Case 9 Failed: Single element list"
