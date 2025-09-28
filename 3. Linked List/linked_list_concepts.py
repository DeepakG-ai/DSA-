# Linked List Concepts: Singly and Doubly

# ------------------------
# Singly Linked List
# ------------------------

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Traverse
def traverse(head):
    node = head
    while node:
        print(node.data, end=' -> ')
        node = node.next
    print('None')

# Insert at beginning
def insert_at_beginning(head, data):
    new_node = Node(data)
    new_node.next = head
    return new_node

# Insert at end
def insert_at_end(head, data):
    new_node = Node(data)
    if not head:
        return new_node
    node = head
    while node.next:
        node = node.next
    node.next = new_node
    return head

# Insert after a given node
def insert_after(node, data):
    if not node:
        return
    new_node = Node(data)
    new_node.next = node.next
    node.next = new_node

# Delete by value
def delete_node(head, key):
    if not head:
        return None
    if head.data == key:
        return head.next
    prev, node = None, head
    while node and node.data != key:
        prev, node = node, node.next
    if node:
        prev.next = node.next
    return head

# Pop last node
def pop_last(head):
    if not head:
        return None
    if not head.next:
        return None
    node = head
    while node.next.next:
        node = node.next
    node.next = None
    return head

# Example usage - Singly
head = Node(10)
head = insert_at_end(head, 20)
head = insert_at_end(head, 30)
traverse(head)  # 10 -> 20 -> 30 -> None
head = insert_at_beginning(head, 5)
traverse(head)  # 5 -> 10 -> 20 -> 30 -> None
insert_after(head.next, 15)
traverse(head)  # 5 -> 10 -> 15 -> 20 -> 30 -> None
head = delete_node(head, 20)
traverse(head)  # 5 -> 10 -> 15 -> 30 -> None
head = pop_last(head)
traverse(head)  # 5 -> 10 -> 15 -> None


# ------------------------
# Doubly Linked List
# ------------------------

class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

# Traverse forward
def traverse_forward(head):
    node = head
    while node:
        print(node.data, end=' <-> ')
        last = node
        node = node.next
    print('None')
    return last

# Traverse backward
def traverse_backward(tail):
    node = tail
    while node:
        print(node.data, end=' <-> ')
        node = node.prev
    print('None')

# Insert at beginning
def insert_at_beginning_dll(head, data):
    new_node = DNode(data)
    if head:
        new_node.next = head
        head.prev = new_node
    return new_node

# Insert at end
def insert_at_end_dll(head, data):
    new_node = DNode(data)
    if not head:
        return new_node
    node = head
    while node.next:
        node = node.next
    node.next = new_node
    new_node.prev = node
    return head

# Delete node by value
def delete_node_dll(head, key):
    node = head
    while node and node.data != key:
        node = node.next
    if not node:
        return head
    if node.prev:
        node.prev.next = node.next
    else:
        head = node.next
    if node.next:
        node.next.prev = node.prev
    return head

# Pop last node
def pop_last_dll(head):
    if not head:
        return None
    if not head.next:
        return None
    node = head
    while node.next:
        node = node.next
    node.prev.next = None
    return head

# Example usage - Doubly
head = DNode(10)
head = insert_at_end_dll(head, 20)
head = insert_at_end_dll(head, 30)
traverse_forward(head)  # 10 <-> 20 <-> 30 <-> None
head = insert_at_beginning_dll(head, 5)
traverse_forward(head)  # 5 <-> 10 <-> 20 <-> 30 <-> None
tail = traverse_forward(head)
traverse_backward(tail)  # 30 <-> 20 <-> 10 <-> 5 <-> None
head = delete_node_dll(head, 20)
traverse_forward(head)  # 5 <-> 10 <-> 30 <-> None
head = pop_last_dll(head)
traverse_forward(head)  # 5 <-> 10 <-> None