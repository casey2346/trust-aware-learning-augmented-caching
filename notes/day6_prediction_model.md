# Day 6: Prediction Model

## Goal

Day 6 defines the prediction model used for learning-augmented caching.

The project does not yet implement prediction-augmented caching. Instead, Day 6 focuses on defining what a prediction means, how prediction error is measured, and how unreliable predictions can be generated for later experiments.

## Prediction Type

The project uses next-use prediction.

At time t, for each item i, the prediction is:

p_t(i) = predicted next request time of item i after time t

This means the model predicts when an item will next appear in the request sequence.

## Why Next-Use Prediction

Next-use prediction is simple and closely related to Belady's offline optimal algorithm.

Belady evicts the cached item whose true next future request is farthest away. Since an online algorithm cannot know the true future, a prediction-augmented caching algorithm can instead use predicted next-use times.

If predictions are accurate, prediction-guided eviction may approximate Belady-style behavior.

If predictions are inaccurate, prediction-guided eviction may evict useful items and increase cache misses.

## Exact Prediction

Exact prediction uses the true next request time.

This is not available to a real online algorithm, but it provides a clean reference point.

Exact prediction should have zero prediction error.

## Gaussian Noise

Gaussian noise adds random perturbation to the true next-use time.

This models predictions that are roughly correct but noisy.

As the noise level increases, prediction error should increase.

## Shifted Prediction

Shifted prediction adds a systematic offset to the true next-use time.

This models a biased prediction system that consistently predicts requests too early or too late.

## Corrupted Prediction

Corrupted prediction randomly replaces some predictions with incorrect future times.

This models partial prediction failure where some predictions are unreliable.

## Adversarial Prediction

Adversarial prediction intentionally reverses useful next-use information.

Items needed soon may be predicted as far away, while items far away may be predicted as soon.

This models worst-case prediction failure.

## Prediction Error Metric

The main prediction-quality metric is mean absolute prediction error:

MAE = average |true_next_use - predicted_next_use|

Lower MAE means more accurate predictions.

Higher MAE means less reliable predictions.

## Implementation

Implemented file:

src/caching/prediction_models.py

The file includes:

* build_exact_next_use_predictions
* add_gaussian_noise_to_predictions
* add_shift_to_predictions
* corrupt_predictions
* build_adversarial_predictions
* mean_absolute_prediction_error

## Experiment

Implemented file:

experiments/day6_prediction_quality.py

Generated figure:

figures/day6_prediction_noise.png

The experiment compares prediction error across exact, Gaussian, shifted, corrupted, and adversarial prediction models.

## Expected Result

Exact prediction should have zero error.

Gaussian prediction error should increase as noise increases.

Shifted prediction error should increase as shift increases.

Corrupted prediction error should increase as the corruption probability increases.

Adversarial prediction should have high error because it intentionally misleads the algorithm.

## Research Significance

Day 6 creates the prediction layer needed for learning-augmented caching.

Later, prediction-augmented caching will use predicted next-use times to decide which item to evict.

Trust-aware caching will then decide how much to trust these predictions compared with a robust LRU fallback.

## Core Conclusion

Next-use prediction provides a direct bridge between Belady's offline optimal algorithm and prediction-augmented online caching.

Accurate predictions may help online caching approach Belady-like behavior, but unreliable predictions create the need for trust-aware fallback.

## Day 6 Output

Completed:

* defined next-use prediction;
* implemented exact prediction;
* implemented Gaussian noisy prediction;
* implemented shifted prediction;
* implemented corrupted prediction;
* implemented adversarial prediction;
* measured mean absolute prediction error;
* generated a prediction-error figure.

Files produced:

* src/caching/prediction_models.py
* experiments/day6_prediction_quality.py
* figures/day6_prediction_noise.png
* notes/day6_prediction_model.md
