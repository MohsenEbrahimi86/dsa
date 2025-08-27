# Splay Tree Implementation in Python

A splay tree is a self-adjusting binary search tree with the additional property that recently accessed elements are quick to access again. It performs basic operations such as insertion, lookup, and removal in O(log n) amortized time.

- [SplayTree](https://github.com/MohsenEbrahimi86/dsa/blob/main/src/tree/splay_tree.py)

## Key Features of this Splay Tree Implementation:

1. **Node Class**: Represents a node in the splay tree with key, value, and references to left, right, and parent nodes.

2. **Rotations**: Implements left and right rotations which are the basic operations for restructuring the tree.

3. **Splaying**: The core operation that moves a node to the root using a series of rotations following the zig-zig and zig-zag cases.

4. **Insert**: Inserts a key-value pair and splays the inserted node to the root.

5. **Find**: Searches for a key and splays the found node (or the last accessed node) to the root.

6. **Delete**: Removes a node with a given key and maintains the splay tree properties.

7. **Additional Operations**: Includes methods for inorder traversal, checking if empty, and finding minimum/maximum values.

8. **Comprehensive Testing**: The test suite verifies all major operations and edge cases.

The splay tree provides amortized O(log n) time complexity for all operations, with the advantage that frequently accessed elements become quicker to access over time due to the splaying operation.