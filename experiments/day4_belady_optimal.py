"""
Day 4 experiment: Belady optimal offline benchmark.

This experiment compares:

1. Belady optimal offline caching;
2. LRU online caching;
3. FIFO online caching.

Belady is used as the offline lower-bound benchmark for cache misses.
It is not an online algorithm because it uses future request information.

Output:
    figures/day4_belady_vs_lru_fifo.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from src.caching.belady import run_belady_cache
from src.caching.fifo import run_fifo_cache
from src.caching.lru import run_lru_cache


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)


def generate_belady_comparison_trace(num_repetitions: int = 25) -> list[int]:
    """
    Generate a request trace with locality, repeated hot items, and disruptions.

    The trace is designed to show why an offline optimal benchmark is useful:
    Belady can use future information to make better eviction choices than
    online policies such as LRU and FIFO.

    Args:
        num_repetitions: Number of repeated trace blocks.

    Returns:
        Request sequence.
    """

    requests: list[int] = []

    for block in range(num_repetitions):
        hot_a = 1
        hot_b = 2
        hot_c = 3
        rotating_item = 10 + (block % 8)
        one_time_item = 100 + block

        requests.extend(
            [
                hot_a,
                hot_b,
                hot_c,
                hot_a,
                hot_b,
                rotating_item,
                hot_a,
                hot_b,
                one_time_item,
                hot_a,
                hot_c,
                hot_b,
            ]
        )

    return requests


def run_belady_experiment() -> None:
    """
    Compare Belady, LRU, and FIFO across cache sizes.
    """

    requests = generate_belady_comparison_trace(num_repetitions=30)
    cache_sizes = list(range(1, 11))

    belady_miss_ratios: list[float] = []
    lru_miss_ratios: list[float] = []
    fifo_miss_ratios: list[float] = []

    for cache_size in cache_sizes:
        belady_result = run_belady_cache(requests=requests, cache_size=cache_size)
        lru_result = run_lru_cache(requests=requests, cache_size=cache_size)
        fifo_result = run_fifo_cache(requests=requests, cache_size=cache_size)

        belady_miss_ratios.append(belady_result.miss_ratio)
        lru_miss_ratios.append(lru_result.miss_ratio)
        fifo_miss_ratios.append(fifo_result.miss_ratio)

        print(
            f"cache_size={cache_size}, "
            f"Belady={belady_result.miss_ratio:.4f}, "
            f"LRU={lru_result.miss_ratio:.4f}, "
            f"FIFO={fifo_result.miss_ratio:.4f}"
        )

    plt.figure(figsize=(7, 4.5))
    plt.plot(cache_sizes, belady_miss_ratios, marker="o", label="Belady optimal")
    plt.plot(cache_sizes, lru_miss_ratios, marker="s", label="LRU")
    plt.plot(cache_sizes, fifo_miss_ratios, marker="^", label="FIFO")

    plt.xlabel("Cache size")
    plt.ylabel("Cache miss ratio")
    plt.title("Day 4: Belady offline optimum vs online baselines")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURE_DIR / "day4_belady_vs_lru_fifo.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved figure to {output_path}")


if __name__ == "__main__":
    run_belady_experiment()