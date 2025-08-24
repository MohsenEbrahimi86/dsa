We can implement a thread-safe non-blocking stack using Python's atomic operations at the interpreter level and the queue module.

- Here's a high-performance implementation:
  [FastNoneBlockingStack](https://github.com/MohsenEbrahimi86/dsa/blob/main/stack/fast_none_blocking_stack.py)

- For even better performance, here's a version that uses queue.LifoQueue (which is implemented in C and highly optimized):
  [OptimizedNoneBlockingStack](https://github.com/MohsenEbrahimi86/dsa/blob/main/stack/optimized_none_blocking_stack.py)

- Here's a high-performance version that minimizes locking for the common case:
  [MinimalLockStack](https://github.com/MohsenEbrahimi86/dsa/blob/main/stack/minimal_lock_stack.py)

Run performance test:

```commandline
python test_stack_performance.py
```

An example output for 1M items per thread:

```commandline
Testing FastNonBlockingStack:
  Producers: 4 threads, avg time: 15.6520s
  Consumers: 4 threads, avg time: 19.9530s
  Final size: 0

Testing OptimizedNonBlockingStack:
  Producers: 4 threads, avg time: 24.4803s
  Consumers: 4 threads, avg time: 24.6686s
  Final size: 0

Testing MinimalLockStack:
  Producers: 4 threads, avg time: 0.2635s
  Consumers: 4 threads, avg time: 0.3843s
  Final size: 0
```

Key Features:

1. Thread-Safe: All operations are protected against race conditions
2. Non-Blocking: Uses try_pop() and non-blocking operations where possible
3. High Performance: Leverages Python's atomic list operations and optimized C implementations
4. Flexible: Supports timeouts, size limits, and various usage patterns
   Memory Efficient: Minimal overhead

## Important Notes for Python:

- Python's GIL (Global Interpreter Lock) makes many operations atomic at the interpreter level
- List append() and pop() operations are atomic in CPython
- For maximum performance, the MinimalLockStack leverages this fact
- The OptimizedNonBlockingStack uses Python's built-in LifoQueue which is implemented in C

Choose the implementation based on your needs.
