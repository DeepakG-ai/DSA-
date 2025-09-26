class Node:
    def __init__(self,data):
        self.data = data
        self.next = None


head = Node(10)
A=Node(20)
B = Node(30)
C= Node(40)
D= Node(50)


head.next = A  #shows the data in object. similiar to access object.attributes
A.next = B
B.next=C
C.next=D
print(head) #address of object
print(head.data) #shows the data in object. similiar to access object.attributes
print(A)
print(A.data)  #accessing the data in the class
print(A.next)  #address of memory <__main__.Node object at 0x000002897C594F50>
print(A.next.data)  #o/p -->30
print(D)
print(D.next) #None


class ListNode:
    def __init__(self,data):
        self.data =data
        self.prev = None
        self.next = None


head = ListNode(10)
A=   ListNode(20)
B =   ListNode(30)
C=   ListNode(40)
D=   ListNode(50)

head.next=A
A.prev = head
A.next = B
B.prev= A
B.next =C
C.prev = B
C.next = D
D.prev = C

print("===Doubly Linked List Start===")
print(head) #address of object
print(head.data)
print(A.prev)  # o/p -->head address
print(A) #address of A
print(A.data)  # Data in object A --> 20
print(A.next)  #address of memory <__main__.Node object at 0x000002897C594F50>
print(A.next.data)  #o/p -->30
print(D)
print(D.prev)
print(D.next) #None


def print_list(node):
    while node:
        print(node.data, end=" -> ")
        node = node.next
    print("None")


print_list(head)

# Singly Linked List Implementation

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# Traverse
def traverse(head):
    node = head
    while node:
        print(node.data, end=" -> ")
        node = node.next
    print("None")


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


# Example usage
if __name__ == "__main__":
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


# Doubly Linked List Implementation

class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


# Traverse forward
def traverse_forward(head):
    node = head
    while node:
        print(node.data, end=" <-> ")
        last = node
        node = node.next
    print("None")
    return last


# Traverse backward
def traverse_backward(tail):
    node = tail
    while node:
        print(node.data, end=" <-> ")
        node = node.prev
    print("None")


# Insert at beginning
def insert_at_beginning(head, data):
    new_node = DNode(data)
    if head:
        new_node.next = head
        head.prev = new_node
    return new_node


# Insert at end
def insert_at_end(head, data):
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
def delete_node(head, key):
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
def pop_last(head):
    if not head:
        return None
    if not head.next:
        return None
    node = head
    while node.next:
        node = node.next
    node.prev.next = None
    return head


# Example usage
if __name__ == "__main__":
    head = DNode(10)
    head = insert_at_end(head, 20)
    head = insert_at_end(head, 30)
    traverse_forward(head)  # 10 <-> 20 <-> 30 <-> None

    head = insert_at_beginning(head, 5)
    traverse_forward(head)  # 5 <-> 10 <-> 20 <-> 30 <-> None

    tail = traverse_forward(head)
    traverse_backward(tail)  # 30 <-> 20 <-> 10 <-> 5 <-> None

    head = delete_node(head, 20)
    traverse_forward(head)  # 5 <-> 10 <-> 30 <-> None

    head = pop_last(head)
    traverse_forward(head)  # 5 <-> 10 <-> None

