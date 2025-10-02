
import .util.*;

public class DataStructures {

    // --- Бинарная куча (Min-Heap) ---
    static class MinHeap {
        private ArrayList<Integer> heap;

        public MinHeap() {
            heap = new ArrayList<>();
        }

        public MinHeap(List<Integer> items) {
            heap = new ArrayList<>(items);
            buildHeap();
        }

        private void buildHeap() {
            for (int i = heap.size() / 2 - 1; i >= 0; i--) {
                heapify(i);
            }
        }

        public void push(int item) {
            heap.add(item);
            int i = heap.size() - 1;
            while (i > 0 && heap.get(i) < heap.get((i - 1) / 2)) {
                swap(i, (i - 1) / 2);
                i = (i - 1) / 2;
            }
        }

        public int pop() {
            if (isEmpty()) {
                throw new NoSuchElementException("pop from an empty heap");
            }
            int min = heap.get(0);
            heap.set(0, heap.get(heap.size() - 1));
            heap.remove(heap.size() - 1);
            if (!isEmpty()) {
                heapify(0);
            }
            return min;
        }

        public int peek() {
            if (isEmpty()) {
                throw new NoSuchElementException("peek from an empty heap");
            }
            return heap.get(0);
        }

        private void heapify(int i) {
            int left = 2 * i + 1;
            int right = 2 * i + 2;
            int smallest = i;
            if (left < heap.size() && heap.get(left) < heap.get(smallest)) {
                smallest = left;
            }
            if (right < heap.size() && heap.get(right) < heap.get(smallest)) {
                smallest = right;
            }
            if (smallest != i) {
                swap(i, smallest);
                heapify(smallest);
            }
        }

        private void swap(int i, int j) {
            int temp = heap.get(i);
            heap.set(i, heap.get(j));
            heap.set(j, temp);
        }

        public boolean isEmpty() {
            return heap.isEmpty();
        }

        public int size() {
            return heap.size();
        }
    }


    // --- Хеш-таблица ---
    static class HashTable<K, V> {
        private static final int DEFAULT_CAPACITY = 11; // Prime number
        private LinkedList<Entry<K, V>>[] table;
        private int size;
        private int capacity;

        public HashTable() {
            this(DEFAULT_CAPACITY);
        }

        public HashTable(int capacity) {
            this.capacity = capacity;
            table = new LinkedList[capacity];
            size = 0;
        }

        private int hash(K key) {
            return Math.abs(key.hashCode()) % capacity;
        }

        public void insert(K key, V value) {
            int index = hash(key);
            if (table[index] == null) {
                table[index] = new LinkedList<>();
            }

            for (Entry<K, V> entry : table[index]) {
                if (entry.key.equals(key)) {
                    entry.value = value; // Update existing key
                    return;
                }
            }

            table[index].add(new Entry<>(key, value));
            size++;

            // Optional: Resize table if load factor is too high
            // if ((double) size / capacity > 0.75) {
            //     resize();
            // }
        }

        public V get(K key) {
            int index = hash(key);
            if (table[index] != null) {
                for (Entry<K, V> entry : table[index]) {
                    if (entry.key.equals(key)) {
                        return entry.value;
                    }
                }
            }
            return null;
        }

        public void delete(K key) {
            int index = hash(key);
            if (table[index] != null) {
                Iterator<Entry<K, V>> iterator = table[index].iterator();
                while (iterator.hasNext()) {
                    Entry<K, V> entry = iterator.next();
                    if (entry.key.equals(key)) {
                        iterator.remove();
                        size--;
                        if (table[index].isEmpty()) {
                            table[index] = null; // Avoid memory leak
                        }
                        return;
                    }
                }
            }
        }

        public int size() {
            return size;
        }

        public boolean containsKey(K key) {
            return get(key) != null;
        }

        private void resize() {
            capacity = capacity * 2; // or find the next prime number
            LinkedList<Entry<K, V>>[] oldTable = table;
            table = new LinkedList[capacity];
            size = 0;

            for (LinkedList<Entry<K, V>> list : oldTable) {
                if (list != null) {
                    for (Entry<K, V> entry : list) {
                        insert(entry.key, entry.value);
                    }
                }
            }
        }


        static class Entry<K, V> {
            K key;
            V value;

            public Entry(K key, V value) {
                this.key = key;
                this.value = value;
            }
        }
    }


    // --- Куча Фибоначчи ---
    static class FibonacciHeap {

        private FibonacciHeapNode min;
        private int size;

        public FibonacciHeap() {
            min = null;
            size = 0;
        }

        public FibonacciHeapNode insert(int key, Object value) {
            FibonacciHeapNode node = new FibonacciHeapNode(key, value);

            if (min == null) {
                min = node;
            } else {
                concatenate(min, node);
                if (node.key < min.key) {
                    min = node;
                }
            }
            size++;
            return node;  //Return node for decreaseKey/delete
        }

        private void concatenate(FibonacciHeapNode node1, FibonacciHeapNode node2) {
            FibonacciHeapNode temp = node1.right;
            node1.right = node2.right;
            node2.right.left = node1;
            node2.right = temp;
            temp.left = node2;
        }


        public int findMinKey() {
            if (isEmpty()) {
                throw new NoSuchElementException("Heap is empty");
            }
            return min.key;
        }

        public Object findMinValue() {
             if (isEmpty()) {
                throw new NoSuchElementException("Heap is empty");
            }
            return min.value;
        }

        public Object extractMin() {
            if (min == null) {
                return null;
            }

            FibonacciHeapNode minNode = min;
            Object minValue = minNode.value;

            // Move children of minNode to the root list
            if (minNode.child != null) {
                FibonacciHeapNode child = minNode.child;
                do {
                    FibonacciHeapNode next = child.right; // Store next before detaching

                    child.parent = null;
                    child = next;
                } while (child != minNode.child);
                concatenate(min, minNode.child); // Add children to the root list
            }

            // Remove minNode from the root list
            FibonacciHeapNode left = minNode.left;
            FibonacciHeapNode right = minNode.right;
            left.right = right;
            right.left = left;

            if (minNode == right) { // minNode was the only node in the root list
                min = null;
            } else {
                min = right;
                consolidate(); // Perform consolidation
            }

            size--;
            return minValue;
        }


        private void consolidate() {
            // Calculate the maximum degree (logarithmic to the number of nodes)
            int D = (int) Math.floor(Math.log(size) / Math.log(2)) + 1;
            ArrayList<FibonacciHeapNode> A = new ArrayList<>(D);
             for (int i = 0; i < D; i++) {
                A.add(null);  // Initialize with null
            }

            // Traverse the root list
            FibonacciHeapNode start = min;
            List<FibonacciHeapNode> toVisit = new ArrayList<>();
            FibonacciHeapNode current = start;

            if (current != null) {
                toVisit.add(current);
                current = current.right;
                while (current != start) {
                    toVisit.add(current);
                    current = current.right;
                }
            }

            for (FibonacciHeapNode x : toVisit) {
                int d = x.degree;
                while (A.get(d) != null) {
                    FibonacciHeapNode y = A.get(d);
                    if (x.key > y.key) {
                        // Swap x and y to ensure x has the smaller key
                        FibonacciHeapNode temp = x;
                        x = y;
                        y = temp;
                    }
                    heapLink(y, x);
                    A.set(d, null);
                    d++;

                    if (d >= A.size()) {
                        A.add(null);
                    }
                }
                A.set(d, x);
            }

            // Reset min pointer
            min = null;
            for (FibonacciHeapNode node : A) {
                if (node != null) {
                    if (min == null) {
                        min = node;
                    } else {
                        concatenate(min, node);
                        if (node.key < min.key) {
                            min = node;
                        }
                    }
                }
            }
        }


        private void heapLink(FibonacciHeapNode y, FibonacciHeapNode x) {
            // Remove y from the root list
            y.left.right = y.right;
            y.right.left = y.left;

            // Make y a child of x
            y.parent = x;
            if (x.child == null) {
                x.child = y;
                y.right = y;
                y.left = y;
            } else {
                concatenate(x.child, y);
            }
            x.degree++;
            y.mark = false;
        }


        public void decreaseKey(FibonacciHeapNode node, int newKey) {
            if (newKey > node.key) {
                throw new IllegalArgumentException("New key is greater than current key.");
            }

            node.key = newKey;
            FibonacciHeapNode parent = node.parent;

            if (parent != null && node.key < parent.key) {
                cut(node, parent);
                cascadingCut(parent);
            }

            if (node.key < min.key) {
                min = node;
            }
        }


        private void cut(FibonacciHeapNode node, FibonacciHeapNode parent) {
            // Remove node from parent's child list
            if (node.right == node) { // node was the only child
                parent.child = null;
            } else {
                parent.child = node.right; // Adjust parent's child pointer
                node.left.right = node.right;
                node.right.left = node.left;
            }
            parent.degree--;
            node.parent = null;
            node.mark = false;  // Clear mark bit

            // Add node to the root list
            concatenate(min, node);
            if (node.key < min.key) {
                min = node;
            }
        }


        private void cascadingCut(FibonacciHeapNode node) {
            FibonacciHeapNode parent = node.parent;
            if (parent != null) {
                if (!node.mark) {
                    node.mark = true; // Mark the node
                } else {
                    cut(node, parent);
                    cascadingCut(parent);
                }
            }
        }


       public void delete(FibonacciHeapNode node) {
            decreaseKey(node, Integer.MIN_VALUE); // Make it the min
            extractMin();  // Extract it and remove it
        }



        public boolean isEmpty() {
            return min == null;
        }

        public int size() {
            return size;
        }


        static class FibonacciHeapNode {
            int key;
            Object value;
            FibonacciHeapNode parent;
            FibonacciHeapNode child;
            FibonacciHeapNode left;
            FibonacciHeapNode right;
            int degree;
            boolean mark;

            public FibonacciHeapNode(int key, Object value) {
                this.key = key;
                this.value = value;
                parent = null;
                child = null;
                left = this;
                right = this;
                degree = 0;
                mark = false;
            }
        }
    }



    public static void main(String[] args) {
        // --- Min-Heap Example ---
        System.out.println("--- Min-Heap Example ---");
        MinHeap minHeap = new MinHeap();
        minHeap.push(5);
        minHeap.push(1);
        minHeap.push(9);
        minHeap.push(3);

        System.out.println("Min element: " + minHeap.peek());

        while (!minHeap.isEmpty()) {
            System.out.println("Popped: " + minHeap.pop());
        }

        // --- HashTable Example ---
        System.out.println("\n--- HashTable Example ---");
        HashTable<String, Integer> hashTable = new HashTable<>();
        hashTable.insert("apple", 1);
        hashTable.insert("banana", 2);
        hashTable.insert("cherry", 3);

        System.out.println("Value of banana: " + hashTable.get("banana"));
        System.out.println("Size of hash table: " + hashTable.size());
        System.out.println("Contains 'apple': " + hashTable.containsKey("apple"));

        hashTable.delete("banana");
        System.out.println("Value of banana after deletion: " + hashTable.get("banana"));
        System.out.println("Size of hash table after deletion: " + hashTable.size());

        // --- Fibonacci Heap Example ---
        System.out.println("\n--- Fibonacci Heap Example ---");
        FibonacciHeap fibHeap = new FibonacciHeap();
        FibonacciHeap.FibonacciHeapNode node1 = fibHeap.insert(5, "A");
        FibonacciHeap.FibonacciHeapNode node2 = fibHeap.insert(1, "B");
        FibonacciHeap.FibonacciHeapNode node3 = fibHeap.insert(9, "C");
        FibonacciHeap.FibonacciHeapNode node4 = fibHeap.insert(3, "D");

        System.out.println("Min element: " + fibHeap.findMinKey() + " : " + fibHeap.findMinValue());

        while (!fibHeap.isEmpty()) {
            System.out.println("Extracted: " + fibHeap.extractMin());
        }

        System.out.println("\n--- Fibonacci Heap with decreaseKey/delete Example ---");
        fibHeap = new FibonacciHeap();
        node1 = fibHeap.insert(5, "A");
        node2 = fibHeap.insert(1, "B");
        node3 = fibHeap.insert(9, "C");
        node4 = fibHeap.insert(3, "D");

        fibHeap.decreaseKey(node3, 2); // Decrease key of node with value "C"
        fibHeap.delete(node2);  // Delete node with value "B"

        System.out.println("Min element after decreaseKey and delete: " + fibHeap.findMinKey() + " : " + fibHeap.findMinValue());


        while (!fibHeap.isEmpty()) {
            System.out.println("Extracted: " + fibHeap.extractMin());
        }


    }
}
