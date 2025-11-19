"""
This module provides a solution to the 3Sum problem.

The 3Sum problem asks to find all unique triplets in a given array of integers
that sum up to zero.

The approach used here is to first sort the input array. Then, for each element,
we use a two-pointer approach on the remaining part of the array to find pairs
that sum up to the negative of the current element. This ensures that the
triplet sums to zero. To handle uniqueness, we skip duplicate elements during
iteration and also ensure that the two-pointer scan doesn't produce duplicate triplets.
"""

from typing import List


def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Finds all unique triplets in the array that sum to zero.

    Args:
        nums: A list of integers.

    Returns:
        A list of lists, where each inner list is a unique triplet
        that sums to zero.

    Raises:
        TypeError: If nums is not a list or contains non-integer elements.
        ValueError: If nums is empty or has less than 3 elements.
    """
    # Input validation
    if not isinstance(nums, list):
        raise TypeError("Input must be a list of integers.")
    if not nums:
        raise ValueError("Input list cannot be empty.")
    # Optimized check for all integers using `all` and a generator expression.
    if not all(isinstance(x, int) for x in nums):
        raise TypeError("All elements in the list must be integers.")
    if len(nums) < 3:
        return []  # Cannot form a triplet with less than 3 elements

    # Sorting the array is a prerequisite for the two-pointer approach.
    # Time complexity: O(N log N)
    nums.sort()
    n = len(nums)
    result: List[List[int]] = []

    # The outer loop iterates up to n-2 because we need at least two
    # elements (left and right pointers) to form a triplet.
    # Time complexity: O(N) for the outer loop.
    for i in range(n - 2):
        # Optimization: Skip duplicate elements for the first number of the triplet.
        # This ensures that we don't consider the same starting number multiple times,
        # thus preventing duplicate triplets originating from the same first element.
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Optimization: If the current number is positive, then any subsequent
        # numbers (since the array is sorted) will also be positive.
        # Therefore, no triplet can sum to zero if the first element is positive.
        if nums[i] > 0:
            break

        # Initialize two pointers: `left` starts just after `i`, and `right` starts
        # at the end of the array.
        left, right = i + 1, n - 1
        # The target sum for the remaining two numbers is the negative of the current number.
        target = -nums[i]

        # The `while` loop uses the two-pointer technique to find pairs that sum to `target`.
        # This inner loop has a time complexity of O(N) because `left` and `right` pointers
        # move towards each other.
        while left < right:
            current_sum = nums[left] + nums[right]

            if current_sum == target:
                # A triplet is found. Add it to the results.
                result.append([nums[i], nums[left], nums[right]])

                # Optimization: Skip duplicate elements for the second number.
                # Move `left` pointer forward while it points to the same element
                # to avoid duplicate triplets with the same `nums[i]` and `nums[left]`.
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Optimization: Skip duplicate elements for the third number.
                # Move `right` pointer backward while it points to the same element
                # to avoid duplicate triplets with the same `nums[i]` and `nums[right]`.
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                # Move both pointers inward to search for the next potential triplet.
                left += 1
                right -= 1
            elif current_sum < target:
                # If the current sum is less than the target, we need a larger sum.
                # Move the `left` pointer to the right to include a larger number.
                left += 1
            else:  # current_sum > target
                # If the current sum is greater than the target, we need a smaller sum.
                # Move the `right` pointer to the left to include a smaller number.
                right -= 1

    # Overall time complexity: O(N log N) for sorting + O(N^2) for the nested loops
    # (outer loop N times, inner two-pointer loop N times) = O(N^2).
    # Space complexity: O(log N) or O(N) depending on the sorting algorithm implementation,
    # plus O(K) for storing K triplets in the result list.
    return result


# Test Cases
def run_tests() -> None:
    """
    Runs test cases for the three_sum function.
    """
    # Test case 1: Standard case with multiple triplets
    nums1 = [-1, 0, 1, 2, -1, -4]
    expected1 = [[-1, -1, 2], [-1, 0, 1]]
    result1 = three_sum(nums1)
    # Sort inner lists for consistent comparison
    sorted_result1 = sorted([sorted(triplet) for triplet in result1])
    sorted_expected1 = sorted([sorted(triplet) for triplet in expected1])
    assert sorted_result1 == sorted_expected1, \
        f"Test Case 1 Failed: Expected {sorted_expected1}, Got {sorted_result1}"
    print("Test Case 1 Passed")

    # Test case 2: No triplets sum to zero
    nums2 = [1, 2, 3, 4, 5]
    expected2: List[List[int]] = []
    result2 = three_sum(nums2)
    assert result2 == expected2, \
        f"Test Case 2 Failed: Expected {expected2}, Got {result2}"
    print("Test Case 2 Passed")

    # Test case 3: Array with all zeros
    nums3 = [0, 0, 0, 0]
    expected3 = [[0, 0, 0]]
    result3 = three_sum(nums3)
    sorted_result3 = sorted([sorted(triplet) for triplet in result3])
    sorted_expected3 = sorted([sorted(triplet) for triplet in expected3])
    assert sorted_result3 == sorted_expected3, \
        f"Test Case 3 Failed: Expected {sorted_expected3}, Got {sorted_result3}"
    print("Test Case 3 Passed")

    # Test case 4: Array with duplicates and negative numbers
    nums4 = [-2, 0, 0, 2, 2]
    expected4 = [[-2, 0, 2]]
    result4 = three_sum(nums4)
    sorted_result4 = sorted([sorted(triplet) for triplet in result4])
    sorted_expected4 = sorted([sorted(triplet) for triplet in expected4])
    assert sorted_result4 == sorted_expected4, \
        f"Test Case 4 Failed: Expected {sorted_expected4}, Got {sorted_result4}"
    print("Test Case 4 Passed")

    # Test case 5: Array with only two elements (should not yield triplets)
    nums5 = [1, -1]
    expected5: List[List[int]] = []
    result5 = three_sum(nums5)
    assert result5 == expected5, \
        f"Test Case 5 Failed: Expected {expected5}, Got {result5}"
    print("Test Case 5 Passed")

    # Test case 6: Array with one element
    nums6 = [0]
    expected6: List[List[int]] = []
    result6 = three_sum(nums6)
    assert result6 == expected6, \
        f"Test Case 6 Failed: Expected {expected6}, Got {result6}"
    print("Test Case 6 Passed")

    # Test case 7: Array with larger numbers
    nums7 = [-4, -1, -1, 0, 1, 2]
    expected7 = [[-1, -1, 2], [-1, 0, 1]]
    result7 = three_sum(nums7)
    sorted_result7 = sorted([sorted(triplet) for triplet in result7])
    sorted_expected7 = sorted([sorted(triplet) for triplet in expected7])
    assert sorted_result7 == sorted_expected7, \
        f"Test Case 7 Failed: Expected {sorted_expected7}, Got {sorted_result7}"
    print("Test Case 7 Passed")

    # Test case 8: Edge case with empty list
    try:
        three_sum([])
        assert False, "Test Case 8 Failed: ValueError not raised for empty list"
    except ValueError:
        print("Test Case 8 Passed (ValueError for empty list)")
    except Exception as e:
        assert False, f"Test Case 8 Failed: Unexpected exception {type(e).__name__}"

    # Test case 9: Edge case with non-list input
    try:
        three_sum("not a list")  # type: ignore
        assert False, "Test Case 9 Failed: TypeError not raised for non-list input"
    except TypeError:
        print("Test Case 9 Passed (TypeError for non-list input)")
    except Exception as e:
        assert False, f"Test Case 9 Failed: Unexpected exception {type(e).__name__}"

    # Test case 10: Edge case with list containing non-integers
    try:
        three_sum([1, 2, "a"])  # type: ignore
        assert False, "Test Case 10 Failed: TypeError not raised for non-integer elements"
    except TypeError:
        print("Test Case 10 Passed (TypeError for non-integer elements)")
    except Exception as e:
        assert False, f"Test Case 10 Failed: Unexpected exception {type(e).__name__}"

    # Test case 11: Array with less than 3 elements
    nums11 = [1, 2]
    expected11: List[List[int]] = []
    result11 = three_sum(nums11)
    assert result11 == expected11, \
        f"Test Case 11 Failed: Expected {expected11}, Got {result11}"
    print("Test Case 11 Passed")


if __name__ == "__main__":
    run_tests()
