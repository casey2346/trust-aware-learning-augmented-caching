"""
Belady's optimal offline caching algorithm.

Belady's algorithm is the classical offline optimal benchmark for caching.
It knows the full future request sequence. When an eviction is needed, it
evicts the cached item whose next future request is farthest away. If a cached
item is never requested again, that item is evicted first.

This algorithm is not implementable online because it uses future information.
In this project, it is used as a lower-bound benchmark for cache misses.
"""

from __future__ import annotations

from math import inf
from typing import Dict, List, Set

from src.caching.problem import CacheResult, Item, RequestSequence, compute_cache_result
from src.caching.problem import validate_cache_size, validate_request_sequence


def _build_future_positions(requests: RequestSequence) -> Dict[Item, List[int]]:
    """
    Build a map from each item to the list of future positions where it appears.

    Args:
        requests: Sequence of requested item identifiers.

    Returns:
        Dictionary mapping each item to a sorted list of request indices.
    """

    future_positions: Dict[Item, List[int]] = {}

    for index, item in enumerate(requests):
        if item not in future_positions:
            future_positions[item] = []
        future_positions[item].append(index)

    return future_positions


def _advance_past_current_position(
    future_positions: Dict[Item, List[int]],
    item: Item,
    current_index: int,
) -> None:
    """
    Remove positions up to and including the current request index.

    Args:
        future_positions: Future-position dictionary.
        item: Requested item.
        current_index: Current time index.
    """

    positions = future_positions[item]

    while positions and positions[0] <= current_index:
        positions.pop(0)


def _next_use_time(future_positions: Dict[Item, List[int]], item: Item) -> float:
    """
    Return the next future use time of an item.

    Args:
        future_positions: Future-position dictionary.
        item: Cached item.

    Returns:
        Next future index if the item appears again; infinity otherwise.
    """

    positions = future_positions.get(item, [])

    if not positions:
        return inf

    return float(positions[0])


def _choose_belady_eviction(
    cache_items: Set[Item],
    future_positions: Dict[Item, List[int]],
) -> Item:
    """
    Choose the item Belady would evict.

    Belady evicts the cached item with the farthest next future request.
    If an item is never requested again, its next-use time is infinity and
    it is evicted first.

    Args:
        cache_items: Current cache contents.
        future_positions: Future-position dictionary.

    Returns:
        Item to evict.
    """

    if not cache_items:
        raise ValueError("Cannot evict from an empty cache.")

    return max(cache_items, key=lambda item: _next_use_time(future_positions, item))


def run_belady_cache(requests: RequestSequence, cache_size: int) -> CacheResult:
    """
    Run Belady's optimal offline caching algorithm.

    Args:
        requests: Sequence of requested item identifiers.
        cache_size: Maximum number of items that can be stored in cache.

    Returns:
        CacheResult containing hits, misses, total requests, and miss ratio.

    Policy:
        - If the requested item is already in cache, count a hit.
        - If the requested item is not in cache, count a miss.
        - If the cache is full, evict the cached item whose next future use is
          farthest away.
        - If a cached item never appears again, evict it first.
    """

    validate_request_sequence(requests)
    validate_cache_size(cache_size)

    future_positions = _build_future_positions(requests)
    cache_items: Set[Item] = set()

    hits = 0
    misses = 0

    for current_index, item in enumerate(requests):
        _advance_past_current_position(future_positions, item, current_index)

        if item in cache_items:
            hits += 1
            continue

        misses += 1

        if len(cache_items) >= cache_size:
            evicted_item = _choose_belady_eviction(cache_items, future_positions)
            cache_items.remove(evicted_item)

        cache_items.add(item)

    return compute_cache_result(hits=hits, misses=misses)


if __name__ == "__main__":
    example_requests = [1, 2, 3, 1, 4, 1, 2, 5]
    example_cache_size = 3

    result = run_belady_cache(example_requests, example_cache_size)

    print("Belady example")
    print("Requests:", example_requests)
    print("Cache size:", example_cache_size)
    print("Hits:", result.hits)
    print("Misses:", result.misses)
    print("Miss ratio:", round(result.miss_ratio, 4))