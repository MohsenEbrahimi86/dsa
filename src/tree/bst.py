from src.tree.binary_tree_node import BinaryTreeNode


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if type(value) is list:
            # Batch Insert
            for item in value:
                self._insert_one(item)
        else:
            self._insert_one(value)

    def _insert_one(self, value):
        """Insert a value to the BST"""
        if not self.root:
            self.root = BinaryTreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        """Helper method for recursive insertion"""
        if value < node.value:
            if node.left is None:
                node.left = BinaryTreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = BinaryTreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        """Search for a value in the BST"""
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """Helper method for recursive search"""
        if node is not None:
            if node.value == value:
                return node

            if value < node.value:
                if node.left is not None:
                    return self._search_recursive(node.left, value)
            else:
                if node.right is not None:
                    return self._search_recursive(node.right, value)
        return None
    def delete(self, value):
        """Delete a value from the BST"""
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        """Helper method for recursive deletion"""
        if not node:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node to be deleted found
            # Case 1: Node has no children (leaf node)
            if not node.left and not node.right:
                return None

            # Case 2: Node has one child
            elif not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Case 3: Node has two children
            else:
                # Find the inorder successor (smallest value in right subtree)
                successor = self._find_min(node.right)
                node.value = successor.value
                node.right = self._delete_recursive(node.right, successor.value)

        return node

    @staticmethod
    def _find_min(node):
        """Find the minimum value node in a subtree"""
        while node.left:
            node = node.left
        return node

    @staticmethod
    def _find_max(node):
        """Find the maximum value node in a subtree"""
        while node.right:
            node = node.right
        return node

    def inorder(self):
        """Return inorder traversal (sorted order)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        """Helper method for inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder(self):
        """Return preorder traversal"""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        """Helper method for preorder traversal"""
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder(self):
        """Return postorder traversal"""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        """Helper method for postorder traversal"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def height(self):
        """Calculate the height of the BST"""
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        """Helper method for height calculation"""
        if not node:
            return -1

        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)

        return max(left_height, right_height) + 1

    def size(self):
        """Calculate the number of nodes in the BST"""
        return self._size_recursive(self.root)

    def _size_recursive(self, node):
        """Helper method for size calculation"""
        if not node:
            return 0
        return 1 + self._size_recursive(node.left) + self._size_recursive(node.right)

    def is_empty(self):
        """Check if the BST is empty"""
        return self.root is None

    def min_value(self):
        """Find the minimum value in the BST"""
        if not self.root:
            return None
        return self._find_min(self.root).value

    def max_value(self):
        """Find the maximum value in the BST"""
        if not self.root:
            return None
        return self._find_max(self.root).value

    def __str__(self):
        """String representation of the BST"""
        return str(self.inorder())


# Example usage and testing
if __name__ == "__main__":
    # Create a BST
    bst = BST()
    # values = [int(1000 * random.random()) for i in range(10000)]

    # Insert values
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    print("Inserting values:", values)

    bst.insert(values)

    # Test various operations
    print(f"\nInorder traversal (sorted): {bst.inorder()}")
    print(f"Preorder traversal: {bst.preorder()}")
    print(f"Postorder traversal: {bst.postorder()}")
    print(f"Tree height: {bst.height()}")
    print(f"Tree size: {bst.size()}")
    print(f"Minimum value: {bst.min_value()}")
    print(f"Maximum value: {bst.max_value()}")

    # Search operations
    print(f"\nSearching for 40: {'Found' if bst.search(40) else 'Not found'}")
    print(f"Searching for 100: {'Found' if bst.search(100) else 'Not found'}")

    # Delete operations
    print(f"\nDeleting 20...")
    bst.delete(20)
    print(f"Inorder after deleting 20: {bst.inorder()}")

    print(f"Deleting 30...")
    bst.delete(30)
    print(f"Inorder after deleting 30: {bst.inorder()}")

    print(f"Deleting 50 (root)...")
    bst.delete(50)
    print(f"Inorder after deleting 50: {bst.inorder()}")

    # Final state
    print(f"\nFinal tree: {bst}")
    print(f"Final height: {bst.height()}")
    print(f"Final size: {bst.size()}")
