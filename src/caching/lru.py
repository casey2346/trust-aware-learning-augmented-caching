"""
Least Recently Used caching baseline.

LRU is a classical online caching policy. It evicts the item that was
requested least recently when the cache is full and a new item must be loaded.

This file provides a clean baseline for later comparison against FIFO,
Belady optimal offline caching, prediction-augmented caching, and
trust-aware caching.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Sequence

from src.caching.problem import CacheResult, Item, RequestSequence, compute_cache_result
from src.caching.problem import validate_cache_size, validate_request_sequence


def run_lru_cache(requests: RequestSequence, cache_size: int) -> CacheResult:
    """
    Run the Least Recently Used caching policy.

    Args:
        requests: Sequence of requested item identifiers.
        cache_size: Maximum number of items that can be stored in cache.

    Returns:
        CacheResult containing hits, misses, total requests, and miss ratio.

    Policy:
        - If the requested item is already in cache, count a hit and mark it
          as most recently used.
        - If the item is not in cache, count a miss.
        - If the cache is full, evict the least recently used item.
        - Insert the requested item as most recently used.
    """

    validate_request_sequence(requests)
    validate_cache_size(cache_size)

    cache: OrderedDict[Item, None] = OrderedDict()
    hits = 0
    misses = 0

    for item in requests:
        if item in cache:
            hits += 1
            cache.move_to_end(item)
        else:
            misses += 1

            if len(cache) >= cache_size:
                cache.popitem(last=False)

            cache[item] = None

    return compute_cache_result(hits=hits, misses=misses)


if __name__ == "__main__":
    example_requests = [1, 2, 3, 1, 4, 1, 2, 5]
    example_cache_size = 3

    result = run_lru_cache(example_requests, example_cache_size)

    print("LRU example")
    print("Requests:", example_requests)
    print("Cache size:", example_cache_size)
    print("Hits:", result.hits)
    print("Misses:", result.misses)
    print("Miss ratio:", round(result.miss_ratio, 4))