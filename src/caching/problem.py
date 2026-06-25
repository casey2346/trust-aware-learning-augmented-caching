"""
Core definitions for the online caching problem.

This file defines the basic objects used throughout the project:
request sequences, cache hits, cache misses, miss ratio, and
simple evaluation utilities for online caching algorithms.

The project studies learning-augmented caching under unreliable
predictions. In later files, we will compare classical online
policies such as LRU and FIFO against prediction-augmented and
trust-aware caching policies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Sequence


Item = int
RequestSequence = Sequence[Item]


@dataclass(frozen=True)
class CacheResult:
    """
    Summary of a caching algorithm's performance on one request sequence.

    Attributes:
        hits: Number of cache hits.
        misses: Number of cache misses.
        total_requests: Total number of requests.
        miss_ratio: Fraction of requests that resulted in a cache miss.
    """

    hits: int
    misses: int
    total_requests: int
    miss_ratio: float


def validate_request_sequence(requests: RequestSequence) -> None:
    """
    Validate that the request sequence is non-empty and contains valid items.

    Args:
        requests: Sequence of requested item identifiers.

    Raises:
        ValueError: If the sequence is empty or contains invalid items.
    """

    if len(requests) == 0:
        raise ValueError("Request sequence must be non-empty.")

    for item in requests:
        if not isinstance(item, int):
            raise ValueError("All requested items must be integers.")
        if item < 0:
            raise ValueError("Requested items must be non-negative integers.")


def validate_cache_size(cache_size: int) -> None:
    """
    Validate the cache size.

    Args:
        cache_size: Number of items that can be stored in cache.

    Raises:
        ValueError: If cache_size is not positive.
    """

    if not isinstance(cache_size, int):
        raise ValueError("Cache size must be an integer.")
    if cache_size <= 0:
        raise ValueError("Cache size must be positive.")


def compute_cache_result(hits: int, misses: int) -> CacheResult:
    """
    Convert hit and miss counts into a CacheResult object.

    Args:
        hits: Number of cache hits.
        misses: Number of cache misses.

    Returns:
        CacheResult containing hits, misses, total requests, and miss ratio.
    """

    total_requests = hits + misses

    if total_requests == 0:
        raise ValueError("Total number of requests must be positive.")

    miss_ratio = misses / total_requests

    return CacheResult(
        hits=hits,
        misses=misses,
        total_requests=total_requests,
        miss_ratio=miss_ratio,
    )


def evaluate_policy(
    requests: RequestSequence,
    cache_size: int,
    policy: Callable[[RequestSequence, int], CacheResult],
) -> CacheResult:
    """
    Evaluate a caching policy on a request sequence.

    Args:
        requests: Sequence of requested items.
        cache_size: Cache capacity.
        policy: Function implementing a caching policy.

    Returns:
        CacheResult for the given policy.
    """

    validate_request_sequence(requests)
    validate_cache_size(cache_size)

    return policy(requests, cache_size)


def unique_items(requests: RequestSequence) -> set[Item]:
    """
    Return the set of unique requested items.

    Args:
        requests: Sequence of requested items.

    Returns:
        Set of item identifiers appearing in the request sequence.
    """

    validate_request_sequence(requests)
    return set(requests)


def prediction_error(true_next_use: int | float, predicted_next_use: int | float) -> float:
    """
    Compute absolute prediction error for a next-use prediction.

    In this project, a prediction estimates when an item will next be requested.
    A larger error means the prediction is less reliable.

    Args:
        true_next_use: True next request time of an item.
        predicted_next_use: Predicted next request time of an item.

    Returns:
        Absolute prediction error.
    """

    return abs(float(true_next_use) - float(predicted_next_use))


if __name__ == "__main__":
    example_requests = [1, 2, 3, 1, 4, 1, 2, 5]
    example_cache_size = 3

    validate_request_sequence(example_requests)
    validate_cache_size(example_cache_size)

    print("Example request sequence:", example_requests)
    print("Cache size:", example_cache_size)
    print("Unique items:", sorted(unique_items(example_requests)))