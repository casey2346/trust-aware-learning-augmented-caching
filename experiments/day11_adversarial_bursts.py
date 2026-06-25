"""
Day 11 experiment: adversarial burst sequence.

This experiment creates a streaming/CDN-style workload where the active hot
items suddenly switch from an old hot set to a new hot set.

The adversarial prediction model stays stale: it continues to believe the old
hot items are important and the new hot items are far away. As a result,
pure prediction-augmented caching can evict the wrong items and suffer many
misses.

LRU adapts by recency.
Trust-aware caching reduces damage by mixing prediction use with LRU fallback.

Output:
    figures/day11_adversarial_burst_failure.png
"""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import Dict, Iterable

import matplotlib.pyplot as plt

from src.caching.problem import Item


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)


def generate_adversarial_burst_trace(
    num_phases: int = 8,
    phase_length: int = 160,
    hot_set_size: int = 12,
    noise_items_per_phase: int = 10,
) -> tuple[list[Item], list[set[Item]]]:
    """
    Generate a burst trace where the active hot set changes suddenly.

    Args:
        num_phases: Number of hot-set phases.
        phase_length: Number of requests per phase.
        hot_set_size: Number of hot items per phase.
        noise_items_per_phase: Number of one-off noise items per phase.

    Returns:
        Tuple of request sequence and active hot sets.
    """

    requests: list[Item] = []
    hot_sets: list[set[Item]] = []

    for phase in range(num_phases):
        hot_start = phase * 100 + 1
        hot_items = list(range(hot_start, hot_start + hot_set_size))
        hot_sets.append(set(hot_items))

        noise_start = 10000 + phase * 100

        for t in range(phase_length):
            if t % 17 == 0:
                requests.append(noise_start + (t % noise_items_per_phase))
            else:
                requests.append(hot_items[t % hot_set_size])

    return requests, hot_sets


def build_stale_predictions(
    requests: list[Item],
    hot_sets: list[set[Item]],
    phase_length: int,
) -> list[Dict[Item, float]]:
    """
    Build stale adversarial predictions.

    At each phase, the model still trusts the previous phase's hot set.
    New hot items are predicted to be far away, so prediction-based eviction
    is likely to evict them even though they are currently useful.

    Args:
        requests: Request sequence.
        hot_sets: Active hot sets by phase.
        phase_length: Number of requests per phase.

    Returns:
        Prediction maps, one per time step.
    """

    all_items = sorted(set(requests))
    horizon = len(requests) + 1000

    predictions: list[Dict[Item, float]] = []

    for time_index in range(len(requests)):
        phase = min(time_index // phase_length, len(hot_sets) - 1)

        if phase == 0:
            stale_hot_set = hot_sets[0]
        else:
            stale_hot_set = hot_sets[phase - 1]

        current_hot_set = hot_sets[phase]

        prediction_map: Dict[Item, float] = {}

        for item in all_items:
            if item in stale_hot_set:
                prediction_map[item] = float(time_index + 1)
            elif item in current_hot_set:
                prediction_map[item] = float(horizon)
            else:
                prediction_map[item] = float(horizon // 2)

        predictions.append(prediction_map)

    return predictions


def rolling_average(values: list[int], window_size: int) -> list[float]:
    """
    Compute rolling average over binary miss indicators.

    Args:
        values: List of 0/1 miss indicators.
        window_size: Rolling window size.

    Returns:
        Rolling average list.
    """

    rolling: list[float] = []

    for index in range(len(values)):
        start = max(0, index - window_size + 1)
        window = values[start : index + 1]
        rolling.append(sum(window) / len(window))

    return rolling


def run_lru_miss_series(requests: list[Item], cache_size: int) -> list[int]:
    """
    Run LRU and return per-time-step miss indicators.
    """

    cache: OrderedDict[Item, None] = OrderedDict()
    misses: list[int] = []

    for item in requests:
        if item in cache:
            cache.move_to_end(item)
            misses.append(0)
        else:
            misses.append(1)

            if len(cache) >= cache_size:
                cache.popitem(last=False)

            cache[item] = None

    return misses


def choose_prediction_eviction(
    cache_items: Iterable[Item],
    predictions_at_time: Dict[Item, float],
) -> Item:
    """
    Evict item with farthest predicted next use.
    """

    return max(cache_items, key=lambda item: predictions_at_time.get(item, float("inf")))


def run_prediction_augmented_miss_series(
    requests: list[Item],
    cache_size: int,
    predictions: list[Dict[Item, float]],
) -> list[int]:
    """
    Run prediction-augmented caching and return per-time-step misses.
    """

    cache: set[Item] = set()
    misses: list[int] = []

    for time_index, item in enumerate(requests):
        if item in cache:
            misses.append(0)
            continue

        misses.append(1)

        if len(cache) >= cache_size:
            evicted = choose_prediction_eviction(cache, predictions[time_index])
            cache.remove(evicted)

        cache.add(item)

    return misses


def choose_trust_aware_eviction(
    cache: OrderedDict[Item, None],
    predictions_at_time: Dict[Item, float],
    confidence: float,
) -> Item:
    """
    Choose eviction using confidence-aware combination of prediction and LRU ranks.
    """

    cache_items = list(cache.keys())

    prediction_sorted = sorted(
        cache_items,
        key=lambda item: predictions_at_time.get(item, float("inf")),
    )
    prediction_rank = {
        item: float(rank)
        for rank, item in enumerate(prediction_sorted)
    }

    # OrderedDict stores least recently used first and most recently used last.
    # Larger LRU rank means less recently used and stronger eviction candidate.
    num_items = len(cache_items)
    lru_rank = {
        item: float(num_items - 1 - index)
        for index, item in enumerate(cache_items)
    }

    scores = {
        item: confidence * prediction_rank[item]
        + (1.0 - confidence) * lru_rank[item]
        for item in cache_items
    }

    return max(scores, key=scores.get)


def run_trust_aware_miss_series(
    requests: list[Item],
    cache_size: int,
    predictions: list[Dict[Item, float]],
    confidence: float,
) -> list[int]:
    """
    Run trust-aware caching and return per-time-step misses.
    """

    cache: OrderedDict[Item, None] = OrderedDict()
    misses: list[int] = []

    for time_index, item in enumerate(requests):
        if item in cache:
            cache.move_to_end(item)
            misses.append(0)
            continue

        misses.append(1)

        if len(cache) >= cache_size:
            evicted = choose_trust_aware_eviction(
                cache=cache,
                predictions_at_time=predictions[time_index],
                confidence=confidence,
            )
            del cache[evicted]

        cache[item] = None

    return misses


def run_adversarial_burst_experiment() -> None:
    """
    Run adversarial burst experiment and plot rolling miss ratio over time.
    """

    cache_size = 12
    phase_length = 160

    requests, hot_sets = generate_adversarial_burst_trace(
        num_phases=8,
        phase_length=phase_length,
        hot_set_size=12,
        noise_items_per_phase=10,
    )

    predictions = build_stale_predictions(
        requests=requests,
        hot_sets=hot_sets,
        phase_length=phase_length,
    )

    lru_misses = run_lru_miss_series(requests, cache_size)
    pred_misses = run_prediction_augmented_miss_series(
        requests=requests,
        cache_size=cache_size,
        predictions=predictions,
    )
    trust_025_misses = run_trust_aware_miss_series(
        requests=requests,
        cache_size=cache_size,
        predictions=predictions,
        confidence=0.25,
    )
    trust_050_misses = run_trust_aware_miss_series(
        requests=requests,
        cache_size=cache_size,
        predictions=predictions,
        confidence=0.50,
    )
    trust_075_misses = run_trust_aware_miss_series(
        requests=requests,
        cache_size=cache_size,
        predictions=predictions,
        confidence=0.75,
    )

    window_size = 50
    time_axis = list(range(len(requests)))

    lru_rolling = rolling_average(lru_misses, window_size)
    pred_rolling = rolling_average(pred_misses, window_size)
    trust_025_rolling = rolling_average(trust_025_misses, window_size)
    trust_050_rolling = rolling_average(trust_050_misses, window_size)
    trust_075_rolling = rolling_average(trust_075_misses, window_size)

    print(f"Final LRU miss ratio: {sum(lru_misses) / len(lru_misses):.4f}")
    print(f"Final prediction-augmented miss ratio: {sum(pred_misses) / len(pred_misses):.4f}")
    print(f"Final trust-aware c=0.25 miss ratio: {sum(trust_025_misses) / len(trust_025_misses):.4f}")
    print(f"Final trust-aware c=0.50 miss ratio: {sum(trust_050_misses) / len(trust_050_misses):.4f}")
    print(f"Final trust-aware c=0.75 miss ratio: {sum(trust_075_misses) / len(trust_075_misses):.4f}")

    plt.figure(figsize=(10, 5.4))

    plt.plot(time_axis, lru_rolling, label="LRU")
    plt.plot(time_axis, pred_rolling, label="Prediction-augmented")
    plt.plot(time_axis, trust_025_rolling, label="Trust-aware c=0.25")
    plt.plot(time_axis, trust_050_rolling, label="Trust-aware c=0.50")
    plt.plot(time_axis, trust_075_rolling, label="Trust-aware c=0.75")

    for phase_boundary in range(phase_length, len(requests), phase_length):
        plt.axvline(phase_boundary, linestyle="--", alpha=0.25)

    plt.xlabel("Time")
    plt.ylabel("Rolling cache miss ratio")
    plt.title("Day 11: Adversarial burst sequence with stale predictions")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURE_DIR / "day11_adversarial_burst_failure.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved figure to {output_path}")


if __name__ == "__main__":
    run_adversarial_burst_experiment()