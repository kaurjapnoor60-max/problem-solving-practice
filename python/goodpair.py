# Given an array of integers nums, return the number of good pairs.
# A pair (i, j) is called good if nums[i] == nums[j] and i < j.
# Example 1:
# Input: nums = [1,2,3,1,1,3]
# Output: 4
# Explanation: There are 4 good pairs (0,3), (0,4), (3,4), (2,5) 0-indexed.
# Example 2:
# Input: nums = [1,1,1,1]
# Output: 6
# Explanation: Each pair in the array are good.
def numIdenticalPairs(nums):
    count = 0

    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                count += 1

    return count

n = int(input("Enter number of elements: "))

nums = []
print("Enter elements:")

for i in range(n):
    num = int(input())
    nums.append(num)
ans = numIdenticalPairs(nums)
print("Number of good pairs:", ans)