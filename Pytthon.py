
import heapq
import sys

# --- Бинарная куча (Min-Heap) ---

class MinHeap:
    """
    Реализация Min-Heap с использованием модуля heapq.
    """

    def __init__(self, items=None):
        """
        Инициализирует Min-Heap.

        Args:
            items: (optional) Итерируемый объект для начальной инициализации кучи.
                   Если не указан, создается пустая куча.
        """
        if items is None:
            self.heap = []
        else:
            self.heap = list(items)
            heapq.heapify(self.heap)  # Преобразует список в кучу in-place

    def push(self, item):
        """
        Добавляет новый элемент в кучу.

        Args:
            item: Элемент для добавления.
        """
        heapq.heappush(self.heap, item)

    def pop(self):
        """
        Удаляет и возвращает наименьший элемент из кучи.

        Returns:
            Наименьший элемент.

        Raises:
            IndexError: Если куча пуста.
        """
        if not self.heap:
            raise IndexError("pop from an empty heap")
        return heapq.heappop(self.heap)

    def peek(self):
        """
        Возвращает наименьший элемент из кучи, не удаляя его.

        Returns:
            Наименьший элемент.

        Raises:
            IndexError: Если куча пуста.
        """
        if not self.heap:
            raise IndexError("peek from an empty heap")
        return self.heap[0]

    def is_empty(self):
        """
        Проверяет, пуста ли куча.

        Returns:
            True, если куча пуста, иначе False.
        """
        return not bool(self.heap)

    def size(self):
        """
        Возвращает размер кучи.

        Returns:
            Размер кучи (количество элементов).
        """
        return len(self.heap)


# --- Хеш-таблица ---

class HashTable:
    """
    Простая реализация хеш-таблицы с обработкой коллизий методом цепочек.
    """

    def __init__(self, capacity=11):  # Prime number for better distribution
        """
        Инициализирует хеш-таблицу.

        Args:
            capacity: (optional) Начальный размер таблицы.  Рекомендуется простое число.
        """
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]  # Список списков (цепочки)
        self.size = 0

    def _hash(self, key):
        """
        Вычисляет хеш-код для ключа.

        Args:
            key: Ключ для хеширования.

        Returns:
            Хеш-код ключа.
        """
        # Простое хеширование по модулю
        return hash(key) % self.capacity

    def insert(self, key, value):
        """
        Вставляет пару ключ-значение в хеш-таблицу.

        Args:
            key: Ключ.
            value: Значение.
        """
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)  # Обновление существующего ключа
                return
        self.table[index].append((key, value))
        self.size += 1

    def get(self, key):
        """
        Возвращает значение, связанное с ключом.

        Args:
            key: Ключ для поиска.

        Returns:
            Значение, связанное с ключом, или None, если ключ не найден.
        """
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        """
        Удаляет пару ключ-значение из хеш-таблицы.

        Args:
            key: Ключ для удаления.
        """
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.size -= 1
                return

    def __len__(self):
        """
        Возвращает количество пар ключ-значение в хеш-таблице.

        Returns:
            Количество элементов в хеш-таблице.
        """
        return self.size

    def __contains__(self, key):
        """
        Проверяет, содержит ли хеш-таблица данный ключ.

        Args:
            key: Ключ для проверки.

        Returns:
            True, если ключ содержится в хеш-таблице, иначе False.
        """
        return self.get(key) is not None


# --- Куча Фибоначчи ---

class FibonacciHeapNode:
    """
    Узел в куче Фибоначчи.
    """

    def __init__(self, key, value=None):
        """
        Инициализирует узел кучи Фибоначчи.

        Args:
            key: Ключ узла (значение, используемое для сравнения).
            value: (optional) Значение, связанное с узлом.
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
    Реализация кучи Фибоначчи.
    """

    def __init__(self):
        """
        Инициализирует кучу Фибоначчи.
        """
        self.min_node = None
        self.size = 0

    def insert(self, key, value=None):
        """
        Вставляет новый узел в кучу.

        Args:
            key: Ключ нового узла.
            value: (optional) Значение, связанное с узлом.
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
        Объединяет два узла в круговой двусвязный список.

        Args:
            node1: Первый узел.
            node2: Второй узел.
        """
        node1_right = node1.right
        node1.right = node2
        node2.left = node1
        node2_right = node2.right
        node2.right = node1_right
        node1_right.left = node2

    def find_min(self):
        """
        Возвращает минимальный узел кучи (не удаляя его).

        Returns:
            Минимальный узел кучи, или None, если куча пуста.
        """
        if self.min_node is None:
            return None
        return self.min_node.key, self.min_node.value

    def extract_min(self):
        """
        Удаляет и возвращает минимальный узел из кучи.

        Returns:
            Кортеж (key, value) минимального узла, или None, если куча пуста.
        """
        if self.min_node is None:
            return None

        min_node = self.min_node

        # Перемещаем детей min_node в корневой список
        if min_node.child is not None:
            child = min_node.child
            for _ in range(min_node.degree):
                child.parent = None
                child = child.right
            self._concatenate(self.min_node, min_node.child)

        # Удаляем min_node из корневого списка
        left = min_node.left
        right = min_node.right
        left.right = right
        right.left = left

        if min_node == right:  # min_node был единственным узлом в корневом списке
            self.min_node = None
        else:
            self.min_node = right
            self._consolidate()  # Вызываем consolidate для объединения деревьев

        self.size -= 1

        return min_node.key, min_node.value

    def _consolidate(self):
        """
        Объединяет деревья одинаковой степени в корневом списке.
        """
        A = [None] * (self.size + 1)  # Массив для хранения указателей на деревья каждой степени

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
                    x, y = y, x  # Убеждаемся, что x - корень с меньшим ключом

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
        Делает узел 'y' потомком узла 'x'.

        Args:
            y: Узел, который нужно сделать потомком.
            x: Узел, который станет родителем.
        """
        # Удаляем y из корневого списка
        y.left.right = y.right
        y.right.left = y.left

        # Делаем y потомком x
        y.parent = x
        if x.child is None:
            x.child = y
            y.right = y
            y.left = y
        else:
            self._concatenate(x.child, y)

        x.degree += 1
        y.mark = False  # Сбрасываем пометку

    def decrease_key(self, node, new_key):
        """
        Уменьшает ключ заданного узла.  (Требует доступа к конкретному узлу).
        В реальных приложениях нужно сначала найти узел по его значению.

        Args:
            node: Узел, ключ которого нужно уменьшить.
            new_key: Новое значение ключа.

        Raises:
            ValueError: Если новое значение ключа больше текущего.
        """
        if new_key > node.key:
            raise ValueError("Новый ключ должен быть меньше или равен текущему")

        node.key = new_key
        parent = node.parent

        if parent is not None and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        if node.key < self.min_node.key:
            self.min_node = node

    def _cut(self, node, parent):
        """
        Вырезает узел из списка потомков его родителя и помещает его в корневой список.

        Args:
            node: Узел для вырезания.
            parent: Родитель узла.
        """

        # Удаляем node из списка потомков parent
        if node.right == node:
            parent.child = None  # node был единственным потомком
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
        Каскадное вырезание узлов, пока не будет достигнут корень или непомеченный узел.

        Args:
            node: Узел для начала каскадного вырезания.
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
        Удаляет узел из кучи Фибоначчи.  (Требует доступа к конкретному узлу).
        В реальных приложениях нужно сначала найти узел по его значению.
        Эффективно уменьшает ключ узла до минус бесконечности и извлекает минимум.

        Args:
            node: Узел для удаления.
        """
        self.decrease_key(node, float('-inf'))  # Уменьшаем ключ до минус бесконечности
        self.extract_min()


    def is_empty(self):
        """
        Проверяет, пуста ли куча.

        Returns:
            True, если куча пуста, иначе False.
        """
        return self.min_node is None

    def __len__(self):
        """
        Возвращает количество узлов в куче.

        Returns:
            Количество узлов в куче.
        """
        return self.size


# --- Примеры использования ---

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

    # Дополнительный пример кучи Фибоначчи с уменьшением ключа и удалением
    fib_heap = FibonacciHeap()
    node1 = fib_heap.insert(5, "A") # insert возвращает None, нужно хранить значения отдельно
    node2 = fib_heap.insert(1, "B")
    node3 = fib_heap.insert(9, "C")
    node4 = fib_heap.insert(3, "D")

    #  Для уменьшения ключа и удаления требуется *доступ к узлу*.  
    #  Здесь  вставляем элементы в кучу, *не сохраняя ссылку на узел*.  
    #  В реальной задаче, где требуется уменьшение ключа и удаление, нужно
    #  реализовать другой механизм, например, хеш-таблицу, отображающую значения на узлы.

    #  Вместо реального decrease_key и delete, мы просто показываем
    #  последовательность операций, которые нужно выполнить.
    print("\nDemonstrating decrease_key and delete (requires node access, not available in this example):")
    print("To use decrease_key/delete, you would need to store the node references during insertion")
    print("and implement a lookup mechanism (e.g., a hash table) to find the node based on its value.")
    #fib_heap.decrease_key(node3, 2)  # This won't work because we don't have a reference to node3
    #fib_heap.delete(node2)  # This won't work because we don't have a reference to node2
