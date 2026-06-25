"""
Day 2 experiment: LRU baseline cache-size sweep.

This experiment evaluates the Least Recently Used caching policy across
different cache sizes. The expected pattern is that miss ratio decreases
as cache size increases.

Output:
    figures/day2_lru_cache_size_sweep.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from src.caching.lru import run_lru_cache


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)


def generate_repeated_trace(num_repetitions: int = 20) -> list[int]:
    """
    Generate a simple repeated request trace.

    The trace contains repeated accesses to a small working set plus occasional
    new items. This makes it useful for visualizing how larger caches reduce
    the miss ratio under LRU.

    Args:
        num_repetitions: Number of repeated pattern blocks.

    Returns:
        Request sequence.
    """

    base_pattern = [1, 2, 3, 1, 4, 1, 2, 5, 1, 2, 3, 6]
    requests: list[int] = []

    for _ in range(num_repetitions):
        requests.extend(base_pattern)

    return requests


def run_cache_size_sweep() -> None:
    """
    Run LRU across a range of cache sizes and plot miss ratio.
    """

    requests = generate_repeated_trace(num_repetitions=30)
    cache_sizes = list(range(1, 11))

    miss_ratios = []

    for cache_size in cache_sizes:
        result = run_lru_cache(requests=requests, cache_size=cache_size)
        miss_ratios.append(result.miss_ratio)

        print(
            f"cache_size={cache_size}, "
            f"hits={result.hits}, "
            f"misses={result.misses}, "
            f"miss_ratio={result.miss_ratio:.4f}"
        )

    plt.figure(figsize=(7, 4.5))
    plt.plot(cache_sizes, miss_ratios, marker="o")
    plt.xlabel("Cache size")
    plt.ylabel("Cache miss ratio")
    plt.title("Day 2: LRU cache-size sweep")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURE_DIR / "day2_lru_cache_size_sweep.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved figure to {output_path}")


if __name__ == "__main__":
    run_cache_size_sweep()