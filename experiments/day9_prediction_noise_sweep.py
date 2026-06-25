"""
Day 9 experiment: prediction noise sweep.

This experiment studies how caching algorithms behave as prediction quality
gets worse.

Noise level ranges from 0% to 100%.

Algorithms compared:
1. Belady optimal offline caching;
2. LRU;
3. FIFO;
4. prediction-augmented caching;
5. trust-aware caching with c=0.25;
6. trust-aware caching with c=0.50;
7. trust-aware caching with c=0.75.

Core message:
    Prediction-augmented caching can perform very well when predictions are
    accurate, but it degrades as predictions become corrupted. Trust-aware
    caching is more stable because confidence controls fallback toward LRU.

Output:
    figures/day9_prediction_noise_sweep.png
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
from src.caching.trace_generators import generate_video_cdn_trace
from src.caching.trust_aware import run_trust_aware_cache


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)


def run_prediction_noise_sweep() -> None:
    """
    Run prediction noise sweep from 0% to 100% corruption.
    """

    requests = generate_video_cdn_trace(
        num_requests=1500,
        num_videos=180,
        hot_video_count=15,
        burst_probability=0.20,
        seed=91,
    )

    cache_size = 15
    noise_levels = [i / 10 for i in range(0, 11)]
    noise_percentages = [int(level * 100) for level in noise_levels]

    exact_predictions = build_exact_next_use_predictions(requests)

    belady_result = run_belady_cache(requests, cache_size)
    lru_result = run_lru_cache(requests, cache_size)
    fifo_result = run_fifo_cache(requests, cache_size)

    belady_ratios: list[float] = []
    lru_ratios: list[float] = []
    fifo_ratios: list[float] = []
    prediction_augmented_ratios: list[float] = []
    trust_025_ratios: list[float] = []
    trust_050_ratios: list[float] = []
    trust_075_ratios: list[float] = []

    for noise_level in noise_levels:
        corrupted_predictions = corrupt_predictions(
            exact_predictions,
            corruption_probability=noise_level,
            seed=123,
        )

        prediction_augmented = run_prediction_augmented_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=corrupted_predictions,
        )

        trust_025 = run_trust_aware_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=corrupted_predictions,
            confidence=0.25,
        )

        trust_050 = run_trust_aware_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=corrupted_predictions,
            confidence=0.50,
        )

        trust_075 = run_trust_aware_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=corrupted_predictions,
            confidence=0.75,
        )

        belady_ratios.append(belady_result.miss_ratio)
        lru_ratios.append(lru_result.miss_ratio)
        fifo_ratios.append(fifo_result.miss_ratio)
        prediction_augmented_ratios.append(prediction_augmented.miss_ratio)
        trust_025_ratios.append(trust_025.miss_ratio)
        trust_050_ratios.append(trust_050.miss_ratio)
        trust_075_ratios.append(trust_075.miss_ratio)

        print(
            f"noise={int(noise_level * 100):3d}%, "
            f"Belady={belady_result.miss_ratio:.4f}, "
            f"LRU={lru_result.miss_ratio:.4f}, "
            f"FIFO={fifo_result.miss_ratio:.4f}, "
            f"PredAug={prediction_augmented.miss_ratio:.4f}, "
            f"Trust025={trust_025.miss_ratio:.4f}, "
            f"Trust050={trust_050.miss_ratio:.4f}, "
            f"Trust075={trust_075.miss_ratio:.4f}"
        )

    plt.figure(figsize=(8.5, 5.2))

    plt.plot(noise_percentages, belady_ratios, marker="o", label="Belady optimal")
    plt.plot(noise_percentages, lru_ratios, marker="s", label="LRU")
    plt.plot(noise_percentages, fifo_ratios, marker="^", label="FIFO")
    plt.plot(
        noise_percentages,
        prediction_augmented_ratios,
        marker="D",
        label="Prediction-augmented",
    )
    plt.plot(noise_percentages, trust_025_ratios, marker="v", label="Trust-aware c=0.25")
    plt.plot(noise_percentages, trust_050_ratios, marker="x", label="Trust-aware c=0.50")
    plt.plot(noise_percentages, trust_075_ratios, marker="P", label="Trust-aware c=0.75")

    plt.xlabel("Prediction noise level (%)")
    plt.ylabel("Cache miss ratio")
    plt.title("Day 9: Prediction noise sweep")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURE_DIR / "day9_prediction_noise_sweep.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved figure to {output_path}")


if __name__ == "__main__":
    run_prediction_noise_sweep()