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
