import pytest
from src.tree.splay_tree import SplayTree


@pytest.fixture
def empty_tree():
    """Fixture that returns an empty splay tree"""
    return SplayTree()


def test_empty_tree(empty_tree):
    """Test operations on an empty tree"""
    assert empty_tree.is_empty() is True
    assert empty_tree.find(1) is None
    assert empty_tree.inorder() == []
    assert empty_tree.minimum() is None
    assert empty_tree.maximum() is None


def test_insert_and_find_single(empty_tree):
    """Test inserting and finding a single element"""
    empty_tree.insert(10, "ten")

    assert empty_tree.is_empty() is False
    assert empty_tree.find(10) == "ten"
    assert empty_tree.find(5) is None
    assert empty_tree.inorder() == [(10, "ten")]


def test_insert_multiple_elements(empty_tree):
    """Test inserting multiple elements"""
    values = [(10, "ten"), (5, "five"), (15, "fifteen"), (3, "three"),
              (7, "seven"), (12, "twelve"), (17, "seventeen")]

    for key, value in values:
        empty_tree.insert(key, value)

    # Verify all values can be found
    for key, value in values:
        assert empty_tree.find(key) == value

    # Verify inorder traversal is sorted
    expected = sorted(values)
    assert empty_tree.inorder() == expected


def test_update_existing_key(empty_tree):
    """Test updating the value of an existing key"""
    empty_tree.insert(10, "ten")
    assert empty_tree.find(10) == "ten"

    # Update the value
    empty_tree.insert(10, "new_ten")
    assert empty_tree.find(10) == "new_ten"


def test_delete_leaf_node():
    """Test deleting a leaf node"""
    tree = SplayTree()

    # Build a simple tree
    tree.insert(10, "ten")
    tree.insert(5, "five")
    tree.insert(15, "fifteen")

    # Delete a leaf
    assert tree.delete(5) is True
    assert tree.find(5) is None
    assert tree.inorder() == [(10, "ten"), (15, "fifteen")]


def test_delete_node_with_one_child():
    """Test deleting a node with one child"""
    tree = SplayTree()

    # Build a tree where 5 has one child
    tree.insert(10, "ten")
    tree.insert(5, "five")
    tree.insert(7, "seven")  # 5 now has a right child

    assert tree.delete(5) is True
    assert tree.find(5) is None
    assert tree.inorder() == [(7, "seven"), (10, "ten")]


def test_delete_node_with_two_children():
    """Test deleting a node with two children"""
    tree = SplayTree()

    # Build a tree
    elements = [(10, "ten"), (5, "five"), (15, "fifteen"), (3, "three"), (7, "seven")]
    for key, value in elements:
        tree.insert(key, value)

    # Delete root (10) which has two children
    assert tree.delete(10) is True
    assert tree.find(10) is None

    # The inorder should still be sorted without the deleted element
    remaining = [(3, "three"), (5, "five"), (7, "seven"), (15, "fifteen")]
    assert tree.inorder() == remaining


def test_delete_nonexistent_key():
    """Test deleting a key that doesn't exist"""
    tree = SplayTree()
    tree.insert(10, "ten")

    assert tree.delete(5) is False  # Key doesn't exist
    assert tree.find(10) == "ten"  # Original key still exists


def test_minimum_and_maximum():
    """Test finding minimum and maximum values"""
    tree = SplayTree()

    elements = [(10, "ten"), (5, "five"), (15, "fifteen"), (3, "three"), (17, "seventeen")]
    for key, value in elements:
        tree.insert(key, value)

    min_key, min_val = tree.minimum()
    assert min_key == 3
    assert min_val == "three"

    max_key, max_val = tree.maximum()
    assert max_key == 17
    assert max_val == "seventeen"


def test_minimum_and_maximum_empty_tree(empty_tree):
    """Test minimum and maximum on empty tree"""
    assert empty_tree.minimum() is None
    assert empty_tree.maximum() is None


def test_splaying_effect():
    """Test that splaying brings accessed elements closer to root"""
    tree = SplayTree()

    # Insert several elements
    for i in range(1, 8):
        tree.insert(i, f"value_{i}")

    # Access element 7 (originally deep in the tree)
    assert tree.find(7) == "value_7"

    # After splaying, 7 should be easier to access
    # While we can't directly check the tree structure,
    # the find operation should still work correctly
    assert tree.find(7) == "value_7"


def test_delete_all_nodes():
    """Test deleting all nodes from the tree"""
    tree = SplayTree()

    elements = [10, 5, 15, 3, 7, 12, 17]
    for key in elements:
        tree.insert(key, f"value_{key}")

    # Delete all nodes
    for key in elements:
        assert tree.delete(key) is True
        assert tree.find(key) is None

    assert tree.is_empty() is True
    assert tree.inorder() == []


def test_edge_cases():
    """Test various edge cases"""
    tree = SplayTree()

    # Test operations on empty tree
    assert tree.find(None) is None
    assert tree.delete(None) is False

    # Test with negative keys
    tree.insert(-5, "negative_five")
    assert tree.find(-5) == "negative_five"
    assert tree.minimum() == (-5, "negative_five")

    # Test with string keys (if supported)
    string_tree = SplayTree()
    string_tree.insert("apple", "fruit")
    string_tree.insert("banana", "yellow")
    assert string_tree.find("apple") == "fruit"
    assert string_tree.find("banana") == "yellow"

    # Clean up
    string_tree.delete("apple")
    string_tree.delete("banana")


def test_large_sequence():
    """Test with a larger sequence of operations"""
    tree = SplayTree()

    # Insert a sequence of numbers
    for i in range(1, 101):
        tree.insert(i, f"value_{i}")

    # Verify some finds
    assert tree.find(1) == "value_1"
    assert tree.find(50) == "value_50"
    assert tree.find(100) == "value_100"
    assert tree.find(101) is None  # Should not exist

    # Delete some elements
    for i in range(1, 51):
        assert tree.delete(i) is True

    # Check remaining elements
    remaining = tree.inorder()
    expected = [(i, f"value_{i}") for i in range(51, 101)]
    assert remaining == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
