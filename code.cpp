
#include <iostream>
#include <vector>
#include <algorithm>
#include <list>
#include <cmath>
#include <stdexcept>  // For exception handling

// --- Binary Min-Heap ---
class MinHeap {
private:
    std::vector<int> heap;

    // Helper function to heapify a subtree rooted at index i
    void heapify(int i) {
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        int smallest = i;

        if (left < heap.size() && heap[left] < heap[smallest]) {
            smallest = left;
        }

        if (right < heap.size() && heap[right] < heap[smallest]) {
            smallest = right;
        }

        if (smallest != i) {
            std::swap(heap[i], heap[smallest]);
            heapify(smallest);
        }
    }

public:
    MinHeap() {}

    // Constructor to build a heap from an existing vector
    MinHeap(const std::vector<int>& items) : heap(items) {
        for (int i = heap.size() / 2 - 1; i >= 0; --i) {
            heapify(i);
        }
    }

    void push(int item) {
        heap.push_back(item);
        int i = heap.size() - 1;
        while (i > 0 && heap[i] < heap[(i - 1) / 2]) {
            std::swap(heap[i], heap[(i - 1) / 2]);
            i = (i - 1) / 2;
        }
    }

    int pop() {
        if (isEmpty()) {
            throw std::out_of_range("pop from an empty heap");
        }
        int min = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        if (!isEmpty()) {
            heapify(0);
        }
        return min;
    }

    int peek() const {
        if (isEmpty()) {
            throw std::out_of_range("peek from an empty heap");
        }
        return heap[0];
    }

    bool isEmpty() const {
        return heap.empty();
    }

    int size() const {
        return heap.size();
    }
};



// --- Hash Table ---
template <typename K, typename V>
class HashTable {
private:
    static const int DEFAULT_CAPACITY = 11;  // Prime number
    std::list<std::pair<K, V>>* table;
    int size;
    int capacity;

    // Hash function
    int hash(const K& key) const {
        return std::abs(std::hash<K>{}(key)) % capacity;  // C++11 hash
    }

public:
    HashTable(int capacity = DEFAULT_CAPACITY) : capacity(capacity), size(0) {
        table = new std::list<std::pair<K, V>>[capacity];
    }

    ~HashTable() {
        delete[] table;
    }

    void insert(const K& key, const V& value) {
        int index = hash(key);
        for (auto& entry : table[index]) {
            if (entry.first == key) {
                entry.second = value;  // Update existing key
                return;
            }
        }
        table[index].emplace_back(key, value);  // Use emplace_back for efficiency
        size++;
    }

    V get(const K& key) const {
        int index = hash(key);
        for (const auto& entry : table[index]) {
            if (entry.first == key) {
                return entry.second;
            }
        }
        return V(); // Return default-constructed value if not found. Could also throw exception.
    }

    void remove(const K& key) {
        int index = hash(key);
        table[index].remove_if([&](const std::pair<K, V>& entry) { return entry.first == key; });
        //table[index].erase(std::remove_if(table[index].begin(), table[index].end(), [&](const std::pair<K,V>& p){ return p.first == key; }), table[index].end());
        size--; //size will need to be corrected if there are duplicates.
    }


    bool containsKey(const K& key) const {
        int index = hash(key);
        for (const auto& entry : table[index]) {
            if (entry.first == key) {
                return true;
            }
        }
        return false;
    }

    int getSize() const {
        return size;
    }
};


// --- Fibonacci Heap ---
class FibonacciHeap {
private:
    struct Node {
        int key;
        void* value; // Generic pointer for value
        Node* parent;
        Node* child;
        Node* left;
        Node* right;
        int degree;
        bool mark;

        Node(int key, void* value) : key(key), value(value), parent(nullptr), child(nullptr), degree(0), mark(false) {
            left = right = this;  // Circular doubly-linked list
        }
    };

    Node* min;
    int size;

    // Helper functions
    void concatenate(Node* node1, Node* node2) {
        Node* temp = node1->right;
        node1->right = node2->right;
        node2->right->left = node1;
        node2->right = temp;
        temp->left = node2;
    }

    void heapLink(Node* y, Node* x) {
        // Remove y from the root list
        y->left->right = y->right;
        y->right->left = y->left;

        // Make y a child of x
        y->parent = x;
        if (x->child == nullptr) {
            x->child = y;
            y->right = y;
            y->left = y;
        } else {
            concatenate(x->child, y);
        }
        x->degree++;
        y->mark = false;
    }

    void consolidate() {
        // Calculate the maximum degree (logarithmic to the number of nodes)
        int D = (int)std::floor(std::log(size) / std::log(2)) + 1;
        std::vector<Node*> A(D, nullptr);

        // Traverse the root list
        Node* start = min;
        std::vector<Node*> toVisit;
        Node* current = start;

        if (current != nullptr) {
            toVisit.push_back(current);
            current = current->right;
            while (current != start) {
                toVisit.push_back(current);
                current = current->right;
            }
        }

        for (Node* x : toVisit) {
            int d = x->degree;
            while (A[d] != nullptr) {
                Node* y = A[d];
                if (x->key > y->key) {
                    std::swap(x, y); // Swap x and y if needed
                }
                heapLink(y, x);
                A[d] = nullptr;
                d++;
                if (d >= A.size()) {
                    A.resize(d + 1, nullptr); // Extend A if needed
                }
            }
            A[d] = x;
        }

        // Reset min pointer
        min = nullptr;
        for (Node* node : A) {
            if (node != nullptr) {
                if (min == nullptr) {
                    min = node;
                } else {
                    concatenate(min, node);
                    if (node->key < min->key) {
                        min = node;
                    }
                }
            }
        }
    }

    void cut(Node* node, Node* parent) {
        // Remove node from parent's child list
        if (node->right == node) {
            parent->child = nullptr;
        } else {
            parent->child = node->right;
            node->left->right = node->right;
            node->right->left = node->left;
        }
        parent->degree--;
        node->parent = nullptr;
        node->mark = false;

        // Add node to the root list
        concatenate(min, node);
        if (node->key < min->key) {
            min = node;
        }
    }

    void cascadingCut(Node* node) {
        Node* parent = node->parent;
        if (parent != nullptr) {
            if (!node->mark) {
                node->mark = true;
            } else {
                cut(node, parent);
                cascadingCut(parent);
            }
        }
    }


public:
    FibonacciHeap() : min(nullptr), size(0) {}

    // Important:  Return the Node* so decreaseKey and delete can be called.
    Node* insert(int key, void* value) {
        Node* node = new Node(key, value);
        if (min == nullptr) {
            min = node;
        } else {
            concatenate(min, node);
            if (node->key < min->key) {
                min = node;
            }
        }
        size++;
        return node;
    }


    int findMinKey() const {
        if (isEmpty()) {
            throw std::out_of_range("Heap is empty");
        }
        return min->key;
    }

    void* findMinValue() const {
        if (isEmpty()) {
            throw std::out_of_range("Heap is empty");
        }
        return min->value;
    }

    void* extractMin() {
        if (min == nullptr) {
            return nullptr;
        }

        Node* minNode = min;
        void* minValue = minNode->value;

        // Move children of minNode to the root list
        if (minNode->child != nullptr) {
            Node* child = minNode->child;
            Node* next;
            do {
                next = child->right; // Store next *before* detaching
                child->parent = nullptr;
                child = next;
            } while(child != minNode->child);

            concatenate(min, minNode->child);
        }

        // Remove minNode from the root list
        Node* left = minNode->left;
        Node* right = minNode->right;
        left->right = right;
        right->left = left;

        if (minNode == right) { // minNode was the only node in the root list
            min = nullptr;
        } else {
            min = right;
            consolidate();
        }

        size--;
        delete minNode;
        return minValue;
    }

    void decreaseKey(Node* node, int newKey) {
        if (newKey > node->key) {
            throw std::invalid_argument("New key is greater than current key.");
        }
        node->key = newKey;
        Node* parent = node->parent;
        if (parent != nullptr && node->key < parent->key) {
            cut(node, parent);
            cascadingCut(parent);
        }
        if (node->key < min->key) {
            min = node;
        }
    }

    void deleteNode(Node* node) {
       decreaseKey(node, std::numeric_limits<int>::min());
       extractMin();
    }

    bool isEmpty() const {
        return min == nullptr;
    }

    int getSize() const {
        return size;
    }
};



int main() {
    // --- Min-Heap Example ---
    std::cout << "--- Min-Heap Example ---" << std::endl;
    MinHeap minHeap;
    minHeap.push(5);
    minHeap.push(1);
    minHeap.push(9);
    minHeap.push(3);

    std::cout << "Min element: " << minHeap.peek() << std::endl;

    while (!minHeap.isEmpty()) {
        std::cout << "Popped: " << minHeap.pop() << std::endl;
    }

    // --- Hash Table Example ---
    std::cout << "\n--- Hash Table Example ---" << std::endl;
    HashTable<std::string, int> hashTable;
    hashTable.insert("apple", 1);
    hashTable.insert("banana", 2);
    hashTable.insert("cherry", 3);

    std::cout << "Value of banana: " << hashTable.get("banana") << std::endl;
    std::cout << "Size of hash table: " << hashTable.getSize() << std::endl;
    std::cout << "Contains 'apple': " << hashTable.containsKey("apple") << std::endl;

    hashTable.remove("banana");
    std::cout << "Value of banana after deletion: " << hashTable.get("banana") << std::endl;
    std::cout << "Size of hash table after deletion: " << hashTable.getSize() << std::endl;


    // --- Fibonacci Heap Example ---
    std::cout << "\n--- Fibonacci Heap Example ---" << std::endl;
    FibonacciHeap fibHeap;
    FibonacciHeap::Node* node1 = fibHeap.insert(5, (void*)"A"); // Store the Node*
    FibonacciHeap::Node* node2 = fibHeap.insert(1, (void*)"B"); // Store the Node*
    FibonacciHeap::Node* node3 = fibHeap.insert(9, (void*)"C"); // Store the Node*
    FibonacciHeap::Node* node4 = fibHeap.insert(3, (void*)"D"); // Store the Node*

    std::cout << "Min element: " << fibHeap.findMinKey() << " : " << (char*)fibHeap.findMinValue() << std::endl;

    while (!fibHeap.isEmpty()) {
        std::cout << "Extracted: " << (char*)fibHeap.extractMin() << std::endl;
    }

    std::cout << "\n--- Fibonacci Heap with decreaseKey/delete Example ---" << std::endl;
    fibHeap = FibonacciHeap();
    node1 = fibHeap.insert(5, (void*)"A"); // Store the Node*
    node2 = fibHeap.insert(1, (void*)"B"); // Store the Node*
    node3 = fibHeap.insert(9, (void*)"C"); // Store the Node*
    node4 = fibHeap.insert(3, (void*)"D"); // Store the Node*

    fibHeap.decreaseKey(node3, 2); // Decrease key of node with value "C"
    fibHeap.deleteNode(node2);  // Delete node with value "B"

    std::cout << "Min element after decreaseKey and delete: " << fibHeap.findMinKey() << " : " << (char*)fibHeap.findMinValue() << std::endl;


    while (!fibHeap.isEmpty()) {
        std::cout << "Extracted: " << (char*)fibHeap.extractMin() << std::endl;
    }


    return 0;
}
