import threading
from typing import Optional, TypeVar, Generic
from queue import LifoQueue
import time

T = TypeVar('T')


class FastNonBlockingStack(Generic[T]):
    """
    A fast thread-safe non-blocking stack implementation for Python.

    Uses Python's atomic operations (which are atomic at the interpreter level)
    and minimizes locking where possible.
    """

    def __init__(self, maxsize: int = 0):
        """
        Initialize the stack.

        Args:
            maxsize: Maximum size of the stack. 0 means unlimited.
        """
        self._items = []
        self._maxsize = maxsize
        self._lock = threading.RLock()  # Reentrant lock for size checks
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)

    def push(self, item: T) -> bool:
        """
        Push an item onto the stack.

        Returns:
            True if successful, False if stack is full (when maxsize > 0)
        """
        with self._lock:
            if self._maxsize > 0 and len(self._items) >= self._maxsize:
                return False

            self._items.append(item)
            self._not_empty.notify()
            return True

    def pop(self, timeout: Optional[float] = None) -> Optional[T]:
        """
        Pop an item from the stack.

        Args:
            timeout: Maximum time to wait for an item if stack is empty

        Returns:
            The popped item, or None if timeout occurs or stack is empty
        """
        with self._lock:
            if not self._items:
                if timeout is None:
                    return None

                end_time = time.time() + timeout
                remaining = timeout

                while not self._items and remaining > 0:
                    if not self._not_empty.wait(remaining):
                        return None
                    remaining = end_time - time.time()

            if self._items:
                item = self._items.pop()
                self._not_full.notify()
                return item

            return None

    def peek(self) -> Optional[T]:
        """Look at the top item without removing it."""
        with self._lock:
            return self._items[-1] if self._items else None

    def try_pop(self) -> Optional[T]:
        """Non-blocking pop - returns item if available, None otherwise."""
        with self._lock:
            if self._items:
                item = self._items.pop()
                self._not_full.notify()
                return item
            return None

    def empty(self) -> bool:
        """Check if the stack is empty."""
        with self._lock:
            return len(self._items) == 0

    def full(self) -> bool:
        """Check if the stack is full."""
        with self._lock:
            return self._maxsize > 0 and len(self._items) >= self._maxsize

    def size(self) -> int:
        """Get the current size of the stack."""
        with self._lock:
            return len(self._items)

    def clear(self) -> int:
        """
        Clear all items from the stack.

        Returns:
            Number of items removed
        """
        with self._lock:
            count = len(self._items)
            self._items.clear()
            self._not_full.notify_all()
            return count