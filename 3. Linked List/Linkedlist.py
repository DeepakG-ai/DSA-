# Node class represents a single element in the linked list
class Node:
    def __init__(self, data):
        self.data = data   # stores the actual data
        self.next = None   # stores reference (address) to the next node


# LinkedList class to manage all linked list operations
class LinkedList:
    def __init__(self):
        self.head = None   # initially list is empty

    # Traverse the list
    def traverse(self):
        node = self.head
        while node:  # traverse till last node. last node is None. so node is False → exits the loop.
            print(node.data, end=" -> ")
            node = node.next
        print("None")

    # Insert at beginning
    def insert_at_beginning(self, data):
        new_node = Node(data)  # create new node
        new_node.next = self.head  # point new node to old head
        self.head = new_node       # update head to new node

    # Insert at end
    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:      # case: empty list
            self.head = new_node
            return

        node = self.head
        while node.next: 
            """
            Condition checks if the next node exists.
            Traverse to last node. next node is None → False → exits the loop.
            That means the loop runs only while there is another node after the current one.
            When you’re at the last node (50) → node.next = None → condition is False → loop stops.
            So you never enter the loop body with node = 50.
            That’s why the last node is skipped inside the loop.
            """
            node = node.next
        node.next = new_node   # attach at end

    # Insert at specific position (0-based index)
    def insert_at_position(self, position, data):
        new_node = Node(data)
        if position == 0:
            new_node.next = self.head
            self.head = new_node
            return

        node = self.head
        for _ in range(position - 1):
            if not node.next:  # if position is greater than length of linked list
                return
            node = node.next
        new_node.next = node.next
        node.next = new_node

    # Delete at beginning
    def delete_at_beginning(self):
        if not self.head:
            return
        self.head = self.head.next  # move head to next node

    # Delete at end
    def delete_at_end(self):
        if not self.head:
            return
        if not self.head.next:  # only one node
            self.head = None
            return

        node = self.head
        while node.next.next:   # stop at last-second node
            node = node.next
        node.next = None        # remove last node

    # Delete at specific position (0-based index)
    def delete_at_position(self, position):
        if not self.head:
            return
        if position == 0:
            self.head = self.head.next
            return

        node = self.head
        for _ in range(position - 1):
            if not node.next:
                return
            node = node.next
        if not node.next:
            return
        node.next = node.next.next


# ------------------- TESTING -------------------

# Create linked list
ll = LinkedList()

# Insert elements
ll.insert_at_end(10)
ll.insert_at_end(20)
ll.insert_at_end(30)
ll.insert_at_end(40)
ll.insert_at_end(50)

print("Initial list:")
ll.traverse()

# Insert at beginning
ll.insert_at_beginning(5)
print("After inserting 5 at beginning:")
ll.traverse()

# Insert at end
ll.insert_at_end(60)
print("After inserting 60 at end:")
ll.traverse()

# Insert at position
ll.insert_at_position(3, 25)
print("After inserting 25 at position 3:")
ll.traverse()

# Delete at beginning
ll.delete_at_beginning()
print("After deleting at beginning:")
ll.traverse()

# Delete at end
ll.delete_at_end()
print("After deleting at end:")
ll.traverse()

# Delete at position
ll.delete_at_position(2)
print("After deleting at position 2:")
ll.traverse()
