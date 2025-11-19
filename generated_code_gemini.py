"""
This module provides a solution to the Two Sum problem.

The Two Sum problem is a classic coding challenge where, given an array
of integers `nums` and an integer `target`, the goal is to find two
indices in the array such that the elements at those indices sum up to
the `target`.

This implementation uses a hash map (dictionary in Python) to achieve
an optimal time complexity of O(n).
"""

from typing import List, Tuple, Dict

# Constants for type checking and error messages
INVALID_NUMS_TYPE_ERROR = "Input 'nums' must be a list of integers."
INVALID_TARGET_TYPE_ERROR = "Input 'target' must be an integer."
EMPTY_NUMS_ERROR = "Input 'nums' cannot be empty."
NO_SOLUTION_FOUND_ERROR = "No two numbers in the list sum up to the target."
DUPLICATE_INDICES_ERROR = "The same element cannot be used twice."


def two_sum(nums: List[int], target: int) -> Tuple[int, int]:
    """
    Finds two indices in a list of integers whose elements sum up to a target.

    This function iterates through the list, and for each element, it checks
    if the complement (target - current_element) exists in a hash map.
    The hash map stores elements seen so far along with their indices.
    If the complement is found, it means we have found the two numbers
    that sum up to the target, and their indices are returned.

    Args:
        nums: A list of integers.
        target: The target integer sum.

    Returns:
        A tuple containing the indices of the two numbers that sum up to the
        target. The order of indices in the tuple does not matter.

    Raises:
        TypeError: If 'nums' is not a list of integers or 'target' is not
                   an integer.
        ValueError: If 'nums' is empty or if no two numbers in the list sum
                    up to the target.
    """
    # Input validation: Check if 'nums' is a list of integers
    if not isinstance(nums, list):
        raise TypeError(INVALID_NUMS_TYPE_ERROR)
    # Optimization: Lazy check for element types within the loop if list is large
    # to avoid upfront O(n) scan if it's not strictly necessary for smaller lists
    # and potentially improve average case if TypeError is rare.
    # However, for robustness and clear error messages, keeping explicit check.
    if not all(isinstance(n, int) for n in nums):
        raise TypeError(INVALID_NUMS_TYPE_ERROR)

    # Input validation: Check if 'target' is an integer
    if not isinstance(target, int):
        raise TypeError(INVALID_TARGET_TYPE_ERROR)

    # Input validation: Check if 'nums' is empty
    if not nums:
        raise ValueError(EMPTY_NUMS_ERROR)

    num_map: Dict[int, int] = {}  # Stores {number: index}

    for index, num in enumerate(nums):
        complement = target - num
        # Check if the complement is already in our map
        # Dictionary lookups are O(1) on average.
        if complement in num_map:
            # Ensure we are not using the same element twice.
            # The check `num_map[complement] != index` is implicit
            # because we add the current `num` to the map *after* checking
            # for its complement. If `complement == num`, then `num_map[complement]`
            # would refer to a previous occurrence of `num`, not the current one.
            # Thus, the explicit check `num_map[complement] != index` is redundant
            # and can be removed for minor performance gain and cleaner code.
            return (num_map[complement], index)
        # Add the current number and its index to the map.
        # This is done after checking for complement to avoid using the same
        # element twice.
        num_map[num] = index

    # If the loop completes without finding a solution
    raise ValueError(NO_SOLUTION_FOUND_ERROR)


# --- Test Cases ---
def run_tests() -> None:
    """
    Runs a suite of test cases to verify the correctness of the two_sum function.
    """
    print("Running tests for two_sum function...")

    # Test case 1: Basic case
    nums1 = [2, 7, 11, 15]
    target1 = 9
    expected1 = (0, 1)
    result1 = two_sum(nums1, target1)
    assert sorted(result1) == sorted(expected1), \
        f"Test 1 Failed: nums={nums1}, target={target1}, Expected={expected1}, Got={result1}"
    print("Test 1 Passed.")

    # Test case 2: Another basic case
    nums2 = [3, 2, 4]
    target2 = 6
    expected2 = (1, 2)
    result2 = two_sum(nums2, target2)
    assert sorted(result2) == sorted(expected2), \
        f"Test 2 Failed: nums={nums2}, target={target2}, Expected={expected2}, Got={result2}"
    print("Test 2 Passed.")

    # Test case 3: List with duplicates, target requires different elements
    nums3 = [3, 3]
    target3 = 6
    expected3 = (0, 1)
    result3 = two_sum(nums3, target3)
    assert sorted(result3) == sorted(expected3), \
        f"Test 3 Failed: nums={nums3}, target={target3}, Expected={expected3}, Got={result3}"
    print("Test 3 Passed.")

    # Test case 4: No solution
    nums4 = [1, 2, 3, 4]
    target4 = 10
    try:
        two_sum(nums4, target4)
        assert False, "Test 4 Failed: Expected ValueError for no solution."
    except ValueError as e:
        assert str(e) == NO_SOLUTION_FOUND_ERROR, \
            f"Test 4 Failed: Incorrect ValueError message: {e}"
    print("Test 4 Passed.")

    # Test case 5: Empty list
    nums5: List[int] = []
    target5 = 5
    try:
        two_sum(nums5, target5)
        assert False, "Test 5 Failed: Expected ValueError for empty list."
    except ValueError as e:
        assert str(e) == EMPTY_NUMS_ERROR, \
            f"Test 5 Failed: Incorrect ValueError message: {e}"
    print("Test 5 Passed.")

    # Test case 6: List with negative numbers
    nums6 = [-1, -2, -3, -4, -5]
    target6 = -8
    expected6 = (2, 4)
    result6 = two_sum(nums6, target6)
    assert sorted(result6) == sorted(expected6), \
        f"Test 6 Failed: nums={nums6}, target={target6}, Expected={expected6}, Got={result6}"
    print("Test 6 Passed.")

    # Test case 7: Target is zero, requires positive and negative numbers
    nums7 = [-3, 4, 3, 90]
    target7 = 0
    expected7 = (0, 2)
    result7 = two_sum(nums7, target7)
    assert sorted(result7) == sorted(expected7), \
        f"Test 7 Failed: nums={nums7}, target={target7}, Expected={expected7}, Got={result7}"
    print("Test 7 Passed.")

    # Test case 8: Large numbers
    nums8 = [1000000, 2000000, 3000000]
    target8 = 3000000
    expected8 = (0, 1)
    result8 = two_sum(nums8, target8)
    assert sorted(result8) == sorted(expected8), \
        f"Test 8 Failed: nums={nums8}, target={target8}, Expected={expected8}, Got={result8}"
    print("Test 8 Passed.")

    # Test case 9: Invalid input type for nums (string)
    try:
        two_sum("not a list", 5)  # type: ignore
        assert False, "Test 9 Failed: Expected TypeError for invalid nums type."
    except TypeError as e:
        assert str(e) == INVALID_NUMS_TYPE_ERROR, \
            f"Test 9 Failed: Incorrect TypeError message: {e}"
    print("Test 9 Passed.")

    # Test case 10: Invalid input type for nums (list of strings)
    try:
        two_sum(["a", "b"], 5)  # type: ignore
        assert False, "Test 10 Failed: Expected TypeError for invalid nums element type."
    except TypeError as e:
        assert str(e) == INVALID_NUMS_TYPE_ERROR, \
            f"Test 10 Failed: Incorrect TypeError message: {e}"
    print("Test 10 Passed.")

    # Test case 11: Invalid input type for target (string)
    try:
        two_sum([1, 2, 3], "5")  # type: ignore
        assert False, "Test 11 Failed: Expected TypeError for invalid target type."
    except TypeError as e:
        assert str(e) == INVALID_TARGET_TYPE_ERROR, \
            f"Test 11 Failed: Incorrect TypeError message: {e}"
    print("Test 11 Passed.")

    # Test case 12: Edge case where the same number appears twice and is the solution
    nums12 = [5, 1, 5, 2]
    target12 = 10
    expected12 = (0, 2)
    result12 = two_sum(nums12, target12)
    assert sorted(result12) == sorted(expected12), \
        f"Test 12 Failed: nums={nums12}, target={target12}, Expected={expected12}, Got={result12}"
    print("Test 12 Passed.")

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
