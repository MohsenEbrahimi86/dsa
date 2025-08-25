class BinaryTreeNode:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return (f"TreeNode: Value= {self.value}, "
                f"Left = {self.left}, "
                f"Right = {self.right}")
