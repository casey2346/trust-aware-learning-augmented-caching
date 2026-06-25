"""
Day 7 experiment: prediction-augmented caching.

This experiment compares:

1. Belady optimal offline caching;
2. LRU online caching;
3. prediction-augmented caching with exact predictions;
4. prediction-augmented caching with noisy predictions;
5. prediction-augmented caching with adversarial predictions.

Core message:
    Prediction-augmented caching can approach Belady when predictions are
    accurate, but it may perform worse than LRU when predictions are unreliable.

Output:
    figures/day7_prediction_augmented_vs_lru.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from src.caching.belady import run_belady_cache
from src.caching.lru import run_lru_cache
from src.caching.prediction_augmented import run_prediction_augmented_cache
from src.caching.prediction_models import (
    add_gaussian_noise_to_predictions,
    build_adversarial_predictions,
    build_exact_next_use_predictions,
    corrupt_predictions,
)
from src.caching.trace_generators import generate_video_cdn_trace


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)


def run_prediction_augmented_experiment() -> None:
    """
    Compare prediction-augmented caching against Belady and LRU.
    """

    requests = generate_video_cdn_trace(
        num_requests=1200,
        num_videos=150,
        hot_video_count=12,
        burst_probability=0.18,
        seed=21,
    )

    cache_sizes = list(range(2, 31, 2))

    belady_ratios: list[float] = []
    lru_ratios: list[float] = []
    exact_prediction_ratios: list[float] = []
    noisy_prediction_ratios: list[float] = []
    corrupted_prediction_ratios: list[float] = []
    adversarial_prediction_ratios: list[float] = []

    exact_predictions = build_exact_next_use_predictions(requests)

    noisy_predictions = add_gaussian_noise_to_predictions(
        exact_predictions,
        std=25.0,
        seed=7,
    )

    corrupted_predictions = corrupt_predictions(
        exact_predictions,
        corruption_probability=0.35,
        seed=7,
    )

    adversarial_predictions = build_adversarial_predictions(exact_predictions)

    for cache_size in cache_sizes:
        belady_result = run_belady_cache(requests, cache_size)
        lru_result = run_lru_cache(requests, cache_size)

        exact_result = run_prediction_augmented_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=exact_predictions,
        )

        noisy_result = run_prediction_augmented_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=noisy_predictions,
        )

        corrupted_result = run_prediction_augmented_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=corrupted_predictions,
        )

        adversarial_result = run_prediction_augmented_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=adversarial_predictions,
        )

        belady_ratios.append(belady_result.miss_ratio)
        lru_ratios.append(lru_result.miss_ratio)
        exact_prediction_ratios.append(exact_result.miss_ratio)
        noisy_prediction_ratios.append(noisy_result.miss_ratio)
        corrupted_prediction_ratios.append(corrupted_result.miss_ratio)
        adversarial_prediction_ratios.append(adversarial_result.miss_ratio)

        print(
            f"cache_size={cache_size}, "
            f"Belady={belady_result.miss_ratio:.4f}, "
            f"LRU={lru_result.miss_ratio:.4f}, "
            f"PredExact={exact_result.miss_ratio:.4f}, "
            f"PredNoisy={noisy_result.miss_ratio:.4f}, "
            f"PredCorrupt={corrupted_result.miss_ratio:.4f}, "
            f"PredAdv={adversarial_result.miss_ratio:.4f}"
        )

    plt.figure(figsize=(8, 5))
    plt.plot(cache_sizes, belady_ratios, marker="o", label="Belady optimal")
    plt.plot(cache_sizes, lru_ratios, marker="s", label="LRU")
    plt.plot(cache_sizes, exact_prediction_ratios, marker="^", label="Prediction exact")
    plt.plot(cache_sizes, noisy_prediction_ratios, marker="D", label="Prediction noisy")
    plt.plot(cache_sizes, corrupted_prediction_ratios, marker="v", label="Prediction corrupted")
    plt.plot(cache_sizes, adversarial_prediction_ratios, marker="x", label="Prediction adversarial")

    plt.xlabel("Cache size")
    plt.ylabel("Cache miss ratio")
    plt.title("Day 7: Prediction-augmented caching vs LRU")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURE_DIR / "day7_prediction_augmented_vs_lru.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved figure to {output_path}")


if __name__ == "__main__":
    run_prediction_augmented_experiment()