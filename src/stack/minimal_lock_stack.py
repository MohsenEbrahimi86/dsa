import threading
from typing import Optional, TypeVar, Generic

T = TypeVar('T')


class MinimalLockStack(Generic[T]):
    """
    A stack implementation that minimizes locking by using atomic operations
    at the Python interpreter level (list operations are atomic for append/pop).
    """

    def __init__(self, maxsize: int = 0):
        self._items = []
        self._maxsize = maxsize
        self._lock = threading.Lock()  # Only used for size checks when maxsize > 0

    def push(self, item: T) -> bool:
        """Push with minimal locking."""
        if self._maxsize > 0:
            with self._lock:
                if len(self._items) >= self._maxsize:
                    return False

        # List append is atomic in CPython due to GIL
        self._items.append(item)
        return True

    def pop(self) -> Optional[T]:
        """Pop with minimal locking."""
        # List pop is atomic in CPython
        if self._items:
            return self._items.pop()
        return None

    def try_pop(self) -> Optional[T]:
        """Non-blocking pop."""
        return self.pop()  # Same as pop in this implementation

    def empty(self) -> bool:
        """Check if empty."""
        return len(self._items) == 0

    def size(self) -> int:
        """Get size."""
        return len(self._items)