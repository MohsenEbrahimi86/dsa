from queue import LifoQueue
from typing import Optional, TypeVar, Generic
import threading

T = TypeVar('T')


class OptimizedNonBlockingStack(Generic[T]):
    """
    An optimized thread-safe non-blocking stack using Python's built-in LifoQueue.
    This leverages C-level optimizations for maximum performance.
    """

    def __init__(self, maxsize: int = 0):
        self._queue = LifoQueue(maxsize=maxsize)
        self._closed = False
        self._close_lock = threading.Lock()

    def push(self, item: T) -> bool:
        """
        Push an item onto the stack.

        Returns:
            True if successful, False if stack is full
        """
        if self._closed:
            raise RuntimeError("Stack is closed")

        try:
            self._queue.put_nowait(item)
            return True
        except:
            return False

    def pop(self, timeout: Optional[float] = None) -> Optional[T]:
        """
        Pop an item from the stack.

        Returns:
            The popped item, or None if timeout occurs
        """
        if self._closed:
            raise RuntimeError("Stack is closed")

        try:
            return self._queue.get_nowait() if timeout is None else self._queue.get(timeout=timeout)
        except:
            return None

    def try_pop(self) -> Optional[T]:
        """Non-blocking pop."""
        if self._closed:
            raise RuntimeError("Stack is closed")

        try:
            return self._queue.get_nowait()
        except:
            return None

    def peek(self) -> Optional[T]:
        """
        Peek at the top item. Note: This is not truly atomic with pop,
        but provides a best-effort peek.
        """
        if self._closed:
            raise RuntimeError("Stack is closed")

        # This is a limitation - we can't truly peek without potentially
        # removing the item. This implementation removes and re-adds,
        # which means other threads might see the item missing temporarily.
        try:
            item = self._queue.get_nowait()
            self._queue.put_nowait(item)
            return item
        except:
            return None

    def empty(self) -> bool:
        """Check if the stack is empty."""
        return self._queue.empty()

    def full(self) -> bool:
        """Check if the stack is full."""
        return self._queue.full()

    def size(self) -> int:
        """Get the current size."""
        return self._queue.qsize()

    def close(self):
        """Close the stack to prevent further operations."""
        with self._close_lock:
            self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()