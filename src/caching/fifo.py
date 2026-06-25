"""
First In First Out caching baseline.

FIFO is a classical online caching policy. It evicts the item that entered
the cache earliest when the cache is full and a new item must be loaded.

Unlike LRU, FIFO does not use recency of access after insertion. This makes
it a useful baseline for comparing how much recency information helps in
online caching.
"""

from __future__ import annotations

from collections import deque
from typing import Deque, Set

from src.caching.problem import CacheResult, Item, RequestSequence, compute_cache_result
from src.caching.problem import validate_cache_size, validate_request_sequence


def run_fifo_cache(requests: RequestSequence, cache_size: int) -> CacheResult:
    """
    Run the First In First Out caching policy.

    Args:
        requests: Sequence of requested item identifiers.
        cache_size: Maximum number of items that can be stored in cache.

    Returns:
        CacheResult containing hits, misses, total requests, and miss ratio.

    Policy:
        - If the requested item is already in cache, count a hit.
        - FIFO does not update item order after a hit.
        - If the item is not in cache, count a miss.
        - If the cache is full, evict the item that was inserted earliest.
        - Insert the requested item at the back of the FIFO queue.
    """

    validate_request_sequence(requests)
    validate_cache_size(cache_size)

    cache_items: Set[Item] = set()
    insertion_order: Deque[Item] = deque()

    hits = 0
    misses = 0

    for item in requests:
        if item in cache_items:
            hits += 1
        else:
            misses += 1

            if len(cache_items) >= cache_size:
                evicted_item = insertion_order.popleft()
                cache_items.remove(evicted_item)

            cache_items.add(item)
            insertion_order.append(item)

    return compute_cache_result(hits=hits, misses=misses)


if __name__ == "__main__":
    example_requests = [1, 2, 3, 1, 4, 1, 2, 5]
    example_cache_size = 3

    result = run_fifo_cache(example_requests, example_cache_size)

    print("FIFO example")
    print("Requests:", example_requests)
    print("Cache size:", example_cache_size)
    print("Hits:", result.hits)
    print("Misses:", result.misses)
    print("Miss ratio:", round(result.miss_ratio, 4))