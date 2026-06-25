"""
Prediction models for learning-augmented caching.

This file defines next-use prediction models. At time t, the model predicts
when each item will next be requested:

    predicted_next_use[item] = predicted next request time of item

These predictions will later be used by prediction-augmented caching policies.
If predictions are accurate, evicting the item with farthest predicted next use
can approximate Belady-style behavior. If predictions are unreliable, the same
strategy may fail.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, List

import numpy as np

from src.caching.problem import Item, RequestSequence, validate_request_sequence


PredictionMap = Dict[Item, float]
PredictionSequence = List[PredictionMap]


def build_exact_next_use_predictions(
    requests: RequestSequence,
    no_future_value: float | None = None,
) -> PredictionSequence:
    """
    Build exact next-use predictions for every time step.

    At each time t, the prediction map stores the true next request time of
    every item after time t. If an item never appears again, it receives
    no_future_value.

    Args:
        requests: Request sequence.
        no_future_value: Value used when an item has no future request.

    Returns:
        A list of prediction maps, one map per time step.
    """

    validate_request_sequence(requests)

    if no_future_value is None:
        no_future_value = float(len(requests) + 1)

    unique_items = sorted(set(requests))
    next_seen: PredictionMap = {item: no_future_value for item in unique_items}
    predictions: PredictionSequence = [{} for _ in requests]

    for time_index in range(len(requests) - 1, -1, -1):
        predictions[time_index] = deepcopy(next_seen)
        current_item = requests[time_index]
        next_seen[current_item] = float(time_index)

    return predictions


def add_gaussian_noise_to_predictions(
    exact_predictions: PredictionSequence,
    std: float,
    seed: int = 0,
) -> PredictionSequence:
    """
    Add Gaussian noise to exact next-use predictions.

    Args:
        exact_predictions: Exact prediction maps.
        std: Standard deviation of Gaussian noise.
        seed: Random seed.

    Returns:
        Noisy prediction maps.
    """

    if std < 0:
        raise ValueError("std must be non-negative.")

    rng = np.random.default_rng(seed)
    noisy_predictions: PredictionSequence = []

    for time_index, prediction_map in enumerate(exact_predictions):
        noisy_map: PredictionMap = {}

        for item, true_next_use in prediction_map.items():
            noisy_value = true_next_use + float(rng.normal(loc=0.0, scale=std))
            noisy_map[item] = max(float(time_index + 1), noisy_value)

        noisy_predictions.append(noisy_map)

    return noisy_predictions


def add_shift_to_predictions(
    exact_predictions: PredictionSequence,
    shift: float,
) -> PredictionSequence:
    """
    Add a systematic shift to next-use predictions.

    Positive shift means the model predicts requests later than reality.
    Negative shift means the model predicts requests earlier than reality.

    Args:
        exact_predictions: Exact prediction maps.
        shift: Additive prediction shift.

    Returns:
        Shifted prediction maps.
    """

    shifted_predictions: PredictionSequence = []

    for time_index, prediction_map in enumerate(exact_predictions):
        shifted_map: PredictionMap = {}

        for item, true_next_use in prediction_map.items():
            shifted_map[item] = max(float(time_index + 1), true_next_use + shift)

        shifted_predictions.append(shifted_map)

    return shifted_predictions


def corrupt_predictions(
    exact_predictions: PredictionSequence,
    corruption_probability: float,
    seed: int = 0,
) -> PredictionSequence:
    """
    Randomly corrupt a fraction of next-use predictions.

    Corrupted predictions are replaced by random future times.

    Args:
        exact_predictions: Exact prediction maps.
        corruption_probability: Probability of corrupting each prediction.
        seed: Random seed.

    Returns:
        Corrupted prediction maps.
    """

    if not 0 <= corruption_probability <= 1:
        raise ValueError("corruption_probability must be in [0, 1].")

    rng = np.random.default_rng(seed)
    horizon = len(exact_predictions) + 1

    corrupted_predictions: PredictionSequence = []

    for time_index, prediction_map in enumerate(exact_predictions):
        corrupted_map: PredictionMap = {}

        for item, true_next_use in prediction_map.items():
            if rng.random() < corruption_probability:
                corrupted_map[item] = float(rng.integers(time_index + 1, horizon + 1))
            else:
                corrupted_map[item] = true_next_use

        corrupted_predictions.append(corrupted_map)

    return corrupted_predictions


def build_adversarial_predictions(
    exact_predictions: PredictionSequence,
) -> PredictionSequence:
    """
    Build adversarial next-use predictions.

    This model intentionally reverses useful next-use information:
    items that are needed soon are predicted to be far away, while items that
    are far away are predicted to be needed soon.

    Args:
        exact_predictions: Exact prediction maps.

    Returns:
        Adversarial prediction maps.
    """

    horizon = len(exact_predictions) + 1
    adversarial_predictions: PredictionSequence = []

    for time_index, prediction_map in enumerate(exact_predictions):
        adversarial_map: PredictionMap = {}

        finite_values = list(prediction_map.values())

        if not finite_values:
            adversarial_predictions.append(adversarial_map)
            continue

        min_next_use = min(finite_values)
        max_next_use = max(finite_values)

        for item, true_next_use in prediction_map.items():
            if true_next_use <= min_next_use + 1:
                adversarial_map[item] = float(horizon)
            elif true_next_use >= max_next_use - 1:
                adversarial_map[item] = float(time_index + 1)
            else:
                adversarial_map[item] = float(horizon + time_index - true_next_use)

        adversarial_predictions.append(adversarial_map)

    return adversarial_predictions


def mean_absolute_prediction_error(
    exact_predictions: PredictionSequence,
    predicted_predictions: PredictionSequence,
) -> float:
    """
    Compute mean absolute prediction error.

    Args:
        exact_predictions: Exact next-use predictions.
        predicted_predictions: Predicted next-use predictions.

    Returns:
        Mean absolute error across time steps and items.
    """

    if len(exact_predictions) != len(predicted_predictions):
        raise ValueError("Prediction sequences must have the same length.")

    total_error = 0.0
    total_count = 0

    for exact_map, predicted_map in zip(exact_predictions, predicted_predictions):
        for item, true_next_use in exact_map.items():
            if item not in predicted_map:
                raise ValueError(f"Missing prediction for item {item}.")

            total_error += abs(true_next_use - predicted_map[item])
            total_count += 1

    if total_count == 0:
        raise ValueError("No predictions available for error computation.")

    return total_error / total_count


if __name__ == "__main__":
    example_requests = [1, 2, 3, 1, 4, 1, 2, 5]

    exact = build_exact_next_use_predictions(example_requests)
    gaussian = add_gaussian_noise_to_predictions(exact, std=2.0, seed=1)
    shifted = add_shift_to_predictions(exact, shift=3.0)
    corrupted = corrupt_predictions(exact, corruption_probability=0.25, seed=1)
    adversarial = build_adversarial_predictions(exact)

    print("Prediction model example")
    print("Requests:", example_requests)
    print("Exact prediction at t=0:", exact[0])
    print("Gaussian prediction at t=0:", gaussian[0])
    print("Shifted prediction at t=0:", shifted[0])
    print("Corrupted prediction at t=0:", corrupted[0])
    print("Adversarial prediction at t=0:", adversarial[0])

    print("Gaussian MAE:", round(mean_absolute_prediction_error(exact, gaussian), 4))
    print("Shifted MAE:", round(mean_absolute_prediction_error(exact, shifted), 4))
    print("Corrupted MAE:", round(mean_absolute_prediction_error(exact, corrupted), 4))
    print("Adversarial MAE:", round(mean_absolute_prediction_error(exact, adversarial), 4))