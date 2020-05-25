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
