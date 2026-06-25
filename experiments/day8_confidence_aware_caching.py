"""
Day 8 experiment: confidence-aware trust-aware caching.

This experiment studies how confidence controls the trade-off between
prediction-guided eviction and LRU fallback.

It compares:
1. Belady optimal offline caching;
2. LRU online caching;
3. prediction-augmented caching;
4. trust-aware caching with different confidence values.

Output:
    figures/day8_confidence_ablation.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from src.caching.belady import run_belady_cache
from src.caching.lru import run_lru_cache
from src.caching.prediction_augmented import run_prediction_augmented_cache
from src.caching.prediction_models import (
    build_adversarial_predictions,
    build_exact_next_use_predictions,
    corrupt_predictions,
)
from src.caching.trace_generators import generate_video_cdn_trace
from src.caching.trust_aware import run_trust_aware_cache


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)


def run_confidence_ablation_experiment() -> None:
    """
    Evaluate trust-aware caching under different confidence values.
    """

    requests = generate_video_cdn_trace(
        num_requests=1200,
        num_videos=150,
        hot_video_count=12,
        burst_probability=0.18,
        seed=31,
    )

    cache_size = 12
    confidence_values = [0.0, 0.25, 0.5, 0.75, 1.0]

    exact_predictions = build_exact_next_use_predictions(requests)
    corrupted_predictions = corrupt_predictions(
        exact_predictions,
        corruption_probability=0.35,
        seed=31,
    )
    adversarial_predictions = build_adversarial_predictions(exact_predictions)

    belady_result = run_belady_cache(requests, cache_size)
    lru_result = run_lru_cache(requests, cache_size)

    pred_exact_result = run_prediction_augmented_cache(
        requests=requests,
        cache_size=cache_size,
        predictions=exact_predictions,
    )

    pred_corrupt_result = run_prediction_augmented_cache(
        requests=requests,
        cache_size=cache_size,
        predictions=corrupted_predictions,
    )

    pred_adv_result = run_prediction_augmented_cache(
        requests=requests,
        cache_size=cache_size,
        predictions=adversarial_predictions,
    )

    trust_exact_ratios: list[float] = []
    trust_corrupt_ratios: list[float] = []
    trust_adv_ratios: list[float] = []

    for confidence in confidence_values:
        trust_exact = run_trust_aware_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=exact_predictions,
            confidence=confidence,
        )

        trust_corrupt = run_trust_aware_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=corrupted_predictions,
            confidence=confidence,
        )

        trust_adv = run_trust_aware_cache(
            requests=requests,
            cache_size=cache_size,
            predictions=adversarial_predictions,
            confidence=confidence,
        )

        trust_exact_ratios.append(trust_exact.miss_ratio)
        trust_corrupt_ratios.append(trust_corrupt.miss_ratio)
        trust_adv_ratios.append(trust_adv.miss_ratio)

        print(
            f"confidence={confidence:.2f}, "
            f"TrustExact={trust_exact.miss_ratio:.4f}, "
            f"TrustCorrupt={trust_corrupt.miss_ratio:.4f}, "
            f"TrustAdv={trust_adv.miss_ratio:.4f}"
        )

    print(f"Belady={belady_result.miss_ratio:.4f}")
    print(f"LRU={lru_result.miss_ratio:.4f}")
    print(f"PredictionExact={pred_exact_result.miss_ratio:.4f}")
    print(f"PredictionCorrupt={pred_corrupt_result.miss_ratio:.4f}")
    print(f"PredictionAdversarial={pred_adv_result.miss_ratio:.4f}")

    plt.figure(figsize=(8, 5))
    plt.axhline(
        belady_result.miss_ratio,
        linestyle="--",
        label="Belady optimal",
    )
    plt.axhline(
        lru_result.miss_ratio,
        linestyle="--",
        label="LRU fallback",
    )
    plt.axhline(
        pred_exact_result.miss_ratio,
        linestyle=":",
        label="Prediction exact",
    )
    plt.axhline(
        pred_adv_result.miss_ratio,
        linestyle=":",
        label="Prediction adversarial",
    )

    plt.plot(
        confidence_values,
        trust_exact_ratios,
        marker="o",
        label="Trust-aware exact",
    )
    plt.plot(
        confidence_values,
        trust_corrupt_ratios,
        marker="s",
        label="Trust-aware corrupted",
    )
    plt.plot(
        confidence_values,
        trust_adv_ratios,
        marker="^",
        label="Trust-aware adversarial",
    )

    plt.xlabel("Confidence in predictions")
    plt.ylabel("Cache miss ratio")
    plt.title("Day 8: Confidence-aware caching ablation")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURE_DIR / "day8_confidence_ablation.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved figure to {output_path}")


if __name__ == "__main__":
    run_confidence_ablation_experiment()