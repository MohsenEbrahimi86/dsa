import pytest
from src.tree.bst import BST


class TestBST:
    """Test suite for Binary Search Tree implementation"""

    def test_empty_tree(self):
        """Test creation of empty BST"""
        bst = BST()
        assert bst.is_empty() == True
        assert bst.inorder() == []
        assert bst.preorder() == []
        assert bst.postorder() == []
        assert bst.height() == -1
        assert bst.size() == 0
        assert bst.min_value() is None
        assert bst.max_value() is None

    def test_insert_single_value(self):
        """Test inserting a single value"""
        bst = BST()
        bst.insert(50)

        assert bst.is_empty() == False
        assert bst.inorder() == [50]
        assert bst.preorder() == [50]
        assert bst.postorder() == [50]
        assert bst.height() == 0
        assert bst.size() == 1
        assert bst.min_value() == 50
        assert bst.max_value() == 50

    def test_insert_multiple_values(self):
        """Test inserting multiple values"""
        bst = BST()
        values = [50, 30, 70, 20, 40, 60, 80]

        bst.insert(values)

        # Inorder should give sorted order
        assert bst.inorder() == sorted(values)
        assert bst.size() == len(values)
        assert bst.min_value() == min(values)
        assert bst.max_value() == max(values)

    def test_search_existing_values(self):
        """Test searching for existing values"""
        bst = BST()
        values = [50, 30, 70, 20, 40, 60, 80]

        for val in values:
            bst.insert(val)

        for val in values:
            assert bst.search(val) is not None

        # Root node
        assert bst.search(50) is not None

    def test_search_nonexistent_values(self):
        """Test searching for non-existent values"""
        bst = BST()
        values = [50, 30, 70, 20, 40, 60, 80]

        for val in values:
            bst.insert(val)

        # Values not in tree
        assert bst.search(25) is None
        assert bst.search(100) is None
        assert bst.search(0) is None

    def test_insert_duplicates(self):
        """Test behavior with duplicate values"""
        bst = BST()
        bst.insert(50)
        bst.insert(50)  # Duplicate

        # Our implementation doesn't insert duplicates
        assert bst.size() == 2
        assert bst.inorder() == [50, 50]

    def test_delete_leaf_node(self):
        """Test deleting a leaf node"""
        bst = BST()
        values = [50, 30, 70, 20, 40, 60, 80]

        for val in values:
            bst.insert(val)

        initial_size = bst.size()

        # Delete a leaf node (20)
        bst.delete(20)
        assert 20 not in bst.inorder()
        assert bst.size() == initial_size - 1

        # Verify tree structure
        assert bst.inorder() == [30, 40, 50, 60, 70, 80]

    def test_delete_node_with_one_child(self):
        """Test deleting a node with one child"""
        bst = BST()
        # Create a node with one child
        bst.insert(50)
        bst.insert(30)
        bst.insert(20)  # 30 has left child 20

        # Delete node with one child (30)
        bst.delete(30)
        assert 30 not in bst.inorder()
        assert 20 in bst.inorder()
        assert bst.inorder() == [20, 50]

    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children"""
        bst = BST()
        values = [50, 30, 70, 20, 40, 60, 80]

        for val in values:
            bst.insert(val)

        # Delete root node (50) which has two children
        bst.delete(50)
        assert 50 not in bst.inorder()
        assert bst.size() == 6

        # The successor (60) should replace 50
        assert bst.inorder() == [20, 30, 40, 60, 70, 80]

    def test_delete_nonexistent_value(self):
        """Test deleting a non-existent value"""
        bst = BST()
        values = [50, 30, 70]

        for val in values:
            bst.insert(val)

        initial_inorder = bst.inorder()
        initial_size = bst.size()

        # Delete non-existent value
        bst.delete(100)

        # Tree should remain unchanged
        assert bst.inorder() == initial_inorder
        assert bst.size() == initial_size

    def test_delete_all_nodes(self):
        """Test deleting all nodes"""
        bst = BST()
        values = [50, 30, 70, 20, 40]

        for val in values:
            bst.insert(val)

        # Delete all nodes
        for val in values:
            bst.delete(val)

        assert bst.is_empty() == True
        assert bst.size() == 0
        assert bst.inorder() == []

    def test_traversals(self):
        """Test different traversal methods"""
        bst = BST()
        values = [50, 30, 70, 20, 40, 60, 80]

        for val in values:
            bst.insert(val)

        # Inorder should be sorted
        assert bst.inorder() == sorted(values)

        # Preorder: root, left, right
        preorder = bst.preorder()
        assert preorder[0] == 50  # Root should be first

        # Postorder: left, right, root
        postorder = bst.postorder()
        assert postorder[-1] == 50  # Root should be last

    def test_height_calculation(self):
        """Test height calculation"""
        bst = BST()

        # Empty tree
        assert bst.height() == -1

        # Single node
        bst.insert(50)
        assert bst.height() == 0

        # Add more nodes to increase height
        bst.insert(30)
        bst.insert(70)
        assert bst.height() == 1

        bst.insert(20)
        assert bst.height() == 2

        bst.insert(10)
        assert bst.height() == 3

    def test_min_max_values(self):
        """Test min and max value functions"""
        bst = BST()

        # Empty tree
        assert bst.min_value() is None
        assert bst.max_value() is None

        # Single node
        bst.insert(50)
        assert bst.min_value() == 50
        assert bst.max_value() == 50

        # Multiple nodes
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(80)

        assert bst.min_value() == 20
        assert bst.max_value() == 80

    def test_edge_cases(self):
        """Test various edge cases"""
        bst = BST()

        # Insert, search, delete on empty tree
        assert bst.search(50) is None
        bst.delete(50)  # Should not raise error
        assert bst.size() == 0

        # Large values
        bst.insert(999999)
        bst.insert(-999999)
        assert bst.min_value() == -999999
        assert bst.max_value() == 999999

        # Zero and negative numbers
        bst = BST()
        values = [0, -10, 5, -3, 8]
        for val in values:
            bst.insert(val)

        assert bst.inorder() == sorted(values)
        assert bst.search(-10) is not None
        assert bst.search(100) is None


# Run tests with specific focus
@pytest.mark.parametrize("values", [
    [1],
    [1, 2],
    [2, 1],
    [5, 3, 7, 2, 4, 6, 8],
    [10, 5, 15, 3, 7, 12, 18, 1, 4, 6, 8, 11, 13, 17, 19]
])
def test_insert_and_traverse(values):
    """Parametrized test for different value sets"""
    bst = BST()
    for val in values:
        bst.insert(val)

    assert bst.inorder() == sorted(values)
    assert bst.size() == len(values)
    assert bst.min_value() == min(values)
    assert bst.max_value() == max(values)

    # Test search for all values
    for val in values:
        assert bst.search(val) is not None


if __name__ == "__main__":
    # This allows running tests directly
    pytest.main([__file__, "-v"])