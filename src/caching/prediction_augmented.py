"""
Prediction-augmented caching policy.

This policy uses predicted next-use times to decide which cached item to evict.

On a cache miss:
    if the cache is full:
        evict the cached item with the farthest predicted next use.

If predictions are accurate, this policy can approach Belady-style behavior.
If predictions are inaccurate, it may perform worse than robust online
baselines such as LRU.
"""

from __future__ import annotations

from typing import Set

from src.caching.problem import CacheResult, Item, RequestSequence, compute_cache_result
from src.caching.problem import validate_cache_size, validate_request_sequence
from src.caching.prediction_models import PredictionSequence, build_exact_next_use_predictions


def _choose_prediction_based_eviction(
    cache_items: Set[Item],
    predictions_at_time: dict[Item, float],
) -> Item:
    """
    Choose the cached item with the farthest predicted next use.

    Args:
        cache_items: Current cache contents.
        predictions_at_time: Prediction map at the current time step.

    Returns:
        Item to evict.
    """

    if not cache_items:
        raise ValueError("Cannot evict from an empty cache.")

    return max(
        cache_items,
        key=lambda item: predictions_at_time.get(item, float("inf")),
    )


def run_prediction_augmented_cache(
    requests: RequestSequence,
    cache_size: int,
    predictions: PredictionSequence,
) -> CacheResult:
    """
    Run prediction-augmented caching.

    Args:
        requests: Sequence of requested item identifiers.
        cache_size: Maximum number of items in cache.
        predictions: A list of prediction maps, one for each time step.

    Returns:
        CacheResult containing hits, misses, total requests, and miss ratio.

    Policy:
        - If the requested item is already in cache, count a hit.
        - If the requested item is not in cache, count a miss.
        - If the cache is full, evict the item whose predicted next use is
          farthest in the future.
        - Insert the requested item.
    """

    validate_request_sequence(requests)
    validate_cache_size(cache_size)

    if len(predictions) != len(requests):
        raise ValueError("predictions must have the same length as requests.")

    cache_items: Set[Item] = set()

    hits = 0
    misses = 0

    for time_index, item in enumerate(requests):
        if item in cache_items:
            hits += 1
            continue

        misses += 1

        if len(cache_items) >= cache_size:
            evicted_item = _choose_prediction_based_eviction(
                cache_items=cache_items,
                predictions_at_time=predictions[time_index],
            )
            cache_items.remove(evicted_item)

        cache_items.add(item)

    return compute_cache_result(hits=hits, misses=misses)


if __name__ == "__main__":
    example_requests = [1, 2, 3, 1, 4, 1, 2, 5]
    example_cache_size = 3

    exact_predictions = build_exact_next_use_predictions(example_requests)

    result = run_prediction_augmented_cache(
        requests=example_requests,
        cache_size=example_cache_size,
        predictions=exact_predictions,
    )

    print("Prediction-augmented caching example")
    print("Requests:", example_requests)
    print("Cache size:", example_cache_size)
    print("Hits:", result.hits)
    print("Misses:", result.misses)
    print("Miss ratio:", round(result.miss_ratio, 4))