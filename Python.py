
import heapq
import sys

# --- �������� ���� (Min-Heap) ---

class MinHeap:
    """
    ���������� Min-Heap � �������������� ������ heapq.
    """

    def __init__(self, items=None):
        """
        �������������� Min-Heap.

        Args:
            items: (optional) ����������� ������ ��� ��������� ������������� ����.
                   ���� �� ������, ��������� ������ ����.
        """
        if items is None:
            self.heap = []
        else:
            self.heap = list(items)
            heapq.heapify(self.heap)  # ����������� ������ � ���� in-place

    def push(self, item):
        """
        ��������� ����� ������� � ����.

        Args:
            item: ������� ��� ����������.
        """
        heapq.heappush(self.heap, item)

    def pop(self):
        """
        ������� � ���������� ���������� ������� �� ����.

        Returns:
            ���������� �������.

        Raises:
            IndexError: ���� ���� �����.
        """
        if not self.heap:
            raise IndexError("pop from an empty heap")
        return heapq.heappop(self.heap)

    def peek(self):
        """
        ���������� ���������� ������� �� ����, �� ������ ���.

        Returns:
            ���������� �������.

        Raises:
            IndexError: ���� ���� �����.
        """
        if not self.heap:
            raise IndexError("peek from an empty heap")
        return self.heap[0]

    def is_empty(self):
        """
        ���������, ����� �� ����.

        Returns:
            True, ���� ���� �����, ����� False.
        """
        return not bool(self.heap)

    def size(self):
        """
        ���������� ������ ����.

        Returns:
            ������ ���� (���������� ���������).
        """
        return len(self.heap)


# --- ���-������� ---

class HashTable:
    """
    ������� ���������� ���-������� � ���������� �������� ������� �������.
    """

    def __init__(self, capacity=11):  # Prime number for better distribution
        """
        �������������� ���-�������.

        Args:
            capacity: (optional) ��������� ������ �������.  ������������� ������� �����.
        """
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]  # ������ ������� (�������)
        self.size = 0

    def _hash(self, key):
        """
        ��������� ���-��� ��� �����.

        Args:
            key: ���� ��� �����������.

        Returns:
            ���-��� �����.
        """
        # ������� ����������� �� ������
        return hash(key) % self.capacity

    def insert(self, key, value):
        """
        ��������� ���� ����-�������� � ���-�������.

        Args:
            key: ����.
            value: ��������.
        """
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)  # ���������� ������������� �����
                return
        self.table[index].append((key, value))
        self.size += 1

    def get(self, key):
        """
        ���������� ��������, ��������� � ������.

        Args:
            key: ���� ��� ������.

        Returns:
            ��������, ��������� � ������, ��� None, ���� ���� �� ������.
        """
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        """
        ������� ���� ����-�������� �� ���-�������.

        Args:
            key: ���� ��� ��������.
        """
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.size -= 1
                return

    def __len__(self):
        """
        ���������� ���������� ��� ����-�������� � ���-�������.

        Returns:
            ���������� ��������� � ���-�������.
        """
        return self.size

    def __contains__(self, key):
        """
        ���������, �������� �� ���-������� ������ ����.

        Args:
            key: ���� ��� ��������.

        Returns:
            True, ���� ���� ���������� � ���-�������, ����� False.
        """
        return self.get(key) is not None


# --- ���� ��������� ---

class FibonacciHeapNode:
    """
    ���� � ���� ���������.
    """

    def __init__(self, key, value=None):
        """
        �������������� ���� ���� ���������.

        Args:
            key: ���� ���� (��������, ������������ ��� ���������).
            value: (optional) ��������, ��������� � �����.
        """
        self.key = key
        self.value = value
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.degree = 0
        self.mark = False

class FibonacciHeap:
    """
    ���������� ���� ���������.
    """

    def __init__(self):
        """
        �������������� ���� ���������.
        """
        self.min_node = None
        self.size = 0

    def insert(self, key, value=None):
        """
        ��������� ����� ���� � ����.

        Args:
            key: ���� ������ ����.
            value: (optional) ��������, ��������� � �����.
        """
        new_node = FibonacciHeapNode(key, value)

        if self.min_node is None:
            self.min_node = new_node
        else:
            self._concatenate(self.min_node, new_node)
            if new_node.key < self.min_node.key:
                self.min_node = new_node

        self.size += 1

    def _concatenate(self, node1, node2):
        """
        ���������� ��� ���� � �������� ���������� ������.

        Args:
            node1: ������ ����.
            node2: ������ ����.
        """
        node1_right = node1.right
        node1.right = node2
        node2.left = node1
        node2_right = node2.right
        node2.right = node1_right
        node1_right.left = node2

    def find_min(self):
        """
        ���������� ����������� ���� ���� (�� ������ ���).

        Returns:
            ����������� ���� ����, ��� None, ���� ���� �����.
        """
        if self.min_node is None:
            return None
        return self.min_node.key, self.min_node.value

    def extract_min(self):
        """
        ������� � ���������� ����������� ���� �� ����.

        Returns:
            ������ (key, value) ������������ ����, ��� None, ���� ���� �����.
        """
        if self.min_node is None:
            return None

        min_node = self.min_node

        # ���������� ����� min_node � �������� ������
        if min_node.child is not None:
            child = min_node.child
            for _ in range(min_node.degree):
                child.parent = None
                child = child.right
            self._concatenate(self.min_node, min_node.child)

        # ������� min_node �� ��������� ������
        left = min_node.left
        right = min_node.right
        left.right = right
        right.left = left

        if min_node == right:  # min_node ��� ������������ ����� � �������� ������
            self.min_node = None
        else:
            self.min_node = right
            self._consolidate()  # �������� consolidate ��� ����������� ��������

        self.size -= 1

        return min_node.key, min_node.value

    def _consolidate(self):
        """
        ���������� ������� ���������� ������� � �������� ������.
        """
        A = [None] * (self.size + 1)  # ������ ��� �������� ���������� �� ������� ������ �������

        nodes = []
        curr = self.min_node
        if curr:
            nodes.append(curr)
            curr = curr.right
            while curr != self.min_node:
                nodes.append(curr)
                curr = curr.right

        for node in nodes:
            x = node
            d = x.degree

            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x  # ����������, ��� x - ������ � ������� ������

                self._heap_link(y, x)
                A[d] = None
                d += 1

            A[d] = x

        self.min_node = None
        for i in range(len(A)):
            if A[i] is not None:
                if self.min_node is None:
                    self.min_node = A[i]
                else:
                    self._concatenate(self.min_node, A[i])
                    if A[i].key < self.min_node.key:
                        self.min_node = A[i]


    def _heap_link(self, y, x):
        """
        ������ ���� 'y' �������� ���� 'x'.

        Args:
            y: ����, ������� ����� ������� ��������.
            x: ����, ������� ������ ���������.
        """
        # ������� y �� ��������� ������
        y.left.right = y.right
        y.right.left = y.left

        # ������ y �������� x
        y.parent = x
        if x.child is None:
            x.child = y
            y.right = y
            y.left = y
        else:
            self._concatenate(x.child, y)

        x.degree += 1
        y.mark = False  # ���������� �������

    def decrease_key(self, node, new_key):
        """
        ��������� ���� ��������� ����.  (������� ������� � ����������� ����).
        � �������� ����������� ����� ������� ����� ���� �� ��� ��������.

        Args:
            node: ����, ���� �������� ����� ���������.
            new_key: ����� �������� �����.

        Raises:
            ValueError: ���� ����� �������� ����� ������ ��������.
        """
        if new_key > node.key:
            raise ValueError("����� ���� ������ ���� ������ ��� ����� ��������")

        node.key = new_key
        parent = node.parent

        if parent is not None and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        if node.key < self.min_node.key:
            self.min_node = node

    def _cut(self, node, parent):
        """
        �������� ���� �� ������ �������� ��� �������� � �������� ��� � �������� ������.

        Args:
            node: ���� ��� ���������.
            parent: �������� ����.
        """

        # ������� node �� ������ �������� parent
        if node.right == node:
            parent.child = None  # node ��� ������������ ��������
        else:
            parent.child = node.right if parent.child == node else parent.child
            node.left.right = node.right
            node.right.left = node.left

        parent.degree -= 1
        node.right = self.min_node
        node.left = self.min_node.left
        self.min_node.left.right = node
        self.min_node.left = node
        node.parent = None
        node.mark = False


    def _cascading_cut(self, node):
        """
        ��������� ��������� �����, ���� �� ����� ��������� ������ ��� ������������ ����.

        Args:
            node: ���� ��� ������ ���������� ���������.
        """

        parent = node.parent
        if parent is not None:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)


    def delete(self, node):
        """
        ������� ���� �� ���� ���������.  (������� ������� � ����������� ����).
        � �������� ����������� ����� ������� ����� ���� �� ��� ��������.
        ���������� ��������� ���� ���� �� ����� ������������� � ��������� �������.

        Args:
            node: ���� ��� ��������.
        """
        self.decrease_key(node, float('-inf'))  # ��������� ���� �� ����� �������������
        self.extract_min()


    def is_empty(self):
        """
        ���������, ����� �� ����.

        Returns:
            True, ���� ���� �����, ����� False.
        """
        return self.min_node is None

    def __len__(self):
        """
        ���������� ���������� ����� � ����.

        Returns:
            ���������� ����� � ����.
        """
        return self.size


# --- ������� ������������� ---

if __name__ == "__main__":
    # --- Min-Heap ---
    print("--- Min-Heap ---")
    min_heap = MinHeap()
    min_heap.push(5)
    min_heap.push(1)
    min_heap.push(9)
    min_heap.push(3)

    print("Min element:", min_heap.peek())  # Output: 1

    while not min_heap.is_empty():
        print("Popped:", min_heap.pop())  # Output: 1, 3, 5, 9

    # --- HashTable ---
    print("\n--- HashTable ---")
    hash_table = HashTable()
    hash_table.insert("apple", 1)
    hash_table.insert("banana", 2)
    hash_table.insert("cherry", 3)

    print("Value of banana:", hash_table.get("banana"))  # Output: 2
    print("Size of hash table:", len(hash_table))  # Output: 3
    print("Contains 'apple':", "apple" in hash_table) # Output: True

    hash_table.delete("banana")
    print("Value of banana after deletion:", hash_table.get("banana"))  # Output: None
    print("Size of hash table after deletion:", len(hash_table))  # Output: 2

    # --- Fibonacci Heap ---
    print("\n--- Fibonacci Heap ---")
    fib_heap = FibonacciHeap()
    fib_heap.insert(5, "A")
    fib_heap.insert(1, "B")
    fib_heap.insert(9, "C")
    fib_heap.insert(3, "D")

    print("Min element:", fib_heap.find_min())  # Output: (1, 'B')

    while not fib_heap.is_empty():
        min_val = fib_heap.extract_min()
        print("Extracted:", min_val)
        #Output: (1, 'B'), (3, 'D'), (5, 'A'), (9, 'C')

    # �������������� ������ ���� ��������� � ����������� ����� � ���������
    fib_heap = FibonacciHeap()
    node1 = fib_heap.insert(5, "A") # insert ���������� None, ����� ������� �������� ��������
    node2 = fib_heap.insert(1, "B")
    node3 = fib_heap.insert(9, "C")
    node4 = fib_heap.insert(3, "D")

    #  ��� ���������� ����� � �������� ��������� *������ � ����*.  
    #  �����  ��������� �������� � ����, *�� �������� ������ �� ����*.  
    #  � �������� ������, ��� ��������� ���������� ����� � ��������, �����
    #  ����������� ������ ��������, ��������, ���-�������, ������������ �������� �� ����.

    #  ������ ��������� decrease_key � delete, �� ������ ����������
    #  ������������������ ��������, ������� ����� ���������.
    print("\nDemonstrating decrease_key and delete (requires node access, not available in this example):")
    print("To use decrease_key/delete, you would need to store the node references during insertion")
    print("and implement a lookup mechanism (e.g., a hash table) to find the node based on its value.")
    #fib_heap.decrease_key(node3, 2)  # This won't work because we don't have a reference to node3
    #fib_heap.delete(node2)  # This won't work because we don't have a reference to node2

