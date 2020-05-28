# Product of Array Except Self
# Given an array nums of n integers where n > 1, 
# return an #array output such that output[i] is equal to the product of all the elements of nums except nums[i].
# Input:  [1,2,3,4]
# Output: [24,12,8,6]

# left and right product -> O(1) space
# 1 2 3 4 ->  2 3 4
# 1 2 3 4 -> 1  3 4
# 1 2 3 4 -> 1 2  4
# 1 2 3 4 -> 1 2 3

def productExceptSelf(nums):
  n = len(nums)
  ans = [0] * n
  
  ans[0] = 1
  for i in range(1, n):
    ans[i] = ans[i-1] * nums[i-1]
    
  p = 1
  for i in range(n-1, -1, -1):
    ans[i] = ans[i] * p
    p *= nums[i]
  return ans
