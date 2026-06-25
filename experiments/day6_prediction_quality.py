"""
Day 6 experiment: prediction quality under different error models.

This experiment evaluates next-use prediction quality using mean absolute
prediction error.

Prediction models:
1. exact prediction;
2. Gaussian noise;
3. systematic shifted prediction;
4. corrupted prediction;
5. adversarial prediction.

Output:
    figures/day6_prediction_noise.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from src.caching.prediction_models import (
    add_gaussian_noise_to_predictions,
    add_shift_to_predictions,
    build_adversarial_predictions,
    build_exact_next_use_predictions,
    corrupt_predictions,
    mean_absolute_prediction_error,
)
from src.caching.trace_generators import generate_video_cdn_trace


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)


def run_prediction_quality_experiment() -> None:
    """
    Compare prediction quality under multiple error models.
    """

    requests = generate_video_cdn_trace(
        num_requests=1000,
        num_videos=120,
        hot_video_count=12,
        burst_probability=0.18,
        seed=11,
    )

    exact_predictions = build_exact_next_use_predictions(requests)

    noise_levels = [0, 2, 5, 10, 20, 40]

    exact_errors: list[float] = []
    gaussian_errors: list[float] = []
    shifted_errors: list[float] = []
    corrupted_errors: list[float] = []
    adversarial_errors: list[float] = []

    adversarial_predictions = build_adversarial_predictions(exact_predictions)
    adversarial_error = mean_absolute_prediction_error(
        exact_predictions,
        adversarial_predictions,
    )

    for noise_level in noise_levels:
        exact_error = mean_absolute_prediction_error(
            exact_predictions,
            exact_predictions,
        )

        gaussian_predictions = add_gaussian_noise_to_predictions(
            exact_predictions,
            std=float(noise_level),
            seed=42,
        )

        shifted_predictions = add_shift_to_predictions(
            exact_predictions,
            shift=float(noise_level),
        )

        corrupted_predictions = corrupt_predictions(
            exact_predictions,
            corruption_probability=min(noise_level / 40.0, 1.0),
            seed=42,
        )

        gaussian_error = mean_absolute_prediction_error(
            exact_predictions,
            gaussian_predictions,
        )
        shifted_error = mean_absolute_prediction_error(
            exact_predictions,
            shifted_predictions,
        )
        corrupted_error = mean_absolute_prediction_error(
            exact_predictions,
            corrupted_predictions,
        )

        exact_errors.append(exact_error)
        gaussian_errors.append(gaussian_error)
        shifted_errors.append(shifted_error)
        corrupted_errors.append(corrupted_error)
        adversarial_errors.append(adversarial_error)

        print(
            f"noise_level={noise_level}, "
            f"exact={exact_error:.4f}, "
            f"gaussian={gaussian_error:.4f}, "
            f"shifted={shifted_error:.4f}, "
            f"corrupted={corrupted_error:.4f}, "
            f"adversarial={adversarial_error:.4f}"
        )

    plt.figure(figsize=(7, 4.5))
    plt.plot(noise_levels, exact_errors, marker="o", label="Exact")
    plt.plot(noise_levels, gaussian_errors, marker="s", label="Gaussian noise")
    plt.plot(noise_levels, shifted_errors, marker="^", label="Shifted")
    plt.plot(noise_levels, corrupted_errors, marker="D", label="Corrupted")
    plt.plot(noise_levels, adversarial_errors, marker="x", label="Adversarial")

    plt.xlabel("Noise level")
    plt.ylabel("Mean absolute prediction error")
    plt.title("Day 6: Next-use prediction error models")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURE_DIR / "day6_prediction_noise.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved figure to {output_path}")


if __name__ == "__main__":
    run_prediction_quality_experiment()