"""
Day 10 experiment: Zipf-distributed request traces.

This experiment evaluates caching algorithms under skewed popularity
distributions. Zipf traces are useful because CDN, video, web, and storage
request workloads often have long-tail popularity patterns.

Experiment settings:
    Zipf alpha = 0.6, 0.8, 1.0, 1.2
    cache size = 10, 20, 50

Algorithms compared:
    Belady optimal offline caching
    LRU
    FIFO
    prediction-augmented caching
    trust-aware caching with c=0.50

Core message:
    Under realistic skewed popularity, prediction-aware caching can help,
    but robustness still depends on prediction reliability.

Output:
    figures/day10_zipf_cache_miss_ratio.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from src.caching.belady import run_belady_cache
from src.caching.fifo import run_fifo_cache
from src.caching.lru import run_lru_cache
from src.caching.prediction_augmented import run_prediction_augmented_cache
from src.caching.prediction_models import (
    build_exact_next_use_predictions,
    corrupt_predictions,
)
from src.caching.trace_generators import generate_zipf_trace
from src.caching.trust_aware import run_trust_aware_cache


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)


def run_zipf_experiment() -> None:
    """
    Run caching experiments under Zipf-distributed request traces.
    """

    zipf_alphas = [0.6, 0.8, 1.0, 1.2]
    cache_sizes = [10, 20, 50]

    num_requests = 2000
    num_items = 300

    results: dict[str, list[float]] = {
        "Belady": [],
        "LRU": [],
        "FIFO": [],
        "Prediction exact": [],
        "Prediction corrupted": [],
        "Trust-aware c=0.50": [],
    }

    x_labels: list[str] = []

    for alpha in zipf_alphas:
        requests = generate_zipf_trace(
            num_requests=num_requests,
            num_items=num_items,
            alpha=alpha,
            seed=100 + int(alpha * 10),
        )

        exact_predictions = build_exact_next_use_predictions(requests)
        corrupted_predictions = corrupt_predictions(
            exact_predictions,
            corruption_probability=0.35,
            seed=100 + int(alpha * 10),
        )

        for cache_size in cache_sizes:
            belady = run_belady_cache(requests, cache_size)
            lru = run_lru_cache(requests, cache_size)
            fifo = run_fifo_cache(requests, cache_size)

            prediction_exact = run_prediction_augmented_cache(
                requests=requests,
                cache_size=cache_size,
                predictions=exact_predictions,
            )

            prediction_corrupted = run_prediction_augmented_cache(
                requests=requests,
                cache_size=cache_size,
                predictions=corrupted_predictions,
            )

            trust_aware = run_trust_aware_cache(
                requests=requests,
                cache_size=cache_size,
                predictions=corrupted_predictions,
                confidence=0.50,
            )

            results["Belady"].append(belady.miss_ratio)
            results["LRU"].append(lru.miss_ratio)
            results["FIFO"].append(fifo.miss_ratio)
            results["Prediction exact"].append(prediction_exact.miss_ratio)
            results["Prediction corrupted"].append(prediction_corrupted.miss_ratio)
            results["Trust-aware c=0.50"].append(trust_aware.miss_ratio)

            x_labels.append(f"α={alpha}, k={cache_size}")

            print(
                f"alpha={alpha:.1f}, cache_size={cache_size}, "
                f"Belady={belady.miss_ratio:.4f}, "
                f"LRU={lru.miss_ratio:.4f}, "
                f"FIFO={fifo.miss_ratio:.4f}, "
                f"PredExact={prediction_exact.miss_ratio:.4f}, "
                f"PredCorrupt={prediction_corrupted.miss_ratio:.4f}, "
                f"Trust050={trust_aware.miss_ratio:.4f}"
            )

    x_positions = list(range(len(x_labels)))

    plt.figure(figsize=(12, 5.8))

    for algorithm_name, miss_ratios in results.items():
        plt.plot(
            x_positions,
            miss_ratios,
            marker="o",
            label=algorithm_name,
        )

    plt.xticks(x_positions, x_labels, rotation=45, ha="right")
    plt.xlabel("Zipf skew alpha and cache size")
    plt.ylabel("Cache miss ratio")
    plt.title("Day 10: Zipf request traces and cache miss ratio")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURE_DIR / "day10_zipf_cache_miss_ratio.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved figure to {output_path}")


if __name__ == "__main__":
    run_zipf_experiment()