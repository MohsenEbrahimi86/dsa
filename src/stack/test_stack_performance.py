import threading
import time

from stack.fast_thread_safe_stack import FastNonBlockingStack
from stack.minimal_lock_stack import MinimalLockStack
from stack.optimized_none_blocking_stack import OptimizedNonBlockingStack


def test_stack_performance():
    """Test the performance of our non-blocking stacks."""

    def worker_producer(stack, items, results):
        start_time = time.time()
        for item in items:
            stack.push(item)
        results.append(time.time() - start_time)

    def worker_consumer(stack, count, results):
        start_time = time.time()
        popped = 0
        while popped < count:
            item = stack.pop()
            if item is not None:
                popped += 1
        results.append(time.time() - start_time)

    # Test with different stack implementations
    stacks = [
        ("FastNonBlockingStack", FastNonBlockingStack[int]()),
        ("OptimizedNonBlockingStack", OptimizedNonBlockingStack[int]()),
        ("MinimalLockStack", MinimalLockStack[int]()),
    ]

    for name, stack in stacks:
        print(f"\nTesting {name}:")

        # Test concurrent operations
        num_threads = 4
        items_per_thread = 1_000_000

        # Producer test
        producer_results = []
        consumer_results = []

        threads = []

        # Producers
        for i in range(num_threads):
            items = list(range(i * items_per_thread, (i + 1) * items_per_thread))
            t = threading.Thread(target=worker_producer, args=(stack, items, producer_results))
            threads.append(t)
            t.start()

        # Wait for producers
        for t in threads:
            t.join()

        # Consumers
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=worker_consumer, args=(stack, items_per_thread, consumer_results))
            threads.append(t)
            t.start()

        # Wait for consumers
        for t in threads:
            t.join()

        print(f"  Producers: {len(producer_results)} threads, "
              f"avg time: {sum(producer_results) / len(producer_results):.4f}s")
        print(f"  Consumers: {len(consumer_results)} threads, "
              f"avg time: {sum(consumer_results) / len(consumer_results):.4f}s")
        print(f"  Final size: {stack.size()}")


if __name__ == "__main__":
    test_stack_performance()
