import heapq

class TreeNode:
    """Used for Cuisine and Meal Type Classification Hierarchy."""
    def __init__(self, name):
        self.name = name
        self.children = {}

    def add_child(self, name):
        if name not in self.children:
            self.children[name] = TreeNode(name)
        return self.children[name]


class PriorityQueue:
    """Priority Queue to rank recommendations based on match score relevance."""
    def __init__(self):
        self.heap = []
        self.count = 0  # Unique tie-breaker counter to completely avoid dict comparison crashes

    def push(self, item, priority):
        # Python's heapq is a min-heap; invert priority to make it a max-heap
        # Insert self.count as a tie-breaker so Python never compares dicts directly
        heapq.heappush(self.heap, (-priority, self.count, item))
        self.count += 1

    def pop(self):
        if self.heap:
            # Pop returns a 3-element tuple (-priority, count, item); grab index 2
            return heapq.heappop(self.heap)[2]
        return None

    def is_empty(self):
        return len(self.heap) == 0


class Stack:
    """Stack to handle Undo operations for navigation history."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0