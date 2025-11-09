
def three_sum_brute_force(nums):
    """
    Finds all unique triplets in a list of integers that sum to zero.

    Args:
        nums: A list of integers.

    Returns:
        A list of unique triplets (lists of three integers) that sum to zero.
    """
    n = len(nums)
    result = []
    nums.sort()  # Sort the input list to handle duplicates efficiently
    for i in range(n - 2):
        # Skip duplicate elements for the first number of the triplet
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        for j in range(i + 1, n - 1):
            # Skip duplicate elements for the second number of the triplet
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            for k in range(j + 1, n):
                # Skip duplicate elements for the third number of the triplet
                if k > j + 1 and nums[k] == nums[k - 1]:
                    continue
                # Check if the sum of the triplet is zero
                if nums[i] + nums[j] + nums[k] == 0:
                    triplet = [nums[i], nums[j], nums[k]]
                    result.append(triplet)
    return result

# Assertions to test the function
assert three_sum_brute_force([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]], "Test Case 1 Failed"
assert three_sum_brute_force([]) == [], "Test Case 2 Failed: Empty list"
assert three_sum_brute_force([0]) == [], "Test Case 3 Failed: Single element list"
assert three_sum_brute_force([0, 0, 0]) == [[0, 0, 0]], "Test Case 4 Failed: All zeros"
assert three_sum_brute_force([1, 2, 3]) == [], "Test Case 5 Failed: No solution"
assert three_sum_brute_force([-1, 0, 1, 0]) == [[-1, 0, 1]], "Test Case 6 Failed: Duplicate elements"
assert three_sum_brute_force([-2, 0, 1, 1, 2]) == [[-2, 0, 2], [-2, 1, 1]], "Test Case 7 Failed: Multiple solutions with duplicates"
