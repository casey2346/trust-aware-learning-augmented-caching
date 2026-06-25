"""
Day 3 experiment: FIFO vs LRU baseline comparison.

This experiment compares two classical online caching policies:

1. LRU: evicts the least recently used item.
2. FIFO: evicts the earliest inserted item.

The goal is to show that LRU uses recency information, while FIFO only uses
insertion order. This provides a stronger baseline setup for later comparison
against Belady, prediction-augmented caching, and trust-aware caching.

Output:
    figures/day3_fifo_vs_lru.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from src.caching.fifo import run_fifo_cache
from src.caching.lru import run_lru_cache


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)


def generate_locality_trace(num_repetitions: int = 25) -> list[int]:
    """
    Generate a request trace with temporal locality.

    The trace repeatedly returns to recently used items. This is useful for
    showing why LRU can outperform FIFO: LRU keeps recently requested items,
    while FIFO may evict them simply because they entered the cache earlier.

    Args:
        num_repetitions: Number of repeated trace blocks.

    Returns:
        Request sequence with locality and occasional new items.
    """

    requests: list[int] = []

    for block in range(num_repetitions):
        hot_a = 1
        hot_b = 2
        rotating_item = 3 + (block % 8)

        requests.extend(
            [
                hot_a,
                hot_b,
                rotating_item,
                hot_a,
                hot_b,
                rotating_item,
                hot_a,
                hot_b,
                20 + block,
                hot_a,
                hot_b,
            ]
        )

    return requests


def run_fifo_vs_lru_experiment() -> None:
    """
    Compare FIFO and LRU across different cache sizes.
    """

    requests = generate_locality_trace(num_repetitions=30)
    cache_sizes = list(range(1, 11))

    lru_miss_ratios: list[float] = []
    fifo_miss_ratios: list[float] = []

    for cache_size in cache_sizes:
        lru_result = run_lru_cache(requests=requests, cache_size=cache_size)
        fifo_result = run_fifo_cache(requests=requests, cache_size=cache_size)

        lru_miss_ratios.append(lru_result.miss_ratio)
        fifo_miss_ratios.append(fifo_result.miss_ratio)

        print(
            f"cache_size={cache_size}, "
            f"LRU miss_ratio={lru_result.miss_ratio:.4f}, "
            f"FIFO miss_ratio={fifo_result.miss_ratio:.4f}"
        )

    plt.figure(figsize=(7, 4.5))
    plt.plot(cache_sizes, lru_miss_ratios, marker="o", label="LRU")
    plt.plot(cache_sizes, fifo_miss_ratios, marker="s", label="FIFO")

    plt.xlabel("Cache size")
    plt.ylabel("Cache miss ratio")
    plt.title("Day 3: FIFO vs LRU baseline comparison")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURE_DIR / "day3_fifo_vs_lru.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved figure to {output_path}")


if __name__ == "__main__":
    run_fifo_vs_lru_experiment()