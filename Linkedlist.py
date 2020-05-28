# reverse LinkedList(iterative)
def reverseLinkedList(head):
  prev = None
  while head:
    next_node = head.next
    head.next = prev
    prev = head
    head = next_node
  return prev

# reverse LinkedList(recursive)
def reverseLinkList(head):
  if head is None or head.next is None:
    return head
  next_node = reverseLinkList(head.next)
  head.next.next = head
  head.next = None
return next_head

# Copy List with Random Pointer
# A linked list is given such that each node contains an additional random pointer 
# which could point to any node in the list or null
# Return a deep copy of the list.
# The Linked List is represented in the input/output as a list of n nodes. 
# Each node is represented as a pair of [val, random_index] where:
# val: an integer representing Node.val
# random_index: the index of the node (range from 0 to n-1) where random pointer points to, 
# or null if it does not point to any node.

class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
        
class Solution:
  def __init__(self):
    self.visitedHashset = {}
    
  def copyRandomList(head):
    if not head:
      return None
    
    if head is self.visitedHashset:
      return self.visitedHashset[head]
    
    # create new node
    node = Node(head.val, None, None)
    
    self.visitedHashset[head] = node
    
    # iterate over all the list to copy
    
    node.next = self.copyRandomList(head.next)
    node.random = self.copyRandomList(head.random)
    return node





