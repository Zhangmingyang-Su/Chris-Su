# Binary Search and Follow Up

# 1 classical binary search
# eg. input -> [1, 3, 5, 7, 9], target = 5    output -> 2
def binary_search(array, target):
  if not array:
     return None
  left, right = 0, len(array) - 1
  while left < right:
    mid = left + (right - left) // 2
    if array[mid] < target:
      left = mid + 1
    elif array[mid] > target:
      right = mid - 1
    else:
      return mid
  return None

# 2 2-D binary search
# eg. input -> [[1,2,3],
#               [4,5,6],    target = 5   output -> [1,1]
#               [7,8,9]]
def matrix_search(matrix, target):
  if not matrix:
    return None
  M = len(matrix)
  N = len(matrix[0])
  left, right = 0, M*N - 1
  while left < right:
    mid = left + (right -left) // 2
    row = mid // N
    col = mid % N
    if matrix[row][col] < target:
      left = mid + 1
    elif matrix[row][col] > target:
      right = mid - 1
    else:
      return [row, col]
  return None

# 3 closest elements
# eg. input -> [1, 2, 4, 5, 8], target = 6  output -> 3
def closest(array, target):
  if not array:
    return None
  left, right = 0, len(array) - 1
  while left < right - 1:
    mid = left + (right - left) // 
    if array[mid] < target:
      left = mid
    elif array[mid] > target:
      right = mid
    else:
      return mid
  return left if abs(left - target) < abs(right - target) else right
      
     
   
