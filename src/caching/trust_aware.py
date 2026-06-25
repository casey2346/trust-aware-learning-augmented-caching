"""
Trust-aware confidence-based caching policy.

This policy combines prediction-guided eviction with LRU-style fallback.

On a cache miss:
    if the cache is full:
        compute an eviction score for each cached item.

The score combines:
    1. predicted next-use rank;
    2. LRU rank.

The confidence value c controls the trade-off:

    c = 1.0  -> fully trust prediction-based eviction
    c = 0.0  -> fall back to LRU eviction
    0 < c < 1 -> interpolate between prediction and LRU

Core idea:
    Confidence controls the trade-off between prediction use and LRU fallback.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Dict

from src.caching.problem import CacheResult, Item, RequestSequence, compute_cache_result
from src.caching.problem import validate_cache_size, validate_request_sequence
from src.caching.prediction_models import PredictionSequence, build_exact_next_use_predictions


def _rank_by_predicted_next_use(
    cache_items: list[Item],
    predictions_at_time: dict[Item, float],
) -> Dict[Item, float]:
    """
    Rank cached items by predicted next-use time.

    Larger rank means the item is predicted to be needed farther in the future,
    so it is a stronger eviction candidate.

    Args:
        cache_items: Current cached items.
        predictions_at_time: Prediction map at the current time step.

    Returns:
        Mapping from item to prediction-based eviction rank.
    """

    sorted_items = sorted(
        cache_items,
        key=lambda item: predictions_at_time.get(item, float("inf")),
    )

    return {item: float(rank) for rank, item in enumerate(sorted_items)}


def _rank_by_lru_order(cache: OrderedDict[Item, None]) -> Dict[Item, float]:
    """
    Rank cached items by LRU order.

    Larger rank means the item is less recently used and should be more likely
    to be evicted under LRU fallback.

    OrderedDict stores items from least recently used to most recently used.

    Args:
        cache: Ordered cache state.

    Returns:
        Mapping from item to LRU-based eviction rank.
    """

    items = list(cache.keys())
    num_items = len(items)

    return {
        item: float(num_items - 1 - index)
        for index, item in enumerate(items)
    }


def _choose_trust_aware_eviction(
    cache: OrderedDict[Item, None],
    predictions_at_time: dict[Item, float],
    confidence: float,
) -> Item:
    """
    Choose an item to evict using confidence-aware interpolation.

    Args:
        cache: Current cache state.
        predictions_at_time: Prediction map at the current time step.
        confidence: Value in [0, 1].

    Returns:
        Item to evict.
    """

    if not cache:
        raise ValueError("Cannot evict from an empty cache.")

    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be in [0, 1].")

    cache_items = list(cache.keys())

    prediction_rank = _rank_by_predicted_next_use(
        cache_items=cache_items,
        predictions_at_time=predictions_at_time,
    )

    lru_rank = _rank_by_lru_order(cache)

    eviction_scores = {
        item: confidence * prediction_rank[item]
        + (1.0 - confidence) * lru_rank[item]
        for item in cache_items
    }

    return max(eviction_scores, key=eviction_scores.get)


def run_trust_aware_cache(
    requests: RequestSequence,
    cache_size: int,
    predictions: PredictionSequence,
    confidence: float,
) -> CacheResult:
    """
    Run confidence-aware trust-aware caching.

    Args:
        requests: Sequence of requested item identifiers.
        cache_size: Maximum number of items in cache.
        predictions: A list of prediction maps, one for each time step.
        confidence: Value in [0, 1] controlling trust in predictions.

    Returns:
        CacheResult containing hits, misses, total requests, and miss ratio.

    Policy:
        - If requested item is in cache, count a hit and update LRU recency.
        - If requested item is not in cache, count a miss.
        - If cache is full, evict using confidence-aware score.
        - Insert requested item as most recently used.
    """

    validate_request_sequence(requests)
    validate_cache_size(cache_size)

    if len(predictions) != len(requests):
        raise ValueError("predictions must have the same length as requests.")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be in [0, 1].")

    cache: OrderedDict[Item, None] = OrderedDict()

    hits = 0
    misses = 0

    for time_index, item in enumerate(requests):
        if item in cache:
            hits += 1
            cache.move_to_end(item)
            continue

        misses += 1

        if len(cache) >= cache_size:
            evicted_item = _choose_trust_aware_eviction(
                cache=cache,
                predictions_at_time=predictions[time_index],
                confidence=confidence,
            )
            del cache[evicted_item]

        cache[item] = None

    return compute_cache_result(hits=hits, misses=misses)


if __name__ == "__main__":
    example_requests = [1, 2, 3, 1, 4, 1, 2, 5]
    example_cache_size = 3
    exact_predictions = build_exact_next_use_predictions(example_requests)

    for confidence in [0.0, 0.5, 1.0]:
        result = run_trust_aware_cache(
            requests=example_requests,
            cache_size=example_cache_size,
            predictions=exact_predictions,
            confidence=confidence,
        )

        print(f"Trust-aware example, confidence={confidence}")
        print("Hits:", result.hits)
        print("Misses:", result.misses)
        print("Miss ratio:", round(result.miss_ratio, 4))