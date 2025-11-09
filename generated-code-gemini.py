
def twoSum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

nums1 = [2, 7, 11, 15]
target1 = 9
result1 = twoSum(nums1, target1)
assert result1 == [0, 1] or result1 == [1, 0], f"Test Case 1 Failed: Expected [0, 1] or [1, 0], Got {result1}"

nums2 = [3, 2, 4]
target2 = 6
result2 = twoSum(nums2, target2)
assert result2 == [1, 2] or result2 == [2, 1], f"Test Case 2 Failed: Expected [1, 2] or [2, 1], Got {result2}"

nums3 = [3, 3]
target3 = 6
result3 = twoSum(nums3, target3)
assert result3 == [0, 1] or result3 == [1, 0], f"Test Case 3 Failed: Expected [0, 1] or [1, 0], Got {result3}"

nums4 = [1, 5, 9, 13, 2]
target4 = 7
result4 = twoSum(nums4, target4)
assert result4 == [1, 4] or result4 == [4, 1], f"Test Case 4 Failed: Expected [1, 4] or [4, 1], Got {result4}"

nums5 = [-1, -3, 5, 9]
target5 = 4
result5 = twoSum(nums5, target5)
assert result5 == [0, 2] or result5 == [2, 0], f"Test Case 5 Failed: Expected [0, 2] or [2, 0], Got {result5}"

print("All test cases passed!")
