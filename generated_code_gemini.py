"""
This module solves the "3Sum" problem from LeetCode.

The problem asks to find all unique triplets in a given array of integers
`nums` such that the sum of the three elements equals zero.

Constraints:
- The solution set must not contain duplicate triplets.

Example:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]

Explanation:
- (-1) + 0 + 1 = 0
- (-1) + (-1) + 2 = 0
- 0 + 1 + (-1) = 0

The triplets [-1,0,1] and [0,1,-1] are considered duplicates.
"""

from typing import List, Set, Tuple


def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Finds all unique triplets in the array that sum up to zero.

    This function sorts the input array and then uses a two-pointer
    approach to efficiently find the triplets.

    Args:
        nums: A list of integers.

    Returns:
        A list of lists, where each inner list is a unique triplet
        that sums to zero.

    Raises:
        TypeError: If the input `nums` is not a list.
        ValueError: If the input list contains non-integer elements.
    """
    # Input validation: Early exit for empty or too small lists.
    if not isinstance(nums, list):
        raise TypeError("Input must be a list.")
    if len(nums) < 3:
        return []
    if not all(isinstance(x, int) for x in nums):
        raise ValueError("All elements in the list must be integers.")

    # Sorting the array is crucial for the two-pointer approach and
    # efficient duplicate handling. Time complexity: O(N log N).
    nums.sort()
    n = len(nums)
    # Using a set to store triplets automatically handles uniqueness of triplets.
    # Storing as tuples since lists are not hashable.
    result_set: Set[Tuple[int, int, int]] = set()

    # Iterate through the array. The element at index `i` is fixed as the first
    # element of a potential triplet. We only need to go up to n-3 because
    # we need at least two more elements (left and right pointers).
    for i in range(n - 2):
        # Optimization: If the smallest possible sum using nums[i] (i.e.,
        # nums[i] + nums[i+1] + nums[i+2]) is already greater than 0,
        # then no further triplets can sum to 0, as the array is sorted.
        if nums[i] + nums[i + 1] + nums[i + 2] > 0:
            break

        # Skip duplicate elements for the first number. If the current element
        # is the same as the previous one, we've already processed all unique
        # triplets starting with this value in the previous iteration.
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Initialize two pointers: `left` starts right after `i`, and `right`
        # starts at the end of the array. This forms the "two-pointer" technique.
        left, right = i + 1, n - 1

        # The inner while loop explores pairs for the fixed nums[i].
        # Time complexity of this loop is O(N) for each `i`.
        # Overall time complexity: O(N log N) for sort + O(N^2) for loops = O(N^2).
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]

            if current_sum == 0:
                # Found a triplet that sums to zero. Add it to the set.
                result_set.add((nums[i], nums[left], nums[right]))

                # Move pointers inwards while skipping duplicates for the second
                # and third numbers to find new unique combinations.
                # This avoids redundant checks and ensures we find distinct triplets.
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                # Move both pointers inwards to search for the next potential triplet.
                left += 1
                right -= 1
            elif current_sum < 0:
                # If the sum is too small, we need a larger number.
                # Move the left pointer to the right.
                left += 1
            else:  # current_sum > 0
                # If the sum is too large, we need a smaller number.
                # Move the right pointer to the left.
                right -= 1

    # Convert the set of unique triplets (tuples) back to a list of lists
    # as required by the problem statement.
    return [list(triplet) for triplet in result_set]


# --- Test Cases ---


def test_three_sum():
    """
    Tests the three_sum function with various inputs.
    """

    # Test case 1: Standard input with multiple triplets
    nums1 = [-1, 0, 1, 2, -1, -4]
    expected1 = sorted([[-1, -1, 2], [-1, 0, 1]])
    result1 = sorted(three_sum(nums1))
    assert result1 == expected1, f"Test Case 1 Failed: Expected {expected1}, Got {result1}"
    print("Test Case 1 Passed")

    # Test case 2: No triplets sum to zero
    nums2 = [1, 2, 3, 4, 5]
    expected2 = []
    result2 = sorted(three_sum(nums2))
    assert result2 == expected2, f"Test Case 2 Failed: Expected {expected2}, Got {result2}"
    print("Test Case 2 Passed")

    # Test case 3: Array with all zeros
    nums3 = [0, 0, 0, 0, 0]
    expected3 = [[0, 0, 0]]
    result3 = sorted(three_sum(nums3))
    assert result3 == expected3, f"Test Case 3 Failed: Expected {expected3}, Got {result3}"
    print("Test Case 3 Passed")

    # Test case 4: Array with negative numbers only
    nums4 = [-5, -2, -1, -3, -4]
    expected4 = []  # No combination sums to 0
    result4 = sorted(three_sum(nums4))
    assert result4 == expected4, f"Test Case 4 Failed: Expected {expected4}, Got {result4}"
    print("Test Case 4 Passed")

    # Test case 5: Array with mixed positive and negative, duplicates
    nums5 = [-2, 0, 0, 2, 2]
    expected5 = [[-2, 0, 2]]
    result5 = sorted(three_sum(nums5))
    assert result5 == expected5, f"Test Case 5 Failed: Expected {expected5}, Got {result5}"
    print("Test Case 5 Passed")

    # Test case 6: Empty list
    nums6: List[int] = []
    expected6: List[List[int]] = []
    result6 = sorted(three_sum(nums6))
    assert result6 == expected6, f"Test Case 6 Failed: Expected {expected6}, Got {result6}"
    print("Test Case 6 Passed")

    # Test case 7: List with fewer than 3 elements
    nums7 = [1, 2]
    expected7: List[List[int]] = []
    result7 = sorted(three_sum(nums7))
    assert result7 == expected7, f"Test Case 7 Failed: Expected {expected7}, Got {result7}"
    print("Test Case 7 Passed")

    # Test case 8: Large numbers, potential for overflow (though Python handles large ints)
    nums8 = [-100000, 0, 100000, -50000, 50000]
    expected8 = sorted([[-100000, 0, 100000], [-50000, 0, 50000]])
    result8 = sorted(three_sum(nums8))
    assert result8 == expected8, f"Test Case 8 Failed: Expected {expected8}, Got {result8}"
    print("Test Case 8 Passed")

    # Test case 9: Input validation - not a list
    try:
        three_sum("not a list")  # type: ignore
        assert False, "Test Case 9 Failed: TypeError not raised for non-list input"
    except TypeError:
        print("Test Case 9 Passed (TypeError caught)")

    # Test case 10: Input validation - list with non-integers
    try:
        three_sum([1, 2, "a"])  # type: ignore
        assert False, "Test Case 10 Failed: ValueError not raised for non-integer element"
    except ValueError:
        print("Test Case 10 Passed (ValueError caught)")

    # Test case 11: List with duplicates that form valid triplets
    nums11 = [-1, -1, -1, 0, 0, 1, 1, 2, 2]
    expected11 = sorted([[-1, -1, 2], [-1, 0, 1]])
    result11 = sorted(three_sum(nums11))
    assert result11 == expected11, f"Test Case 11 Failed: Expected {expected11}, Got {result11}"
    print("Test Case 11 Passed")

    # Test case 12: All negative numbers that sum to zero with some positive
    nums12 = [-4, -1, -1, 0, 1, 2]
    expected12 = sorted([[-1, -1, 2], [-1, 0, 1]])
    result12 = sorted(three_sum(nums12))
    assert result12 == expected12, f"Test Case 12 Failed: Expected {expected12}, Got {result12}"
    print("Test Case 12 Passed")


if __name__ == "__main__":
    test_three_sum()
