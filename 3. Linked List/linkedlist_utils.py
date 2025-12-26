"""
Linked List Utility Functions
------------------------------
Helper functions for converting between arrays and linked lists.
These are what LeetCode uses internally (but hides from you!).

Use these for:
- Testing your linked list solutions locally
- Understanding how LeetCode processes input/output
"""

# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ================================================
# 1. ARRAY TO LINKED LIST
# ================================================
def array_to_linkedlist(arr):
    """
    Convert an array to a linked list.
    
    Input:  [1, 2, 3, 4, 5]
    Output: head → 1 → 2 → 3 → 4 → 5 → None
    
    Time: O(n)
    Space: O(n)
    """
    if not arr:
        return None
    
    # Create head with first element
    head = ListNode(arr[0])
    current = head
    
    # Create remaining nodes
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    
    return head


# ================================================
# 2. LINKED LIST TO ARRAY
# ================================================
def linkedlist_to_array(head):
    """
    Convert a linked list to an array.
    
    Input:  head → 1 → 2 → 3 → 4 → 5 → None
    Output: [1, 2, 3, 4, 5]
    
    Time: O(n)
    Space: O(n)
    """
    result = []
    current = head
    
    while current:
        result.append(current.val)
        current = current.next
    
    return result


# ================================================
# 3. CREATE LINKED LIST WITH CYCLE
# ================================================
def create_cycle_list(arr, pos):
    """
    Create a linked list with a cycle at position 'pos'.
    pos = -1 means no cycle.
    
    Input:  [3, 2, 0, -4], pos = 1
    Output: 3 → 2 → 0 → -4
                ↑         ↓
                └─────────┘
    """
    if not arr:
        return None
    
    nodes = [ListNode(val) for val in arr]
    
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # Create cycle if pos is valid
    if 0 <= pos < len(nodes):
        nodes[-1].next = nodes[pos]
    
    return nodes[0]


# ================================================
# 4. PRINT LINKED LIST (for debugging)
# ================================================
def print_linkedlist(head, max_nodes=20):
    """
    Print linked list in readable format.
    Stops after max_nodes to avoid infinite loop if cycle exists.
    """
    result = []
    current = head
    count = 0
    
    while current and count < max_nodes:
        result.append(str(current.val))
        current = current.next
        count += 1
    
    if current:
        result.append("... (cycle or more nodes)")
    else:
        result.append("None")
    
    print(" → ".join(result))


# ================================================
# USAGE EXAMPLES
# ================================================
if __name__ == "__main__":
    print("=" * 50)
    print("LINKED LIST UTILITY FUNCTIONS DEMO")
    print("=" * 50)
    
    # Example 1: Array to Linked List
    print("\n1. Array to Linked List:")
    arr = [1, 2, 3, 4, 5]
    print(f"   Input array: {arr}")
    head = array_to_linkedlist(arr)
    print("   Output: ", end="")
    print_linkedlist(head)
    
    # Example 2: Linked List to Array
    print("\n2. Linked List to Array:")
    output = linkedlist_to_array(head)
    print(f"   Output array: {output}")
    
    # Example 3: Create Cycle List
    print("\n3. Create Linked List with Cycle:")
    cycle_head = create_cycle_list([3, 2, 0, -4], pos=1)
    print("   Input: [3, 2, 0, -4], pos=1")
    print("   Output: ", end="")
    print_linkedlist(cycle_head)
    
    # Example 4: No Cycle
    print("\n4. Create Linked List without Cycle:")
    no_cycle_head = create_cycle_list([1, 2, 3], pos=-1)
    print("   Input: [1, 2, 3], pos=-1")
    print("   Output: ", end="")
    print_linkedlist(no_cycle_head)
    

