# Vertical Traversal for a Binary Tree
#Given a binary tree, return the vertical order traversal of its nodes' values. (ie, from top to bottom, column by column).
#If two nodes are in the same row and column, the order should be from left to right.
# Input: [3,9,20,null,null,15,7]
#               3
#              / \
#             9  20
#                / \
#              15   7 
#Output:[[9],[3,15],[20],[7]]

from collections import deque, defaultdict
def vertival_traverse(root):
  if not root:
    return []
  collection = defaultdict(list)
  queue = deque([(root, 0)])
  while queue:
    node,count = queue.popleft()
    if node is not None:
      collection[count].append(node.val)
      queue.append((node.left, count - 1))
      queue.append((node.right, count + 1))
  return [collection[x] for x in sorted(collection.key())]


# 2 In a given grid, each cell can have one of three values:
# the value 0 representing an empty cell;
# the value 1 representing a fresh orange;
# the value 2 representing a rotten orange.
# Every minute, any fresh orange that is adjacent (4-directionally) to a rotten orange becomes rotten.
# Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1 instead.

# Input: [[2,1,1],[1,1,0],[0,1,1]]
# Output: 4
from collections import deque
def orangeRotting(grid):
  if not grid:
    return -1
  cnt = 0
  Q = deque([])
  N, M = len(grid), len(grid[0])
  for i in range(N):
    for j in range(M):
      if grid[i][j] == 1:
        cnt += 1
      if grid[i][j] == 2:
        Q.append((i, j))
  res = 0
  while Q:
    next_level = deque([])
    size = len(Q)
    for _ in range(size):
      i, j = Q.popleft()
      for x,y in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
        if 0 <= x < N and 0 <= y < M and grid[x][y] == 1:
          grid[x][y] = 2
          cnt -= 1
          next_level.append((x, y))
    Q = next_level
    res += 1
  return max(0, res - 1) if cnt == 0 else -1
        
        
