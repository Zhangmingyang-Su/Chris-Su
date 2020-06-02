# subarray sums divisible by k
# Given an array A of integers, return the number of (contiguous, non-empty) subarrays that have a sum divisible by K.
# Input: A = [4,5,0,-2,-3,1], K = 5
# Output: 7
# Explanation: There are 7 subarrays with a sum divisible by K = 5:
# [4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]

def subarraysDivByK(array, k):
  preSum = 0
  res = 0
  dic = {}
  for num in array:
    preSum = (preSum + num) % k
    if preSum in dic:
      res += dic[preSum]
      dic[preSum] += 1
    else:
      dic[preSum] = 1
  return res
