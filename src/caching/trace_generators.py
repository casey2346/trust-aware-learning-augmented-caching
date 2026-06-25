"""
Synthetic request trace generators for caching experiments.

This file provides several controlled request-sequence generators:

1. uniform random trace;
2. Zipf-distributed trace;
3. burst trace;
4. video/CDN-style trace;
5. adversarial trace.

These traces allow the project to test caching algorithms under different
workload patterns, from simple random requests to skewed, bursty, and
adversarial request sequences.
"""

from __future__ import annotations

import random
from typing import List

import numpy as np

from src.caching.problem import Item, RequestSequence, validate_request_sequence


def generate_uniform_trace(
    num_requests: int,
    num_items: int,
    seed: int = 0,
) -> list[Item]:
    """
    Generate a uniform random request trace.

    Each item has approximately equal probability of being requested.

    Args:
        num_requests: Length of the request sequence.
        num_items: Number of distinct items.
        seed: Random seed for reproducibility.

    Returns:
        Request sequence.
    """

    if num_requests <= 0:
        raise ValueError("num_requests must be positive.")
    if num_items <= 0:
        raise ValueError("num_items must be positive.")

    rng = random.Random(seed)

    return [rng.randint(1, num_items) for _ in range(num_requests)]


def generate_zipf_trace(
    num_requests: int,
    num_items: int,
    alpha: float = 1.1,
    seed: int = 0,
) -> list[Item]:
    """
    Generate a Zipf-distributed request trace.

    A small number of popular items are requested frequently, while many
    long-tail items are requested rarely. This is a useful approximation for
    CDN, web, and video request workloads.

    Args:
        num_requests: Length of the request sequence.
        num_items: Number of distinct items.
        alpha: Zipf skew parameter. Larger alpha means stronger popularity skew.
        seed: Random seed for reproducibility.

    Returns:
        Request sequence.
    """

    if num_requests <= 0:
        raise ValueError("num_requests must be positive.")
    if num_items <= 0:
        raise ValueError("num_items must be positive.")
    if alpha <= 0:
        raise ValueError("alpha must be positive.")

    rng = np.random.default_rng(seed)

    ranks = np.arange(1, num_items + 1)
    probabilities = 1.0 / np.power(ranks, alpha)
    probabilities = probabilities / probabilities.sum()

    items = np.arange(1, num_items + 1)
    requests = rng.choice(items, size=num_requests, p=probabilities)

    return requests.astype(int).tolist()


def generate_burst_trace(
    num_requests: int,
    num_items: int,
    burst_length: int = 20,
    hot_set_size: int = 5,
    seed: int = 0,
) -> list[Item]:
    """
    Generate a bursty request trace.

    The trace switches between different hot sets. During each burst, requests
    concentrate on a small group of items.

    Args:
        num_requests: Length of the request sequence.
        num_items: Number of distinct items.
        burst_length: Number of requests per burst.
        hot_set_size: Number of hot items active in each burst.
        seed: Random seed for reproducibility.

    Returns:
        Request sequence.
    """

    if num_requests <= 0:
        raise ValueError("num_requests must be positive.")
    if num_items <= 0:
        raise ValueError("num_items must be positive.")
    if burst_length <= 0:
        raise ValueError("burst_length must be positive.")
    if hot_set_size <= 0 or hot_set_size > num_items:
        raise ValueError("hot_set_size must be between 1 and num_items.")

    rng = random.Random(seed)
    requests: list[Item] = []

    while len(requests) < num_requests:
        hot_set = rng.sample(range(1, num_items + 1), hot_set_size)

        for _ in range(burst_length):
            if len(requests) >= num_requests:
                break
            requests.append(rng.choice(hot_set))

    return requests


def generate_video_cdn_trace(
    num_requests: int,
    num_videos: int,
    hot_video_count: int = 10,
    burst_probability: float = 0.15,
    seed: int = 0,
) -> list[Item]:
    """
    Generate a simple video/CDN-style request trace.

    The trace combines:
    - a small set of popular videos;
    - a long tail of rarely requested videos;
    - occasional bursts caused by trending content.

    Args:
        num_requests: Length of the request sequence.
        num_videos: Number of distinct video items.
        hot_video_count: Number of globally popular videos.
        burst_probability: Probability of a burst-style request.
        seed: Random seed for reproducibility.

    Returns:
        Request sequence.
    """

    if num_requests <= 0:
        raise ValueError("num_requests must be positive.")
    if num_videos <= 0:
        raise ValueError("num_videos must be positive.")
    if hot_video_count <= 0 or hot_video_count > num_videos:
        raise ValueError("hot_video_count must be between 1 and num_videos.")
    if not 0 <= burst_probability <= 1:
        raise ValueError("burst_probability must be in [0, 1].")

    rng = random.Random(seed)

    hot_videos = list(range(1, hot_video_count + 1))
    long_tail_videos = list(range(hot_video_count + 1, num_videos + 1))

    requests: list[Item] = []
    current_trending_video = rng.choice(hot_videos)

    for t in range(num_requests):
        if t % 50 == 0:
            current_trending_video = rng.randint(1, num_videos)

        roll = rng.random()

        if roll < burst_probability:
            requests.append(current_trending_video)
        elif roll < 0.75:
            requests.append(rng.choice(hot_videos))
        else:
            requests.append(rng.choice(long_tail_videos))

    return requests


def generate_adversarial_trace(
    num_blocks: int = 30,
    cache_size: int = 3,
) -> list[Item]:
    """
    Generate an adversarial-style request trace.

    This trace repeatedly changes the active working set. It is designed to be
    difficult for policies that over-trust stale or shifted predictions.

    Args:
        num_blocks: Number of adversarial blocks.
        cache_size: Intended cache size used to structure the trace.

    Returns:
        Request sequence.
    """

    if num_blocks <= 0:
        raise ValueError("num_blocks must be positive.")
    if cache_size <= 0:
        raise ValueError("cache_size must be positive.")

    requests: list[Item] = []

    for block in range(num_blocks):
        old_hot_items = list(range(1, cache_size + 1))
        new_hot_items = list(
            range(
                cache_size + 1 + block * cache_size,
                cache_size + 1 + (block + 1) * cache_size,
            )
        )

        requests.extend(old_hot_items)
        requests.extend(old_hot_items)
        requests.extend(new_hot_items)
        requests.extend(new_hot_items)
        requests.append(10000 + block)

    return requests


def summarize_trace(requests: RequestSequence) -> dict[str, float]:
    """
    Summarize a request trace.

    Args:
        requests: Request sequence.

    Returns:
        Dictionary with trace length, number of unique items, and repetition rate.
    """

    validate_request_sequence(requests)

    total_requests = len(requests)
    unique_count = len(set(requests))
    repetition_rate = 1.0 - (unique_count / total_requests)

    return {
        "total_requests": float(total_requests),
        "unique_items": float(unique_count),
        "repetition_rate": repetition_rate,
    }


if __name__ == "__main__":
    generators = {
        "uniform": generate_uniform_trace(50, 20, seed=1),
        "zipf": generate_zipf_trace(50, 20, alpha=1.1, seed=1),
        "burst": generate_burst_trace(50, 20, seed=1),
        "video_cdn": generate_video_cdn_trace(50, 30, seed=1),
        "adversarial": generate_adversarial_trace(num_blocks=5, cache_size=3),
    }

    for name, trace in generators.items():
        summary = summarize_trace(trace)
        print(name, summary)
        print("first 20 requests:", trace[:20])