# splay_tree.py

class Node:
    """Node class for Splay Tree"""

    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None


class SplayTree:
    """Splay Tree implementation"""

    def __init__(self):
        self.root = None

    def _rotate_right(self, x):
        """Right rotation"""
        y = x.left
        x.left = y.right

        if y.right:
            y.right.parent = x

        y.parent = x.parent

        if not x.parent:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

        return y

    def _rotate_left(self, x):
        """Left rotation"""
        y = x.right
        x.right = y.left

        if y.left:
            y.left.parent = x

        y.parent = x.parent

        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

        return y

    def _splay(self, node):
        """Splay the given node to the root"""
        if not node:
            return None

        while node.parent:
            parent = node.parent
            grandparent = parent.parent

            # Zig case (node is child of root)
            if not grandparent:
                if node == parent.left:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)
            # Zig-zig case (both node and parent are left children or both are right children)
            elif node == parent.left and parent == grandparent.left:
                self._rotate_right(grandparent)
                self._rotate_right(parent)
            elif node == parent.right and parent == grandparent.right:
                self._rotate_left(grandparent)
                self._rotate_left(parent)
            # Zig-zag case (node is left child, parent is right child, or vice versa)
            elif node == parent.left and parent == grandparent.right:
                self._rotate_right(parent)
                self._rotate_left(grandparent)
            else:  # node == parent.right and parent == grandparent.left
                self._rotate_left(parent)
                self._rotate_right(grandparent)

        return node

    def insert(self, key, value=None):
        """Insert a key-value pair into the splay tree"""
        if not self.root:
            self.root = Node(key, value)
            return

        # Find the place to insert
        current = self.root
        while True:
            if key == current.key:
                current.value = value
                self._splay(current)
                return
            elif key < current.key:
                if not current.left:
                    current.left = Node(key, value)
                    current.left.parent = current
                    self._splay(current.left)
                    return
                current = current.left
            else:  # key > current.key
                if not current.right:
                    current.right = Node(key, value)
                    current.right.parent = current
                    self._splay(current.right)
                    return
                current = current.right

    def find(self, key):
        """Find a node with the given key and splay it to the root"""
        if not self.root:
            return None

        current = self.root
        while current:
            if key == current.key:
                self._splay(current)
                return current.value
            elif key < current.key:
                if not current.left:
                    self._splay(current)  # Splay the last accessed node
                    return None
                current = current.left
            else:  # key > current.key
                if not current.right:
                    self._splay(current)  # Splay the last accessed node
                    return None
                current = current.right

        return None

    def _find_node(self, key):
        """Find a node with the given key (internal method that returns the node)"""
        if not self.root:
            return None

        current = self.root
        while current:
            if key == current.key:
                return current
            elif key < current.key:
                if not current.left:
                    return current
                current = current.left
            else:  # key > current.key
                if not current.right:
                    return current
                current = current.right

        return None

    def delete(self, key):
        """Delete a node with the given key"""
        node = self._find_node(key)
        if not node or node.key != key:
            return False  # Key not found

        self._splay(node)  # Splay the node to be deleted to the root

        # Now the node to be deleted is at the root
        if not node.left:
            # No left child, replace root with right child
            self.root = node.right
            if self.root:
                self.root.parent = None
        elif not node.right:
            # No right child, replace root with left child
            self.root = node.left
            if self.root:
                self.root.parent = None
        else:
            # Node has both children
            # Find the maximum node in the left subtree
            left_max = node.left
            while left_max.right:
                left_max = left_max.right

            # Splay the maximum node in the left subtree to the root of the left subtree
            self._splay(left_max)

            # Now left_max is the new root of the left subtree and has no right child
            left_max.right = node.right
            node.right.parent = left_max
            self.root = left_max

        return True

    def _inorder(self, node, result):
        """Helper method for inorder traversal"""
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)

    def inorder(self):
        """Return a list of all key-value pairs in inorder (sorted by key)"""
        result = []
        self._inorder(self.root, result)
        return result

    def is_empty(self):
        """Check if the tree is empty"""
        return self.root is None

    def minimum(self):
        """Find the minimum key in the tree"""
        if not self.root:
            return None

        current = self.root
        while current.left:
            current = current.left

        self._splay(current)
        return current.key, current.value

    def maximum(self):
        """Find the maximum key in the tree"""
        if not self.root:
            return None

        current = self.root
        while current.right:
            current = current.right

        self._splay(current)
        return current.key, current.value
