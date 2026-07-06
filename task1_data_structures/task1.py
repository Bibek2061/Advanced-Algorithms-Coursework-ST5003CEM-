import random
import time
import heapq
import matplotlib.pyplot as plt

# ============================================================
# ADVANCED ALGORITHMS
# TASK 1 – ADVANCED DATA STRUCTURES
# Route Planning Application
# ============================================================


# ============================================================
# CITY CLASS
# ============================================================

class City:

    def __init__(self, name, x, y, population, distance):
        self.name = name
        self.x = x
        self.y = y
        self.population = population
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance

    def __str__(self):
        return (
            f"{self.name} | "
            f"Coordinates=({self.x}, {self.y}) | "
            f"Population={self.population} | "
            f"Distance={self.distance:.2f} km"
        )


# ============================================================
# RANDOM CITY GENERATOR
# ============================================================

def generate_city(index):

    return City(
        name=f"City_{index}",
        x=random.randint(0, 1000),
        y=random.randint(0, 1000),
        population=random.randint(10000, 5000000),
        distance=random.uniform(1, 500)
    )


def generate_dataset(size):

    cities = []

    for i in range(size):
        cities.append(generate_city(i))

    return cities


# ============================================================
# BST NODE
# ============================================================

class BSTNode:

    def __init__(self, city):

        self.city = city
        self.left = None
        self.right = None


# BINARY SEARCH TREE

class BinarySearchTree:

    def __init__(self):

        self.root = None

    # --------------------------

    def insert(self, city):

        if self.root is None:

            self.root = BSTNode(city)

        else:

            self.root = self._insert(self.root, city)

    def _insert(self, node, city):

        if node is None:
            return BSTNode(city)

        if city.name < node.city.name:
            node.left = self._insert(node.left, city)
        else:
            node.right = self._insert(node.right, city)

        return node

    # --------------------------

    def search(self, city_name):

        return self._search(self.root, city_name)

    def _search(self, node, city_name):

        if node is None:
            return None

        if node.city.name == city_name:
            return node.city

        if city_name < node.city.name:
            return self._search(node.left, city_name)

        return self._search(node.right, city_name)

    # --------------------------

    def minimum(self, node):

        while node.left:

            node = node.left

        return node

    # --------------------------

    def delete(self, city_name):

        self.root = self._delete(self.root, city_name)

    def _delete(self, node, city_name):

        if node is None:
            return node

        if city_name < node.city.name:

            node.left = self._delete(node.left, city_name)

        elif city_name > node.city.name:

            node.right = self._delete(node.right, city_name)

        else:

            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            temp = self.minimum(node.right)

            node.city = temp.city

            node.right = self._delete(
                node.right,
                temp.city.name
            )

        return node

    # --------------------------

    def inorder(self):

        data = []

        self._inorder(self.root, data)

        return data

    def _inorder(self, node, data):

        if node:

            self._inorder(node.left, data)

            data.append(node.city)

            self._inorder(node.right, data)


# ============================================================
# AVL NODE
# ============================================================

class AVLNode:

    def __init__(self, city):
        self.city = city
        self.left = None
        self.right = None
        self.height = 1



# AVL TREE

class AVLTree:

    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def balance_factor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def right_rotate(self, y):
        x = y.left
        temp = x.right

        x.right = y
        y.left = temp

        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        return x

    def left_rotate(self, x):
        y = x.right
        temp = y.left

        y.left = x
        x.right = temp

        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def insert(self, city):
        self.root = self._insert(self.root, city)

    def _insert(self, node, city):
        if node is None:
            return AVLNode(city)

        if city.name < node.city.name:
            node.left = self._insert(node.left, city)
        elif city.name > node.city.name:
            node.right = self._insert(node.right, city)
        else:
            return node

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.balance_factor(node)

        if balance > 1 and city.name < node.left.city.name:
            return self.right_rotate(node)

        if balance < -1 and city.name > node.right.city.name:
            return self.left_rotate(node)

        if balance > 1 and city.name > node.left.city.name:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        if balance < -1 and city.name < node.right.city.name:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def search(self, city_name):
        return self._search(self.root, city_name)

    def _search(self, node, city_name):
        if node is None:
            return None

        if node.city.name == city_name:
            return node.city

        if city_name < node.city.name:
            return self._search(node.left, city_name)

        return self._search(node.right, city_name)

    def inorder(self):
        data = []
        self._inorder(self.root, data)
        return data

    def _inorder(self, node, data):
        if node:
            self._inorder(node.left, data)
            data.append(node.city)
            self._inorder(node.right, data)



# MIN HEAP

class MinHeap:

    def __init__(self):
        self.heap = []

    def insert(self, city):
        heapq.heappush(self.heap, city)

    def extract_min(self):
        if self.heap:
            return heapq.heappop(self.heap)
        return None

    def peek(self):
        if self.heap:
            return self.heap[0]
        return None

    def size(self):
        return len(self.heap)
    







    

# HASH TABLE (CHAINING)
class HashTable:

    def __init__(self, size=1009):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, city):
        index = self.hash_function(city.name)

        # Update if already exists
        for i, existing in enumerate(self.table[index]):
            if existing.name == city.name:
                self.table[index][i] = city
                return

        self.table[index].append(city)

    def search(self, city_name):
        index = self.hash_function(city_name)

        for city in self.table[index]:
            if city.name == city_name:
                return city

        return None

    def delete(self, city_name):
        index = self.hash_function(city_name)

        for i, city in enumerate(self.table[index]):
            if city.name == city_name:
                del self.table[index][i]
                return True

        return False

    def count_items(self):
        total = 0

        for bucket in self.table:
            total += len(bucket)

        return total
    







   
    